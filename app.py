import cv2

from modules.database import create_database
from modules.face_recognition import FaceRecognition


def main():

    create_database()

    recognizer = FaceRecognition(
        threshold=0.50
    )

    camera = cv2.VideoCapture(0)

    if not camera.isOpened():

        print("Could not open webcam.")

        return

    print()
    print("Face recognition started.")
    print("Press Q to quit.")

    while True:

        ret, frame = camera.read()

        if not ret:
            break

        faces = recognizer.detector.detect_faces(
            frame
        )

        for face in faces:

            x1, y1, x2, y2 = (
                face.bbox.astype(int)
            )

            person, similarity = (
                recognizer.recognize(face)
            )

            if person:

                person_id, name = person

                label = (
                    f"{name} "
                    f"({similarity:.2f})"
                )

            else:

                label = (
                    f"Unknown "
                    f"({similarity:.2f})"
                )

            cv2.rectangle(
                frame,
                (x1, y1),
                (x2, y2),
                (0, 255, 0),
                2
            )

            cv2.putText(
                frame,
                label,
                (x1, y1 - 10),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.7,
                (0, 255, 0),
                2
            )

        cv2.imshow(
            "AI Face Recognition",
            frame
        )

        if cv2.waitKey(1) & 0xFF == ord("q"):
            break

    camera.release()

    cv2.destroyAllWindows()


if __name__ == "__main__":
    main()