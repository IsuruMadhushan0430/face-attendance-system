from collections import defaultdict

from modules.database import mark_attendance


class AttendanceManager:

    def __init__(self, required_frames=5):

        self.required_frames = required_frames

        self.frame_counts = defaultdict(int)

        self.marked_people = set()

    def update(
        self,
        person,
        session_id
    ):

        if person is None:

            return False

        person_id, name = person

        if person_id in self.marked_people:

            return False

        self.frame_counts[person_id] += 1

        current_count = self.frame_counts[person_id]

        print(
            f"{name}: "
            f"{current_count}/"
            f"{self.required_frames}"
        )

        if current_count < self.required_frames:

            return False

        success = mark_attendance(
            person_id,
            name,
            session_id
        )

        if success:

            self.marked_people.add(
                person_id
            )

            print(
                f"✓ Attendance marked: "
                f"{name}"
            )

            return True

        return False