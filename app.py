from modules.database import create_database
from modules.enrollment import Enrollment


def main():

    create_database()

    print("==============================")
    print(" AI FACE ATTENDANCE SYSTEM")
    print("==============================")

    print()
    print("1. Enroll Person")
    print("2. Exit")

    choice = input("Select option: ")

    if choice == "1":

        person_id = input("Enter Person ID: ")
        name = input("Enter Person Name: ")

        enrollment = Enrollment()

        enrollment.enroll_person(
            person_id,
            name,
            required_samples=5
        )

    elif choice == "2":

        print("Goodbye.")

    else:

        print("Invalid option.")


if __name__ == "__main__":
    main()