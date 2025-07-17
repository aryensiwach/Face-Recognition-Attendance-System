import tkinter as tk
from tkinter import messagebox, ttk
import cv2
import os
import csv
from admin_login import admin_login_page
from train_model import train_model
from mark_attendance import mark_attendance
from generate_subjectwise_attendance import daily_attendance_summary
import tkinter.simpledialog as simpledialog
import tkinter.messagebox as messagebox
import pandas as pd
from datetime import datetime
from export_attendance import export_monthly_attendance_report
from camera_selector import select_camera







# ----------- Root Window -----------
root = tk.Tk()
root.title("Face Attendance System")
root.geometry("800x490")
root.resizable(False, False)

# ----------- Frames -----------
main_frame = tk.Frame(root)
student_frame = tk.Frame(root)
register_frame = tk.Frame(root)
help_frame = tk.Frame(root)
admin_dashboard_frame = tk.Frame(root)
timetable_frame = tk.Frame(root)

for frame in (main_frame, student_frame, help_frame, admin_dashboard_frame, register_frame, timetable_frame):
    frame.place(x=0, y=0, width=800, height=500)


# ----------- Navigation Functions -----------


def generate_subject_attendance_ui():
    from datetime import datetime
    today = datetime.now().strftime("%Y-%m-%d")
    try:
        daily_attendance_summary(f"attendance_{today}.csv", "timetable.csv", "students.csv")
        messagebox.showinfo("Success", f"Attendance generated for {today}")
    except Exception as e:
        messagebox.showerror("Error", str(e))

def get_camera_source():
    try:
        with open("camera_config.txt", "r") as f:
            source = f.read().strip()
            if source.startswith("http"):
                return source
            else:
                return int(source)
    except:
        return 0

def show_frame(frame):
    frame.tkraise()

def show_admin_login():
    admin_login_page(root, show_main_menu, show_admin_dashboard)

def show_admin_dashboard():
    build_admin_dashboard()
    show_frame(admin_dashboard_frame)

def show_main_menu():
    show_frame(main_frame)

# ----------- Time Table -----------
def build_timetable():
    for widget in timetable_frame.winfo_children():
        widget.destroy()

    canvas = tk.Canvas(timetable_frame)
    scrollbar = tk.Scrollbar(timetable_frame, orient="vertical", command=canvas.yview)
    scroll_frame = tk.Frame(canvas)

    scroll_frame.bind(
        "<Configure>",
        lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
    )

    canvas.create_window((0, 0), window=scroll_frame, anchor="nw")
    canvas.configure(yscrollcommand=scrollbar.set)

    canvas.pack(side="left", fill="both", expand=True)
    scrollbar.pack(side="right", fill="y")

    # Title
    tk.Label(scroll_frame, text="🗓 Set Time Table", font=("Arial", 16, "bold")).pack(pady=10)

    # Vars
    day_var = tk.StringVar(value="Monday")
    start_var = tk.StringVar()
    end_var = tk.StringVar()
    subject_var = tk.StringVar()

    # Inputs
    tk.Label(scroll_frame, text="Day").pack()
    day_menu = ttk.Combobox(scroll_frame, textvariable=day_var, width=30, state="readonly")
    day_menu['values'] = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday"]
    day_menu.pack(pady=5)

    tk.Label(scroll_frame, text="Start Time (HH:MM)").pack()
    start_entry = tk.Entry(scroll_frame, textvariable=start_var, width=30)
    start_entry.pack(pady=5)

    tk.Label(scroll_frame, text="End Time (HH:MM)").pack()
    end_entry = tk.Entry(scroll_frame, textvariable=end_var, width=30)
    end_entry.pack(pady=5)

    tk.Label(scroll_frame, text="Subject Name").pack()
    subject_entry = tk.Entry(scroll_frame, textvariable=subject_var, width=30)
    subject_entry.pack(pady=5)

    # Table
    # Treeview with scrollbar
    tree_frame = tk.Frame(scroll_frame)
    tree_frame.pack(pady=10)

    tree_scroll = tk.Scrollbar(tree_frame)
    tree_scroll.pack(side="right", fill="y")

    tree = ttk.Treeview(tree_frame, columns=("Day", "Start", "End", "Subject"), show="headings", yscrollcommand=tree_scroll.set, height=10)
    tree.heading("Day", text="Day")
    tree.heading("Start", text="Start Time")
    tree.heading("End", text="End Time")
    tree.heading("Subject", text="Subject")
    tree.pack(side="left", fill="both")

    tree_scroll.config(command=tree.yview)

    


    # Load
    def load_data():
        tree.delete(*tree.get_children())
        if os.path.exists("timetable.csv"):
            with open("timetable.csv", 'r') as f:
                reader = csv.reader(f)
                next(reader, None)
                for row in reader:
                    tree.insert("", tk.END, values=row)

    # Add
    def add_entry():
        data = [day_var.get(), start_var.get(), end_var.get(), subject_var.get()]
        if any(not val for val in data):
            messagebox.showerror("Error", "Please fill all fields.")
            return
        file_exists = os.path.exists("timetable.csv")
        with open("timetable.csv", 'a', newline='') as f:
            writer = csv.writer(f)
            if not file_exists:
                writer.writerow(["Day", "Start Time", "End Time", "Subject"])
            writer.writerow(data)
        messagebox.showinfo("Success", "Entry added!")
        clear_fields()
        load_data()

    # Update
    def update_entry():
        selected = tree.focus()
        if not selected:
            messagebox.showerror("Error", "Select a row to update.")
            return
        new_data = [day_var.get(), start_var.get(), end_var.get(), subject_var.get()]
        updated_rows = []
        with open("timetable.csv", 'r') as f:
            reader = csv.reader(f)
            header = next(reader, None)
            for row in reader:
                if row == list(tree.item(selected, 'values')):
                    updated_rows.append(new_data)
                else:
                    updated_rows.append(row)
        with open("timetable.csv", 'w', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(["Day", "Start Time", "End Time", "Subject"])
            writer.writerows(updated_rows)
        messagebox.showinfo("Success", "Entry updated.")
        clear_fields()
        load_data()

    # Delete
    def delete_entry():
        selected = tree.focus()
        if not selected:
            messagebox.showerror("Error", "Select a row to delete.")
            return
        selected_values = list(tree.item(selected, 'values'))
        updated_rows = []
        with open("timetable.csv", 'r') as f:
            reader = csv.reader(f)
            header = next(reader, None)
            for row in reader:
                if row != selected_values:
                    updated_rows.append(row)
        with open("timetable.csv", 'w', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(["Day", "Start Time", "End Time", "Subject"])
            writer.writerows(updated_rows)
        messagebox.showinfo("Success", "Entry deleted.")
        clear_fields()
        load_data()

    # Clear
    def clear_fields():
        day_var.set("Monday")
        start_var.set("")
        end_var.set("")
        subject_var.set("")

    # Row select
    def on_row_select(event):
        selected = tree.focus()
        if not selected:
            return
        values = tree.item(selected, 'values')
        if values:
            day_var.set(values[0])
            start_var.set(values[1])
            end_var.set(values[2])
            subject_var.set(values[3])

    tree.bind("<<TreeviewSelect>>", on_row_select)

    # Buttons
    tk.Button(scroll_frame, text="➕ Add", command=add_entry, width=20).pack(pady=2)
    tk.Button(scroll_frame, text="🔄 Update", command=update_entry, width=20).pack(pady=2)
    tk.Button(scroll_frame, text="❌ Delete", command=delete_entry, width=20).pack(pady=2)
    tk.Button(scroll_frame, text="🧹 Clear Fields", command=clear_fields, width=20).pack(pady=2)
    tk.Button(scroll_frame, text="🔙 Back", command=show_admin_dashboard, width=20).pack(pady=10)

    load_data()
    show_frame(timetable_frame)



# ----------- Save Student -----------
def save_student_to_csv(name, enrollment, course):
    file_path = "students.csv"
    file_exists = os.path.isfile(file_path)
    student_id = 1
    if file_exists:
        with open(file_path, mode="r") as file:
            reader = csv.reader(file)
            next(reader, None)
            rows = [row for row in reader if row]
            if rows:
                try:
                    student_id = int(rows[-1][0]) + 1
                except ValueError:
                    student_id = len(rows) + 1
    with open(file_path, mode="a", newline='') as file:
        writer = csv.writer(file)
        if not file_exists:
            writer.writerow(["ID", "Name", "Enrollment", "Course"])
        writer.writerow([student_id, name, enrollment, course])
    return student_id

# ----------- Main Menu -----------
def build_main_menu():
    tk.Label(main_frame, text="Welcome to Face Attendance System", font=("Arial", 16, "bold")).pack(pady=30)
    tk.Button(main_frame, text="Admin", width=20, height=2, bg="blue", fg="white", command=show_admin_login).pack(pady=10)
    tk.Button(main_frame, text="Student", width=20, height=2, bg="green", fg="white", command=lambda: [build_student(), show_frame(student_frame)]).pack(pady=10)
    tk.Button(main_frame, text="Help", width=20, height=2, command=lambda: show_frame(help_frame)).pack(pady=10)

# ----------- Admin Dashboard -----------
def build_admin_dashboard():
    for widget in admin_dashboard_frame.winfo_children():
        widget.destroy()
    tk.Label(admin_dashboard_frame, text="Admin Dashboard", font=("Arial", 16, "bold")).pack(pady=20)
    tk.Button(admin_dashboard_frame, text="📷 Register Student", width=25, command=build_register_form).pack(pady=5)
    tk.Button(admin_dashboard_frame, text="🧠 Train Model", width=25, command=train_model).pack(pady=5)
    tk.Button(admin_dashboard_frame, text="✅ Mark Attendance", width=25, command=mark_attendance).pack(pady=5)
    tk.Button(admin_dashboard_frame, text="🗓 Set Time Table", width=25, command=build_timetable).pack(pady=5)
    tk.Button(admin_dashboard_frame, text=" Generate Subject Attendance", width=25, command=generate_subject_attendance_ui).pack(pady=5)
    tk.Button(admin_dashboard_frame, text="📁 Export Attendance", width=25, command=export_monthly_attendance_report).pack(pady=5)
    tk.Button(admin_dashboard_frame, text="🎥 Change Camera", width=25, command=select_camera).pack(pady=5)
    tk.Button(admin_dashboard_frame, text="🚪 Logout", bg="red", fg="white", width=15, command=show_main_menu).pack(pady=15)

# ----------- Register Student -----------
def build_register_form():
    for widget in register_frame.winfo_children():
        widget.destroy()
    tk.Label(register_frame, text="Register Student", font=("Arial", 16, "bold")).pack(pady=10)
    tk.Label(register_frame, text="Name").pack()
    name_entry = tk.Entry(register_frame, width=30)
    name_entry.pack(pady=5)
    tk.Label(register_frame, text="Enrollment No.").pack()
    enroll_entry = tk.Entry(register_frame, width=30)
    enroll_entry.pack(pady=5)
    tk.Label(register_frame, text="Course").pack()
    course_entry = tk.Entry(register_frame, width=30)
    course_entry.pack(pady=5)

    def capture_face():
        name = name_entry.get().strip()
        enroll = enroll_entry.get().strip()
        course = course_entry.get().strip()
        if not name or not enroll or not course:
            messagebox.showerror("Error", "Please fill all fields.")
            return
        student_id = save_student_to_csv(name, enroll, course)
        save_path = f"dataset/{enroll}"
        os.makedirs(save_path, exist_ok=True)
        face_cascade = cv2.CascadeClassifier("haarcascade_frontalface_default.xml")
        cap = cv2.VideoCapture(get_camera_source())

        count = 0
        while True:
            ret, frame = cap.read()
            if not ret:
                break
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            faces = face_cascade.detectMultiScale(gray, 1.3, 5)
            for (x, y, w, h) in faces:
                count += 1
                face_img = gray[y:y + h, x:x + w]
                cv2.imwrite(f"{save_path}/{count}.jpg", face_img)
                cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
            cv2.putText(frame, f"Capturing: {count}/100", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)
            cv2.imshow("Capturing Face", frame)
            if cv2.waitKey(1) == 27 or count >= 100:
                break
        cap.release()
        cv2.destroyAllWindows()
        messagebox.showinfo("Success", f"100 face images captured for {name}!")

    tk.Button(register_frame, text="📷 Capture Face", width=20, command=capture_face).pack(pady=15)
    tk.Button(register_frame, text="🔙 Go Back", width=15, command=show_admin_dashboard).pack(pady=10)
    show_frame(register_frame)

# ----------- Student Panel -----------
def show_attendance():
    enrollment = simpledialog.askstring("Enrollment", "Enter your Enrollment No.")
    if not enrollment:
        return

    today = datetime.now().strftime("%Y-%m-%d")
    filename = f"attendance_{today}.csv"

    if not os.path.exists(filename):
        messagebox.showerror("Error", f"No attendance file found for {today}")
        return

    df = pd.read_csv(filename)
    df = df[df["Enrollment"] == int(enrollment)]

    if df.empty:
        messagebox.showinfo("Info", "No attendance marked for this enrollment today.")
        return

    result_window = tk.Toplevel()
    result_window.title("Your Attendance")
    result_text = tk.Text(result_window, width=50, height=15)
    result_text.pack(padx=10, pady=10)

    result_text.insert(tk.END, f"Attendance for {enrollment}:\n\n")
    for index, row in df.iterrows():
        result_text.insert(tk.END, f"{row['Time']} | {row['Name']} | {row['Day']} | {row['Date']}\n")

    result_text.config(state=tk.DISABLED)

def build_student():
    for widget in student_frame.winfo_children():
        widget.destroy()
    
    
    tk.Label(student_frame, text="Student Panel", font=("Arial", 16, "bold")).pack(pady=20)
    tk.Button(student_frame, text="📈 Show Attendance", width=25, height=2, command=show_attendance).pack(pady=10)

    tk.Button(student_frame, text="🔙 Go Back", width=15, height=2, command=show_main_menu).pack(pady=20)

# ----------- Help Page -----------
def build_help():
    tk.Label(help_frame, text="Help / Info", font=("Arial", 16, "bold")).pack(pady=10)
    help_text = """
This software is for marking attendance using face recognition.

▶ Admin Login:
- Can train data, set timetable 
- View & export attendance

▶ Students:
- Can register face
- Check their attendance

Note: Face training is required before attendance.
"""
    tk.Label(help_frame, text=help_text, justify="left").pack(pady=10)
    tk.Button(help_frame, text="Go Back", command=show_main_menu).pack(pady=10)

# ----------- Initialize -----------
build_main_menu()
build_help()
show_frame(main_frame)
root.mainloop()
