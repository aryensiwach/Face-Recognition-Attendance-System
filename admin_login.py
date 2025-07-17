import tkinter as tk
from tkinter import messagebox

CREDENTIALS_FILE = "credentials.txt"

def load_credentials():
    creds = {}
    try:
        with open(CREDENTIALS_FILE, "r") as f:
            for line in f:
                if ':' in line:
                    username, password = line.strip().split(":", 1)
                    creds[username] = password
    except FileNotFoundError:
        open(CREDENTIALS_FILE, "w").close()
    return creds

def save_credentials(creds):
    with open(CREDENTIALS_FILE, "w") as f:
        for user, pwd in creds.items():
            f.write(f"{user}:{pwd}\n")

def admin_login_page(root, go_back_callback, success_callback):
    
    credentials = load_credentials()

    root.configure(bg="#f0f0f0")
    login_frame = tk.Frame(root, bg="#ffffff", bd=2, relief="groove")
    login_frame.place(relx=0.5, rely=0.5, anchor="center", width=450, height=450)

    def check_login():
        username = username_entry.get()
        password = password_entry.get()

        if username in credentials and credentials[username] == password:
            messagebox.showinfo("Success", "Login Successful")
            login_frame.destroy()
            success_callback()
        else:
            messagebox.showerror("Error", "Invalid credentials")

    def forgot_password():
        def validate_username():
            uname = reset_username.get()
            if uname in credentials:
                username_frame.destroy()
                show_reset_form(uname)
            else:
                messagebox.showerror("Error", "Username not found")

        def show_reset_form(username):
            tk.Label(forgot_win, text=f"Reset password for '{username}'", font=("Arial", 10)).pack(pady=5)
            tk.Label(forgot_win, text="New Password:").pack()
            new_pass_entry = tk.Entry(forgot_win, show="*")
            new_pass_entry.pack(pady=5)

            tk.Label(forgot_win, text="Confirm Password:").pack()
            confirm_pass_entry = tk.Entry(forgot_win, show="*")
            confirm_pass_entry.pack(pady=5)

            def update_password():
                new_pass = new_pass_entry.get()
                confirm_pass = confirm_pass_entry.get()

                if new_pass != confirm_pass:
                    messagebox.showerror("Error", "Passwords do not match")
                elif len(new_pass) < 3:
                    messagebox.showerror("Error", "Password too short")
                else:
                    credentials[username] = new_pass
                    save_credentials(credentials)
                    messagebox.showinfo("Success", "Password successfully updated")
                    forgot_win.destroy()

            tk.Button(forgot_win, text="Update Password", bg="#4CAF50", fg="white", command=update_password).pack(pady=10)

        forgot_win = tk.Toplevel(root)
        forgot_win.title("Forgot Password")
        forgot_win.geometry("300x200")

        username_frame = tk.Frame(forgot_win)
        username_frame.pack(pady=10)

        tk.Label(username_frame, text="Enter your username:").pack()
        reset_username = tk.Entry(username_frame)
        reset_username.pack(pady=5)
        tk.Button(username_frame, text="Submit", bg="#2196F3", fg="white", command=validate_username).pack()

    # ----- Styled UI -----
    tk.Label(login_frame, text="🔐 Admin Login", font=("Helvetica", 20, "bold"), bg="white", fg="#333").pack(pady=20)

    tk.Label(login_frame, text="Username", bg="white", anchor="w").pack(fill="x", padx=40)
    username_entry = tk.Entry(login_frame, bd=2, relief="groove", font=("Arial", 12))
    username_entry.pack(padx=40, pady=5, fill="x")

    tk.Label(login_frame, text="Password", bg="white", anchor="w").pack(fill="x", padx=40, pady=(10, 0))
    password_entry = tk.Entry(login_frame, show="*", bd=2, relief="groove", font=("Arial", 12))
    password_entry.pack(padx=40, pady=5, fill="x")

    tk.Button(login_frame, text="Login", bg="#4CAF50", fg="white", font=("Arial", 12), command=check_login).pack(pady=15)

    tk.Button(login_frame, text="Forgot Password?", bg="#FFC107", fg="black", command=forgot_password).pack(pady=5)
    tk.Button(login_frame, text="⬅ Back", bg="#f44336", fg="white", command=lambda: [login_frame.destroy(), go_back_callback()]).pack(pady=10)
