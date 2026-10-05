import cv2
import uuid

from modules.database import create_database
from modules.face_recognition import FaceRecognition
from modules.attendance import AttendanceManager


def main():

    create_database()

    session_id = str(uuid.uuid4())

    print()
    print("==============================")
    print(" AI FACE ATTENDANCE SYSTEM")
    print("==============================")
    print()
    print(f"Session: {session_id}")
    print("Press Q to quit.")
    print()

    recognizer = FaceRecognition(
        threshold=0.50
    )

    attendance = AttendanceManager(
        required_frames=5
    )

    camera = cv2.VideoCapture(0)

    if not camera.isOpened():

        print("Could not open webcam.")

        return

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
                    f"{similarity:.2f}"
                )

                marked = attendance.update(
                    person,
                    session_id
                )

                if marked:

                    label = (
                        f"{name} - PRESENT"
                    )

            else:

                label = (
                    f"Unknown "
                    f"{similarity:.2f}"
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
            "AI Face Attendance",
            frame
        )

        if cv2.waitKey(1) & 0xFF == ord("q"):
            break

    camera.release()
    cv2.destroyAllWindows()

    print()
    print("Attendance session ended.")


if __name__ == "__main__":
    main()