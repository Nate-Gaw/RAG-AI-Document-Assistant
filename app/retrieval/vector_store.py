import json
import os
from typing import Any

import faiss
import numpy as np


class VectorStore:
    def __init__(self, dim: int, index_path: str, chunks_path: str) -> None:
        self.dim = dim
        self.index_path = index_path
        self.chunks_path = chunks_path
        self.index = faiss.IndexFlatIP(dim)
        self.chunks: list[str] = []

    def add(self, embeddings: np.ndarray, chunks: list[str]) -> None:
        if embeddings.size == 0:
            return
        if embeddings.dtype != np.float32:
            embeddings = embeddings.astype("float32")
        self.index.add(embeddings)
        self.chunks.extend(chunks)

    def search(self, query_embedding: np.ndarray, top_k: int = 4) -> list[dict[str, Any]]:
        if self.index.ntotal == 0:
            return []
        if query_embedding.dtype != np.float32:
            query_embedding = query_embedding.astype("float32")
        scores, indices = self.index.search(query_embedding, top_k)
        results = []
        for score, idx in zip(scores[0], indices[0]):
            if idx < 0 or idx >= len(self.chunks):
                continue
            results.append({"text": self.chunks[idx], "score": float(score)})
        return results

    def save(self) -> None:
        os.makedirs(os.path.dirname(self.index_path), exist_ok=True)
        faiss.write_index(self.index, self.index_path)
        with open(self.chunks_path, "w", encoding="utf-8") as file:
            json.dump(self.chunks, file, ensure_ascii=True, indent=2)

    def clear(self) -> None:
        self.index = faiss.IndexFlatIP(self.dim)
        self.chunks = []

    @classmethod
    def load(cls, dim: int, index_path: str, chunks_path: str) -> "VectorStore":
        store = cls(dim, index_path, chunks_path)
        if os.path.exists(index_path):
            store.index = faiss.read_index(index_path)
        if os.path.exists(chunks_path):
            with open(chunks_path, "r", encoding="utf-8") as file:
                store.chunks = json.load(file)
        return store
