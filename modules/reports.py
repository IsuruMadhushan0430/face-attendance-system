import pandas as pd

from modules.database import get_all_attendance


def get_attendance_dataframe():

    records = get_all_attendance()

    columns = [
        "Person ID",
        "Name",
        "Date",
        "Time",
        "Session ID"
    ]

    dataframe = pd.DataFrame(
        records,
        columns=columns
    )

    return dataframe


def export_attendance_csv(
    filename="exports/attendance.csv"
):

    dataframe = get_attendance_dataframe()

    dataframe.to_csv(
        filename,
        index=False
    )

    return filename