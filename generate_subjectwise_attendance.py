import pandas as pd
from datetime import datetime
import os

def daily_attendance_summary(attendance_file, timetable_file, students_file):
    if not os.path.exists(attendance_file):
        print(f" Attendance file '{attendance_file}' not found.")
        return
    if not os.path.exists(timetable_file):
        print(f" Timetable file '{timetable_file}' not found.")
        return
    if not os.path.exists(students_file):
        print(f" Students file '{students_file}' not found.")
        return

    attendance_df = pd.read_csv(attendance_file)
    timetable_df = pd.read_csv(timetable_file)
    students_df = pd.read_csv(students_file)

    attendance_df["Time"] = pd.to_datetime(attendance_df["Time"], format="%H:%M:%S").dt.time
    timetable_df["Start Time"] = pd.to_datetime(timetable_df["Start Time"], format="%H:%M").dt.time
    timetable_df["End Time"] = pd.to_datetime(timetable_df["End Time"], format="%H:%M").dt.time

    if "Date" not in attendance_df.columns:
        attendance_df["Date"] = attendance_df.iloc[:, -1]

    date_today = attendance_df["Date"].iloc[0]
    day_today = attendance_df["Day"].iloc[0].lower()
    subjects = timetable_df[timetable_df["Day"].str.lower() == day_today]["Subject"].unique()

    data = []

    for idx, student in students_df.iterrows():
        row = {
            "sr no.": idx + 1,
            "enrollment": student["Enrollment"],
            "name": student["Name"]
        }

        for subject in subjects:
            slots = timetable_df[
                (timetable_df["Subject"] == subject) &
                (timetable_df["Day"].str.lower() == day_today)
            ]

            total = len(slots)
            present = 0

            for _, slot in slots.iterrows():
                start, end = slot["Start Time"], slot["End Time"]
                filtered = attendance_df[
                    (attendance_df["Enrollment"] == student["Enrollment"]) &
                    (attendance_df["Time"].apply(lambda t: start <= t <= end))
                ]
                if not filtered.empty:
                    present += 1

            row[f"{subject} attendance"] = f"{present}/{total}" if total > 0 else "-"

        data.append(row)

    df_final = pd.DataFrame(data)

    # ✅ Folder name = Month (like "June")
    month_folder = datetime.strptime(date_today, "%Y-%m-%d").strftime("%B")
    if not os.path.exists(month_folder):
        os.makedirs(month_folder)

    # ✅ File name = dd-mm-yyyy.csv
    out_filename = datetime.strptime(date_today, "%Y-%m-%d").strftime("%d-%m-%Y") + ".csv"
    full_path = os.path.join(month_folder, out_filename)
    
    df_final.to_csv(full_path, index=False)
    print(f"Attendance saved in folder '{month_folder}' as: {out_filename}")

# ✅ Run
if __name__ == "__main__":
    daily_attendance_summary(
        attendance_file="attendance_2025-06-16.csv",
        timetable_file="timetable.csv",
        students_file="students.csv"
    )
