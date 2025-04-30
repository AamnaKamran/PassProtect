import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
from db import *

create_tables()

class UserApp:
    def __init__(self, root):
        self.root = root
        self.root.title("PassProtect")
        self.root.geometry("600x400")
        self.root.resizable(False, False)
        self.current_user_id = None

        # === Left Frame ===
        self.left_frame = tk.Frame(self.root, width=200, height=400, bg="white")
        self.left_frame.pack(side="left", fill="both")

        logo_image = Image.open("padlock.png")
        logo_image = self.resize_logo(logo_image, 150)
        logo_photo = ImageTk.PhotoImage(logo_image)

        self.logo_label = tk.Label(self.left_frame, image=logo_photo, bg="white")
        self.logo_label.image = logo_photo
        self.logo_label.place(relx=0.5, rely=0.5, anchor="center")

        # === Right Frame ===
        self.right_frame = tk.Frame(self.root, width=400, height=400, bg="#ADD8E6")
        self.right_frame.pack(side="right", fill="both", expand=True)

        self.heading = tk.Label(self.right_frame, text="Login", font=("Helvetica", 20, "bold"), bg="#ADD8E6")
        self.heading.pack(pady=(50, 40))

        self.username_label = tk.Label(self.right_frame, text="Username:", bg="#ADD8E6")
        self.username_label.pack(pady=(5, 0))
        self.username_entry = tk.Entry(self.right_frame)
        self.username_entry.pack(pady=5)

        self.password_label = tk.Label(self.right_frame, text="Password:", bg="#ADD8E6")
        self.password_label.pack(pady=(10, 0))
        self.password_entry = tk.Entry(self.right_frame, show="*")
        self.password_entry.pack(pady=5)

        self.login_button = tk.Button(self.right_frame, text="Login", command=self.check_credentials,
                                      bg="maroon", fg="white", width=15)
        self.login_button.pack(pady=30)

    def resize_logo(self, image, target_height):
        width, height = image.size
        new_width = int((target_height / height) * width)
        return image.resize((new_width, target_height), Image.Resampling.LANCZOS)

    def check_credentials(self):
        username = self.username_entry.get()
        password = self.password_entry.get()

        if not username or not password:
            messagebox.showwarning("Input Error", "Please enter both username and password.")
            return

        user = user_exists(username)
        if user:
            stored_password = user[1]
            if password == stored_password:
                self.current_user_id = user[0]
                messagebox.showinfo("Login Success", f"Welcome back, {username}!")
                self.show_options_screen()
            else:
                messagebox.showerror("Login Failed", "Incorrect password.")
        else:
            create = messagebox.askyesno("User Not Found", "Username not found. Create a new account?")
            if create:
                self.create_account(username)
            else:
                messagebox.showinfo("Exit", "No account created.")

    def create_account(self, username):
        pw_window = tk.Toplevel(self.root)
        pw_window.title("Create Account")
        pw_window.geometry("300x200")
        pw_window.configure(bg="#ADD8E6")

        label = tk.Label(pw_window, text="Create a password:", bg="#ADD8E6")
        label.pack(pady=(20, 5))

        pw_entry = tk.Entry(pw_window, show='*')
        pw_entry.pack(pady=5)

        def submit():
            password = pw_entry.get()
            if not password:
                messagebox.showwarning("Input Error", "Password cannot be empty.")
                return
            user = User(username, password)
            insert_user(user)
            messagebox.showinfo("Success", "Account created!")
            pw_window.destroy()

        submit_btn = tk.Button(pw_window, text="Create", command=submit, bg="maroon", fg="white")
        submit_btn.pack(pady=15)

    def show_options_screen(self):
        for widget in self.root.winfo_children():
            widget.destroy()

        self.root.configure(bg="#ADD8E6")

        label = tk.Label(self.root, text="Welcome!", font=("Helvetica", 16, "bold"), bg="#ADD8E6")
        label.pack(pady=(60, 20))

        save_btn = tk.Button(self.root, text="Save New Password", width=20, bg="maroon", fg="white",
                             command=self.save_new_password)
        save_btn.pack(pady=10)

        view_btn = tk.Button(self.root, text="View All Passwords", width=20, bg="maroon", fg="white", command=self.view_all_passwords)
        view_btn.pack(pady=10)

    def save_new_password(self):
        if not self.current_user_id:
            messagebox.showerror("Error", "User not logged in.")
            return

        save_window = tk.Toplevel(self.root)
        save_window.title("Save New Password")
        save_window.geometry("350x300")
        save_window.configure(bg="#ADD8E6")

        tk.Label(save_window, text="App Name:", bg="#ADD8E6").pack(pady=5)
        app_name_entry = tk.Entry(save_window)
        app_name_entry.pack(pady=5)

        tk.Label(save_window, text="Username:", bg="#ADD8E6").pack(pady=5)
        username_entry = tk.Entry(save_window)
        username_entry.pack(pady=5)

        tk.Label(save_window, text="Email (optional):", bg="#ADD8E6").pack(pady=5)
        email_entry = tk.Entry(save_window)
        email_entry.pack(pady=5)

        tk.Label(save_window, text="Password:", bg="#ADD8E6").pack(pady=5)
        password_entry = tk.Entry(save_window, show="*")
        password_entry.pack(pady=5)

        def submit_credential():
            app_name = app_name_entry.get()
            uname = username_entry.get()
            email = email_entry.get()
            pwd = password_entry.get()

            if not all([app_name, uname, pwd]):
                messagebox.showwarning("Missing Info", "Please fill in all required fields.")
                return

            credential = Credential(app_name, uname, email, pwd)
            insert_credential(credential, self.current_user_id)
            messagebox.showinfo("Success", "Credential saved.")
            save_window.destroy()

        tk.Button(save_window, text="Save", width=8, command=submit_credential, bg="maroon", fg="white").pack(pady=20)


    def view_all_passwords(self):
        if not self.current_user_id:
            messagebox.showerror("Error", "User not logged in.")
            return

        creds = fetch_credentials_for_user(self.current_user_id)

        if not creds:
            messagebox.showinfo("No Data", "No credentials saved.")
            return

        view_window = tk.Toplevel(self.root)
        view_window.title("Saved Credentials")
        view_window.geometry("500x400")
        view_window.configure(bg="#ADD8E6")

        # Title label
        tk.Label(view_window, text="Your Passwords", font=("Helvetica", 14, "bold"), bg="#ADD8E6").pack(pady=10)

        # Scrollable canvas setup
        container = tk.Frame(view_window)
        container.pack(fill="both", expand=True)

        canvas = tk.Canvas(container, bg="#ADD8E6", highlightthickness=0)
        scrollbar = tk.Scrollbar(container, orient="vertical", command=canvas.yview)
        scroll_frame = tk.Frame(canvas, bg="#ADD8E6")

        scroll_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(
                scrollregion=canvas.bbox("all")
            )
        )

        canvas.create_window((0, 0), window=scroll_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)

        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        # Add credential entries
        for app_name, uname, email, pwd in creds:
            entry_frame = tk.Frame(scroll_frame, bg="white", bd=1, relief="solid", width=460, height=80)
            entry_frame.pack_propagate(False)  # Prevent resizing to fit content
            entry_frame.pack(fill="x", padx=10, pady=5)

            tk.Label(entry_frame, text=f"App: {app_name}", anchor="w", bg="white").pack(fill="x")
            tk.Label(entry_frame, text=f"Username: {uname}", anchor="w", bg="white").pack(fill="x")
            tk.Label(entry_frame, text=f"Email: {email}", anchor="w", bg="white").pack(fill="x")
            tk.Label(entry_frame, text=f"Password: {pwd}", anchor="w", bg="white").pack(fill="x")


# === Run the app ===
if __name__ == "__main__":
    root = tk.Tk()
    app = UserApp(root)
    root.mainloop()
