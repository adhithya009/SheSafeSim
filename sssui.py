import tkinter as tk
from tkinter import messagebox, ttk
import webbrowser
from sssmain import User, Contact

# --- GLOBALS ---
users = []
current_user = None


# ---------- LOGIN PAGE ----------
class LoginPage(tk.Frame):
    def __init__(self, master, switch_page):
        super().__init__(master)
        self.switch_page = switch_page
        self.build_ui()

    def build_ui(self):
        tk.Label(self, text="🚨 SheSafeSim Emergency System 🚨", font=("Arial", 18, "bold"), fg="deep pink").pack(pady=20)

        tk.Label(self, text="Username:").pack()
        self.username_entry = tk.Entry(self)
        self.username_entry.pack(pady=5)

        tk.Label(self, text="User ID:").pack()
        self.userid_entry = tk.Entry(self)
        self.userid_entry.pack(pady=5)

        tk.Label(self, text="Password:").pack()
        self.password_entry = tk.Entry(self, show="*")
        self.password_entry.pack(pady=5)

        tk.Button(self, text="Login", bg="deep pink", fg="white", command=self.login).pack(pady=10)
        tk.Button(self, text="Create New Account", command=lambda: self.switch_page("register")).pack()

    def login(self):
        global current_user
        name = self.username_entry.get()
        uid = self.userid_entry.get()
        pwd = self.password_entry.get()

        for user in users:
            if user.get_name() == name and user.get_user_id() == uid and user.check_password(pwd):
                current_user = user
                messagebox.showinfo("Success", "Login successful!")
                self.switch_page("dashboard")
                return
        messagebox.showerror("Error", "Invalid credentials!")


# ---------- REGISTER PAGE ----------
class RegisterPage(tk.Frame):
    def __init__(self, master, switch_page):
        super().__init__(master)
        self.switch_page = switch_page
        self.build_ui()

    def build_ui(self):
        tk.Label(self, text="🧍 Register New User", font=("Arial", 16, "bold"), fg="blue violet").pack(pady=20)

        self.name_entry = tk.Entry(self)
        self.uid_entry = tk.Entry(self)
        self.pwd_entry = tk.Entry(self, show="*")

        for label, entry in [("Name:", self.name_entry), ("User ID:", self.uid_entry), ("Password:", self.pwd_entry)]:
            tk.Label(self, text=label).pack()
            entry.pack(pady=5)

        tk.Button(self, text="Register", bg="blue violet", fg="white", command=self.create_user).pack(pady=10)
        tk.Button(self, text="Back to Login", command=lambda: self.switch_page("login")).pack()

    def create_user(self):
        name = self.name_entry.get()
        uid = self.uid_entry.get()
        pwd = self.pwd_entry.get()

        if not name or not uid or not pwd:
            messagebox.showerror("Error", "All fields are required!")
            return

        user = User(name, uid)
        user.set_password(pwd)
        users.append(user)
        messagebox.showinfo("Success", f"Account created for {name}!")
        self.switch_page("login")


# ---------- DASHBOARD PAGE ----------
class DashboardPage(tk.Frame):
    def __init__(self, master, switch_page):
        super().__init__(master)
        self.switch_page = switch_page
        self.build_ui()

    def build_ui(self):
        tk.Label(self, text="👤 User Dashboard", font=("Arial", 16, "bold"), fg="green").pack(pady=10)
        tk.Button(self, text="Add Contact", width=20, command=self.add_contact_ui).pack(pady=5)
        tk.Button(self, text="View Contacts", width=20, command=self.view_contacts_ui).pack(pady=5)
        tk.Button(self, text="Update Location", width=20, command=self.update_location_ui).pack(pady=5)
        tk.Button(self, text="Send Panic Alert 🚨", bg="red", fg="white", width=20, command=self.trigger_alert).pack(pady=5)
        tk.Button(self, text="Open Map 📍", width=20, command=self.open_map).pack(pady=5)
        tk.Button(self, text="Logout", width=20, command=lambda: self.switch_page("login")).pack(pady=10)

    def add_contact_ui(self):
        global current_user
        popup = tk.Toplevel(self)
        popup.title("Add Contact")

        tk.Label(popup, text="Contact Name:").pack()
        name = tk.Entry(popup)
        name.pack(pady=5)

        tk.Label(popup, text="Contact Number:").pack()
        number = tk.Entry(popup)
        number.pack(pady=5)

        def save_contact():
            contact = Contact(name.get(), number.get())
            current_user.add_contact(contact)
            messagebox.showinfo("Added", "Contact saved successfully!")
            popup.destroy()

        tk.Button(popup, text="Save", bg="green", fg="white", command=save_contact).pack(pady=10)

    def view_contacts_ui(self):
        global current_user
        popup = tk.Toplevel(self)
        popup.title("Your Contacts")
        popup.geometry("300x300")
        tk.Label(popup, text="📇 Saved Contacts", font=("Arial", 12, "bold")).pack(pady=5)
        text_box = tk.Text(popup, wrap="word", height=12)
        text_box.pack(pady=10, padx=10)

        if not current_user._User__contacts:
            text_box.insert("end", "No contacts saved.")
        else:
            for c in current_user._User__contacts:
                text_box.insert("end", f"{c.get_name()} - {c.get_number()}\n")

    def update_location_ui(self):
        global current_user
        popup = tk.Toplevel(self)
        popup.title("Update Location")

        tk.Label(popup, text="Enter your current location:").pack(pady=5)
        loc_entry = tk.Entry(popup)
        loc_entry.pack(pady=5)

        def save_location():
            loc = loc_entry.get()
            current_user.update_location(loc)
            messagebox.showinfo("Updated", f"Location updated to {loc}")
            popup.destroy()

        tk.Button(popup, text="Save", bg="green", fg="white", command=save_location).pack(pady=10)

    def trigger_alert(self):
        global current_user
        if not current_user:
            messagebox.showerror("Error", "No user logged in!")
            return
        current_user.quick_panic_alert()
        messagebox.showinfo("Sent", "🚨 Panic alert sent to all contacts!")

    def open_map(self):
        # You can swap this with your own Google Maps API link or current_user location
        webbrowser.open("https://www.google.com/maps")


# ---------- MAIN WINDOW ----------
class MainApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("SheSafeSim Emergency System")
        self.geometry("400x500")
        self.resizable(False, False)
        self.current_frame = None
        self.switch_page("login")

    def switch_page(self, page_name):
        if self.current_frame:
            self.current_frame.destroy()

        if page_name == "login":
            self.current_frame = LoginPage(self, self.switch_page)
        elif page_name == "register":
            self.current_frame = RegisterPage(self, self.switch_page)
        elif page_name == "dashboard":
            self.current_frame = DashboardPage(self, self.switch_page)

        self.current_frame.pack(fill="both", expand=True)


if __name__ == "__main__":
    app = MainApp()
    app.mainloop()
