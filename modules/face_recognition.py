import numpy as np
from pathlib import Path

from modules.face_detector import FaceDetector
from modules.face_recognizer import FaceRecognizer
from modules.database import get_person


EMBEDDING_DIR = Path("data/embeddings")


class FaceRecognition:

    def __init__(self, threshold=0.50):

        self.detector = FaceDetector()
        self.recognizer = FaceRecognizer()

        self.threshold = threshold

        self.embeddings = {}

        self.load_embeddings()

    def load_embeddings(self):

        self.embeddings = {}

        if not EMBEDDING_DIR.exists():
            return

        for file in EMBEDDING_DIR.glob("*.npy"):

            person_id = file.stem

            embedding = np.load(file)

            self.embeddings[person_id] = embedding

        print(
            f"Loaded {len(self.embeddings)} "
            f"registered face(s)."
        )

    def recognize(self, face):

        if not self.embeddings:
            return None, 0.0

        live_embedding = (
            self.recognizer.get_embedding(face)
        )

        best_person = None
        best_similarity = -1.0

        for person_id, saved_embedding in self.embeddings.items():

            similarity = (
                self.recognizer.cosine_similarity(
                    live_embedding,
                    saved_embedding
                )
            )

            if similarity > best_similarity:

                best_similarity = similarity
                best_person = person_id

        if best_similarity >= self.threshold:

            person = get_person(best_person)

            if person:

                return (
                    person,
                    best_similarity
                )

        return None, best_similarity