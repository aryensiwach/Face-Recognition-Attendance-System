import os
import csv
from collections import defaultdict
from tkinter import filedialog, messagebox
import pandas as pd
import datetime

def export_monthly_attendance_report():
    try:
        month_folder = filedialog.askdirectory(title="Select Month Folder")
        if not month_folder:
            return

        student_subject_attendance = defaultdict(lambda: defaultdict(lambda: [0, 0]))  # enrollment -> subject -> [present, total]
        student_info = {}  # enrollment -> name

        for file in sorted(os.listdir(month_folder)):
            if not file.endswith(".csv"):
                continue
            file_path = os.path.join(month_folder, file)

            with open(file_path, 'r', encoding='utf-8') as f:
                reader = csv.DictReader(f)
                if reader.fieldnames is None:
                    continue

                subject_columns = [col for col in reader.fieldnames if 'attendance' in col.lower()]

                for row in reader:
                    enrollment = row.get("enrollment") or row.get(" Enrollment") or row.get("Enroll")
                    name = row.get("name") or row.get(" Name")
                    if not enrollment:
                        continue
                    student_info[enrollment] = name

                    for subject in subject_columns:
                        val = row.get(subject, "0/0").strip()
                        if "/" in val:
                            try:
                                present, total = map(int, val.split("/"))
                            except:
                                present, total = 0, 0
                        else:
                            present, total = 0, 0

                        student_subject_attendance[enrollment][subject][0] += present
                        student_subject_attendance[enrollment][subject][1] += total

        # Build final report
        output_rows = []
        all_subjects = set()
        for sub_data in student_subject_attendance.values():
            all_subjects.update(sub_data.keys())
        all_subjects = sorted(all_subjects)

        for i, enrollment in enumerate(student_subject_attendance.keys(), start=1):
            row = {
                "sr no.": i,
                "enrollment": enrollment,
                "name": student_info.get(enrollment, "")
            }

            total_present = 0
            total_lectures = 0

            for subject in all_subjects:
                present, total = student_subject_attendance[enrollment][subject]
                row[subject] = f"{present}/{total}"
                total_present += present
                total_lectures += total

            row["Total"] = f"{total_present}/{total_lectures}"
            row["Percentage"] = f"{(total_present / total_lectures * 100):.2f}%" if total_lectures > 0 else "0.00%"
            output_rows.append(row)

        if not output_rows:
            messagebox.showinfo("No Data", "No attendance data found.")
            return

        df = pd.DataFrame(output_rows)
        output_file = os.path.join(month_folder, f"Monthly_Report_{datetime.datetime.now().strftime('%d-%m-%Y_%H-%M')}.xlsx")
        df.to_excel(output_file, index=False)
        messagebox.showinfo("Success", f"Attendance exported to:\n{output_file}")

    except Exception as e:
        messagebox.showerror("Error", f"Something went wrong!\n{str(e)}")
