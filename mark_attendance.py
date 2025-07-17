import cv2
import numpy as np
import pandas as pd
import csv
import os
from datetime import datetime
import time
from camera_selector import get_camera_source




def mark_attendance():
    face_cascade = cv2.CascadeClassifier("haarcascade_frontalface_default.xml")
    recognizer = cv2.face.LBPHFaceRecognizer_create()

    # Check if model file exists
    if not os.path.exists("trainer/trainer.yml"):
        print("trainer.yml file not found. Please train the model first.")
        return

    recognizer.read("trainer/trainer.yml")

    # Load label_map.csv safely
    label_map = {}
    if not os.path.exists("label_map.csv"):
        print(" label_map.csv file not found. Please train the model first.")
        return
    else:
        with open("label_map.csv", 'r') as f:
            reader = csv.reader(f)
            next(reader)
            for row in reader:
                label_map[int(row[1])] = row[0]  # ID -> Enrollment

    # Load student info
    if not os.path.exists("students.csv"):
        print(" students.csv not found.")
        return
    students_df = pd.read_csv("students.csv")

    today = datetime.now().strftime("%Y-%m-%d")
    filename = f"attendance_{today}.csv"

    cap = cv2.VideoCapture(get_camera_source())

    attendance_done = False
    marked_time = None

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = face_cascade.detectMultiScale(gray, 1.2, 5)

        for (x, y, w, h) in faces:
            roi_gray = gray[y:y + h, x:x + w]
            id_, confidence = recognizer.predict(roi_gray)

            if confidence < 70:
                enroll = label_map.get(id_, None)
                if enroll:
                    row = students_df[students_df['Enrollment'] == int(enroll)]
                    if not row.empty:
                        name = row.iloc[0]['Name']
                        allow_mark = True
                        current_time = datetime.now()

                        # ✅ Check last marked time if already marked today
                        if os.path.exists(filename):
                            df = pd.read_csv(filename)
                            df = df[df["Enrollment"] == int(enroll)]
                            if not df.empty:
                                last_time_str = df.iloc[-1]["Time"]
                                last_time = datetime.strptime(last_time_str, "%H:%M:%S")
                                last_time = current_time.replace(hour=last_time.hour, minute=last_time.minute, second=last_time.second)
                                time_diff = (current_time - last_time).total_seconds()
                                if time_diff < 100:
                                    allow_mark = False  # ❌ Less than 1 hour

                        if allow_mark:
                            with open(filename, 'a', newline='') as f:
                                writer = csv.writer(f)
                                time_str = current_time.strftime("%H:%M:%S")
                                day_str = current_time.strftime("%A")

                                if not os.path.exists(filename) or os.stat(filename).st_size == 0:
                                    writer.writerow(["Time", "Enrollment", "Name", "Day","Date"])

                                writer.writerow([time_str, enroll, name, day_str,today])
                            attendance_done = True
                            marked_time = time.time()
                            label = f"Marked: {name} | {enroll}"
                        else:
                            label = f"Already marked"
                    else:
                        label = "Unknown"
                else:
                    label = "Unknown"
            else:
                label = "Unknown Face"

            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
            cv2.putText(frame, label, (x, y - 10),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)

        cv2.imshow("📸 Marking Attendance", frame)

        # Close window after 2.5 sec of success
        if attendance_done and (time.time() - marked_time > 2.5):
            break

        if cv2.waitKey(1) == 27:  # ESC to quit
            break

    cap.release()
    cv2.destroyAllWindows()
