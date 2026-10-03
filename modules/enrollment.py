import cv2
import numpy as np
from pathlib import Path

from modules.face_detector import FaceDetector
from modules.face_recognizer import FaceRecognizer
from modules.database import add_person


EMBEDDING_DIR = Path("data/embeddings")


class Enrollment:

    def __init__(self):

        self.detector = FaceDetector()
        self.recognizer = FaceRecognizer()

        EMBEDDING_DIR.mkdir(
            parents=True,
            exist_ok=True
        )

    def enroll_person(
        self,
        person_id,
        name,
        required_samples=5
    ):

        camera = cv2.VideoCapture(0)

        if not camera.isOpened():
            print("Could not open webcam.")
            return False

        embeddings = []

        print()
        print("Enrollment started.")
        print("Look directly at the camera.")
        print(f"Collecting {required_samples} samples...")
        print()

        while len(embeddings) < required_samples:

            ret, frame = camera.read()

            if not ret:
                continue

            faces = self.detector.detect_faces(frame)

            if len(faces) == 1:

                face = faces[0]

                embedding = self.recognizer.get_embedding(face)

                embeddings.append(embedding)

                x1, y1, x2, y2 = face.bbox.astype(int)

                cv2.rectangle(
                    frame,
                    (x1, y1),
                    (x2, y2),
                    (0, 255, 0),
                    2
                )

                cv2.putText(
                    frame,
                    f"Samples: {len(embeddings)}/{required_samples}",
                    (20, 40),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    0.8,
                    (0, 255, 0),
                    2
                )

            else:

                cv2.putText(
                    frame,
                    "Please show exactly one face",
                    (20, 40),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    0.7,
                    (0, 0, 255),
                    2
                )

            cv2.imshow(
                "Face Enrollment",
                frame
            )

            if cv2.waitKey(500) & 0xFF == ord("q"):
                break

        camera.release()
        cv2.destroyAllWindows()

        if len(embeddings) < required_samples:

            print("Enrollment cancelled.")

            return False

        average_embedding = np.mean(
            embeddings,
            axis=0
        )

        average_embedding = (
            average_embedding /
            np.linalg.norm(average_embedding)
        )

        embedding_path = (
            EMBEDDING_DIR /
            f"{person_id}.npy"
        )

        np.save(
            embedding_path,
            average_embedding
        )

        add_person(
            person_id,
            name
        )

        print()
        print("Enrollment successful!")
        print(f"Person ID: {person_id}")
        print(f"Name: {name}")
        print(f"Embedding: {embedding_path}")

        return True