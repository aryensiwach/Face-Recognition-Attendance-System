import cv2
import numpy as np
import pandas as pd
import csv

# Load Haar Cascade and trained model
face_cascade = cv2.CascadeClassifier("haarcascade_frontalface_default.xml")
recognizer = cv2.face.LBPHFaceRecognizer_create()
recognizer.read("trainer/trainer.yml")

# Load label map (Enrollment => ID)
label_map = {}
with open("label_map.csv", 'r') as f:
    reader = csv.reader(f)
    next(reader)
    for row in reader:
        label_map[int(row[1])] = row[0]  # ID -> Enrollment

# Load student info
students_df = pd.read_csv("students.csv")

cap = cv2.VideoCapture(0)

while True:
    ret, frame = cap.read()
    if not ret:
        break

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray, scaleFactor=1.2, minNeighbors=5)

    for (x, y, w, h) in faces:
        roi_gray = gray[y:y+h, x:x+w]
        id_, confidence = recognizer.predict(roi_gray)

        if confidence < 70:
            enroll = label_map.get(id_, None)
            if enroll:
                row = students_df[students_df['Enrollment'] == int(enroll)]
                if not row.empty:
                    name = row.iloc[0]['Name']
                    label = f"{name} | {enroll} | {100 - int(confidence)}% matched"
                else:
                    label = f"{enroll} | {100 - int(confidence)}% matched"
            else:
                label = f"Unknown ({int(confidence)}%)"
        else:
            label = f"Unknown ({int(confidence)}%)"

        cv2.rectangle(frame, (x, y), (x+w, y+h), (0,255,0), 2)
        cv2.putText(frame, label, (x, y-10), cv2.FONT_HERSHEY_SIMPLEX,
                    0.7, (0,255,0), 2)

    cv2.imshow("Model Test - Face Detection", frame)

    if cv2.waitKey(1) == 27:  # ESC
        break

cap.release()
cv2.destroyAllWindows()
