import cv2
import numpy as np
from PIL import Image
import os
import csv
import time
import threading
import itertools
import sys

def train_model():
    def loading_animation(msg):
        for c in itertools.cycle(['|', '/', '-', '\\']):
            if done:
                break
            sys.stdout.write(f'\r{msg} ' + c)
            sys.stdout.flush()
            time.sleep(0.1)
        sys.stdout.write('\r Model training complete!        \n')

    data_path = 'dataset'
    recognizer = cv2.face.LBPHFaceRecognizer_create()
    detector = cv2.CascadeClassifier("haarcascade_frontalface_default.xml")

    faces = []
    ids = []
    label_map = {}  # enrollment => numeric ID
    current_id = 0

    label_map_path = 'label_map.csv'
    if os.path.exists(label_map_path):
        with open(label_map_path, 'r') as f:
            reader = csv.reader(f)
            next(reader)
            for row in reader:
                label_map[row[0]] = int(row[1])
            current_id = max(label_map.values()) + 1

    print(" Scanning dataset folders...")
    for root, dirs, _ in os.walk(data_path):
        for folder in dirs:
            folder_path = os.path.join(root, folder)
            label = folder  # enrollment number

            if label not in label_map:
                label_map[label] = current_id
                current_id += 1

            numeric_id = label_map[label]

            for filename in os.listdir(folder_path):
                if filename.lower().endswith("jpg"):
                    img_path = os.path.join(folder_path, filename)
                    pil_img = Image.open(img_path).convert('L')
                    img_np = np.array(pil_img, 'uint8')
                    detected_faces = detector.detectMultiScale(img_np)

                    for (x, y, w, h) in detected_faces:
                        face = img_np[y:y + h, x:x + w]
                        faces.append(face)
                        ids.append(numeric_id)

    if not faces:
        print(" No faces found in dataset.")
        return

    # Start loading animation in background
    done = False
    t = threading.Thread(target=loading_animation, args=(" Training model",))
    t.start()

    os.makedirs("trainer", exist_ok=True)
    recognizer.train(faces, np.array(ids))
    recognizer.save("trainer/trainer.yml")
    done = True
    t.join()

    # Save label map
    with open(label_map_path, 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(["Enrollment", "ID"])
        for enroll, id_val in label_map.items():
            writer.writerow([enroll, id_val])

    print(" Label map saved to label_map.csv")

# Run script
if __name__ == "__main__":
    train_model()
