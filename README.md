# RAG AI Document Assistant

A production-style retrieval-augmented generation (RAG) system that ingests documents, stores semantic embeddings, retrieves relevant chunks, and generates grounded answers using retrieved context only.

## Architecture

- app/api: FastAPI request handling
- app/processing: document parsing and chunking
- app/embeddings: embedding generation
- app/retrieval: vector search with FAISS
- app/generation: LLM answer generation
- app/ui: Streamlit frontend

## Quick Start

1) Create and activate a Python environment.
2) Install dependencies:

```
pip install -r requirements.txt
```

3) Start the backend API:

```
uvicorn app.api.main:app --reload
```

4) Start the Streamlit UI:

```
streamlit run app/ui/streamlit_app.py
```

## Environment Variables

- OPENAI_API_KEY (required)
- OPENAI_MODEL (default: gpt-5.2)
- EMBEDDING_MODEL (default: sentence-transformers/all-MiniLM-L6-v2)
- RAG_DATA_DIR (default: data)
- BACKEND_URL (default: http://localhost:8000)

## Notes

- The system will only answer using retrieved chunks. If the answer is not in the context, it responds with uncertainty.
- Uploaded documents are chunked into 300-500 word segments with overlap for better retrieval.
