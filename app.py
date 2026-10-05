import streamlit as st

from modules.database import (
    create_database,
    get_all_attendance
)

create_database()

st.set_page_config(
    page_title="AI Face Attendance",
    page_icon="👤",
    layout="wide"
)

st.sidebar.title("AI Face Attendance")

page = st.sidebar.radio(
    "Navigation",
    [
        "Dashboard",
        "Enroll Person",
        "Live Attendance",
        "Reports"
    ]
)

if page == "Dashboard":

    st.title("📊 Attendance Dashboard")

    attendance = get_all_attendance()

    people = set()

    for record in attendance:
        people.add(record[0])

    total_attendance = len(attendance)
    unique_people = len(people)

    col1, col2, col3 = st.columns(3)

    with col1:

        st.metric(
            "Attendance Records",
            total_attendance
        )

    with col2:

        st.metric(
            "People Present",
            unique_people
        )

    with col3:

        st.metric(
            "System Status",
            "Online"
        )

    st.divider()

    st.subheader("Recent Attendance")

    if attendance:

        for record in attendance[:10]:

            person_id = record[0]
            name = record[1]
            date = record[2]
            time = record[3]

            st.write(
                f"**{name}** "
                f"({person_id}) — "
                f"{date} {time}"
            )

    else:

        st.info(
            "No attendance records yet."
        )

elif page == "Enroll Person":

    st.title("👤 Enroll Person")

    st.write(
        "Register a person in the face recognition system."
    )

    person_id = st.text_input(
        "Person ID",
        placeholder="ST001"
    )

    name = st.text_input(
        "Full Name",
        placeholder="Isuru Madhushan"
    )

    consent = st.checkbox(
        "I confirm that this person has provided "
        "consent for biometric enrollment."
    )

    if st.button(
        "Start Enrollment",
        type="primary"
    ):

        if not person_id or not name:

            st.error(
                "Please enter Person ID and Name."
            )

        elif not consent:

            st.error(
                "Consent is required before enrollment."
            )

        else:

            st.success(
                "Enrollment module will be connected here."
            )

elif page == "Live Attendance":

    st.title("📷 Live Attendance")

    st.info(
        "Live camera recognition will be connected here."
    )

    if st.button(
        "Start Attendance"
    ):

        st.warning(
            "Camera module will be connected "
            "in the next step."
        )

elif page == "Reports":

    st.title("📋 Attendance Reports")

    attendance = get_all_attendance()

    if attendance:

        import pandas as pd

        dataframe = pd.DataFrame(
            attendance,
            columns=[
                "Person ID",
                "Name",
                "Date",
                "Time",
                "Session ID"
            ]
        )

        st.dataframe(
            dataframe,
            use_container_width=True
        )

        csv = dataframe.to_csv(
            index=False
        )

        st.download_button(
            label="⬇️ Download CSV",
            data=csv,
            file_name="attendance.csv",
            mime="text/csv"
        )

    else:

        st.info(
            "No attendance records available."
        )