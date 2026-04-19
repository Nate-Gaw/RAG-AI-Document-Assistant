import os
import re

from dotenv import load_dotenv
from fastapi import FastAPI, File, HTTPException, UploadFile
from pydantic import BaseModel

from app.embeddings.encoder import Embedder
from app.generation.answer import generate_answer
from app.processing.chunker import clean_text, chunk_text
from app.processing.extractor import extract_text
from app.retrieval.vector_store import VectorStore

load_dotenv()

app = FastAPI(title="RAG AI Document Assistant")

DATA_DIR = os.getenv("RAG_DATA_DIR", "data")
INDEX_PATH = os.path.join(DATA_DIR, "faiss.index")
CHUNKS_PATH = os.path.join(DATA_DIR, "chunks.json")
EMBEDDING_MODEL = os.getenv("EMBEDDING_MODEL", "sentence-transformers/all-MiniLM-L6-v2")

embedder = Embedder(EMBEDDING_MODEL)
store = VectorStore.load(embedder.dimension(), INDEX_PATH, CHUNKS_PATH)


class QueryRequest(BaseModel):
    question: str
    top_k: int = 4


@app.get("/health")
def health() -> dict:
    return {"status": "ok", "chunks": len(store.chunks)}


@app.post("/upload")
async def upload(file: UploadFile = File(...)) -> dict:
    content = await file.read()
    text = extract_text(content, file.filename)
    if not text.strip():
        raise HTTPException(status_code=400, detail="No text found in file.")

    cleaned = clean_text(text)
    chunks = chunk_text(cleaned)
    if not chunks:
        raise HTTPException(status_code=400, detail="No chunks produced from file.")

    embeddings = embedder.embed_texts(chunks)
    store.add(embeddings, chunks)
    store.save()
    return {"chunks_added": len(chunks)}


@app.post("/query")
def query(req: QueryRequest) -> dict:
    question = req.question.strip()
    if not question:
        raise HTTPException(status_code=400, detail="Question is required.")
    try:
        query_embedding = embedder.embed_query(question)
        results = store.search(query_embedding, top_k=req.top_k)
        if results:
            top_score = results[0].get("score", 0.0)
        else:
            top_score = 0.0

        if top_score < 0.25:
            tokens = re.findall(r"[A-Za-z0-9']+", question.lower())
            stopwords = {
                "the",
                "is",
                "are",
                "a",
                "an",
                "of",
                "to",
                "for",
                "and",
                "or",
                "what",
                "which",
                "who",
                "when",
                "where",
                "why",
                "how",
                "does",
                "do",
                "did",
                "it",
                "in",
                "on",
                "with",
                "by",
                "about",
                "from",
                "be",
                "as",
                "at",
                "this",
                "that",
                "these",
                "those",
            }
            keywords = [token for token in tokens if token not in stopwords]
            if keywords:
                lexical_hits = []
                for chunk in store.chunks:
                    chunk_lower = chunk.lower()
                    if any(term in chunk_lower for term in keywords):
                        lexical_hits.append({"text": chunk, "score": 1.0})
                        if len(lexical_hits) >= req.top_k:
                            break
                if lexical_hits:
                    results = lexical_hits

        answer, sources = generate_answer(question, results)
        return {"answer": answer, "sources": sources}
    except Exception as exc:
        raise HTTPException(status_code=500, detail=f"Query failed: {exc}") from exc


@app.post("/reset")
def reset() -> dict:
    store.clear()
    store.save()
    return {"status": "cleared"}
