import numpy as np

class FaceRecognizer:

    def get_embedding(self, face):
        
        embedding = face.embedding.astype(np.float32)

        norm = np.linalg.norm(embedding)

        if norm == 0:
            return embedding

        return embedding / norm

    def cosine_similarity(self, embedding1, embedding2):

        embedding1 = np.asarray(
            embedding1,
            dtype=np.float32
        )

        embedding2 = np.asarray(
            embedding2,
            dtype=np.float32
        )

        norm1 = np.linalg.norm(embedding1)
        norm2 = np.linalg.norm(embedding2)

        if norm1 == 0 or norm2 == 0:
            return 0.0

        return float(
            np.dot(embedding1, embedding2)
            / (norm1 * norm2)
        )