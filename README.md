# Face Recognition Attendance System
Run Main.py and enjoy,
The admin username and password are stored in credentials.txt

This is a Python-based facial recognition attendance system. It uses OpenCV and the face_recognition library to detect and recognize faces from a webcam feed and mark attendance automatically.

## ✅ Features
- Real-time face detection and recognition
- Marks attendance with name, date, and time
- Attendance stored in a CSV file (Attendance.csv)
- Add new faces by simply adding images
- Admin login system
- Simple and easy to use

## 🔧 How It Works
1. Add clear images in the `ImagesAttendance/` folder. Use filenames as the person's name (e.g., Aryendra.jpg).
2. Run the main script (`face_recog.py`)
3. Camera will open and recognize known faces
4. Automatically logs attendance in `Attendance.csv`

## 📁 Folder Structure
ATTENDANCE  
├── ImagesAttendance/ → Folder with known face images (filenames = names)  
├── Attendance.csv → Stores attendance logs  
├── face_recog.py → Main Python script  
├── credentials.txt → Admin login credentials  
├── requirements.txt → Required Python libraries  
└── readme.txt → You are here

## 🚀 Setup Instructions

### 1. Clone the Repository
If you're using Git:
git clone https://github.com/your-username/your-repo.git
cd your-repo


### 2. Install Dependencies
Make sure you have Python 3.6 or above installed.
Then install required packages:
pip install -r requirements.txt


### 3. Run the Project
## requirements.txt
This file contains all Python libraries used in the project.
You can create it by running this command:

## About Me
Project created by Aryendra Chaudhary  
GitHub: https://github.com/aryensiwach  


The camera change feature and student panel is under build ,will update when finished.
---




