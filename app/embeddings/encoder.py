import numpy as np
from sentence_transformers import SentenceTransformer


class Embedder:
    def __init__(self, model_name: str) -> None:
        self.model = SentenceTransformer(model_name)

    def dimension(self) -> int:
        return self.model.get_sentence_embedding_dimension()

    def embed_texts(self, texts: list[str]) -> np.ndarray:
        vectors = self.model.encode(texts, normalize_embeddings=True)
        return np.array(vectors, dtype="float32")

    def embed_query(self, text: str) -> np.ndarray:
        return self.embed_texts([text])
