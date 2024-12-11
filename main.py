
'''
import tkinter as tk
from tkinter import ttk, messagebox
import csv
import os

# File paths for CSV data
BOOKS_FILE = "books.csv"
MEMBERS_FILE = "members.csv"
TRANSACTIONS_FILE = "transactions.csv"
USERS_FILE = "users.csv"

# Initialize data files if not present
def initialize_files():
    for file, headers in [
        (BOOKS_FILE, ["Book ID", "Title", "Author", "Available"]),
        (MEMBERS_FILE, ["Member ID", "Name", "Phone"]),
        (TRANSACTIONS_FILE, ["Transaction ID", "Book ID", "Member ID", "Date", "Type"]),
        (USERS_FILE, ["Username", "Password", "Role"]),
    ]:
        if not os.path.exists(file):
            with open(file, mode="w", newline="") as f:
                writer = csv.writer(f)
                writer.writerow(headers)

# GUI Application class
class LibraryApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Library Management System")
        self.show_login_screen()

    def show_login_screen(self):
        self.clear_screen()

        ttk.Label(self.root, text="Login", font=("Arial", 18)).pack(pady=20)

        form_frame = ttk.Frame(self.root)
        form_frame.pack(pady=20)

        ttk.Label(form_frame, text="Username:").grid(row=0, column=0, padx=5, pady=5)
        self.username_entry = ttk.Entry(form_frame)
        self.username_entry.grid(row=0, column=1, padx=5, pady=5)

        ttk.Label(form_frame, text="Password:").grid(row=1, column=0, padx=5, pady=5)
        self.password_entry = ttk.Entry(form_frame, show="*")
        self.password_entry.grid(row=1, column=1, padx=5, pady=5)

        ttk.Button(form_frame, text="Login", command=self.handle_login).grid(row=2, column=0, pady=10)
        ttk.Button(form_frame, text="Register", command=self.show_register_screen).grid(row=2, column=1, pady=10)

    def handle_login(self):
        username = self.username_entry.get()
        password = self.password_entry.get()

        if not username or not password:
            messagebox.showerror("Error", "Both fields are required")
            return

        with open(USERS_FILE, mode="r") as f:
            reader = csv.DictReader(f)
            for row in reader:
                if row["Username"] == username and row["Password"] == password:
                    if row["Role"] == "Admin":
                        self.show_admin_homepage()
                    elif row["Role"] == "User":
                        self.show_user_homepage()
                    return

        messagebox.showerror("Error", "Invalid credentials")

    def show_register_screen(self):
        self.clear_screen()

        ttk.Label(self.root, text="Register", font=("Arial", 18)).pack(pady=20)

        form_frame = ttk.Frame(self.root)
        form_frame.pack(pady=20)

        ttk.Label(form_frame, text="Username:").grid(row=0, column=0, padx=5, pady=5)
        self.reg_username_entry = ttk.Entry(form_frame)
        self.reg_username_entry.grid(row=0, column=1, padx=5, pady=5)

        ttk.Label(form_frame, text="Password:").grid(row=1, column=0, padx=5, pady=5)
        self.reg_password_entry = ttk.Entry(form_frame, show="*")
        self.reg_password_entry.grid(row=1, column=1, padx=5, pady=5)

        ttk.Label(form_frame, text="Role:").grid(row=2, column=0, padx=5, pady=5)
        self.reg_role_combo = ttk.Combobox(form_frame, values=["Admin", "User"], state="readonly")
        self.reg_role_combo.grid(row=2, column=1, padx=5, pady=5)

        ttk.Button(form_frame, text="Register", command=self.handle_register).grid(row=3, columnspan=2, pady=10)
        ttk.Button(form_frame, text="Back", command=self.show_login_screen).grid(row=4, columnspan=2, pady=10)

    def handle_register(self):
        username = self.reg_username_entry.get()
        password = self.reg_password_entry.get()
        role = self.reg_role_combo.get()

        if not username or not password or not role:
            messagebox.showerror("Error", "All fields are required")
            return

        with open(USERS_FILE, mode="r") as f:
            reader = csv.DictReader(f)
            for row in reader:
                if row["Username"] == username:
                    messagebox.showerror("Error", "Username already exists")
                    return

        with open(USERS_FILE, mode="a", newline="") as f:
            writer = csv.writer(f)
            writer.writerow([username, password, role])

        messagebox.showinfo("Success", "Registration successful")
        self.show_login_screen()

    def show_admin_homepage(self):
        self.clear_screen()
        ttk.Label(self.root, text="Admin Homepage", font=("Arial", 18)).pack(pady=20)
        ttk.Button(self.root, text="Manage Books", command=self.show_books_tab).pack(pady=10)
        ttk.Button(self.root, text="Manage Members", command=self.show_members_tab).pack(pady=10)
        ttk.Button(self.root, text="Logout", command=self.show_login_screen).pack(pady=10)

    def show_user_homepage(self):
        self.clear_screen()
        ttk.Label(self.root, text="User Homepage", font=("Arial", 18)).pack(pady=20)
        ttk.Button(self.root, text="View Books", command=self.show_books_tab).pack(pady=10)
        ttk.Button(self.root, text="Logout", command=self.show_login_screen).pack(pady=10)

    def show_books_tab(self):
        self.clear_screen()
        ttk.Label(self.root, text="Books", font=("Arial", 18)).pack(pady=20)
        # Book list
        self.book_tree = ttk.Treeview(self.root, columns=("Book ID", "Title", "Author", "Available"), show="headings")
        for col in ["Book ID", "Title", "Author", "Available"]:
            self.book_tree.heading(col, text=col)
            self.book_tree.column(col, width=100)
        self.book_tree.pack(fill="both", expand=True, pady=10)
        self.load_books()
        ttk.Button(self.root, text="Back", command=self.show_admin_homepage if self.is_admin() else self.show_user_homepage).pack(pady=10)

    def show_members_tab(self):
        self.clear_screen()
        ttk.Label(self.root, text="Members", font=("Arial", 18)).pack(pady=20)
        # Member list
        self.member_tree = ttk.Treeview(self.root, columns=("Member ID", "Name", "Phone"), show="headings")
        for col in ["Member ID", "Name", "Phone"]:
            self.member_tree.heading(col, text=col)
            self.member_tree.column(col, width=100)
        self.member_tree.pack(fill="both", expand=True, pady=10)
        self.load_members()
        ttk.Button(self.root, text="Back", command=self.show_admin_homepage).pack(pady=10)

    def clear_screen(self):
        for widget in self.root.winfo_children():
            widget.destroy()

    def load_books(self):
        self.book_tree.delete(*self.book_tree.get_children())
        with open(BOOKS_FILE, mode="r") as f:
            reader = csv.DictReader(f)
            for row in reader:
                self.book_tree.insert("", "end", values=(row["Book ID"], row["Title"], row["Author"], row["Available"]))

    def load_members(self):
        self.member_tree.delete(*self.member_tree.get_children())
        with open(MEMBERS_FILE, mode="r") as f:
            reader = csv.DictReader(f)
            for row in reader:
                self.member_tree.insert("", "end", values=(row["Member ID"], row["Name"], row["Phone"]))

    def is_admin(self):
        return hasattr(self, "current_role") and self.current_role == "Admin"

# Initialize files and add sample user data
initialize_files()
if os.stat(USERS_FILE).st_size == 0:  # Add sample users if the file is empty
    with open(USERS_FILE, mode="a", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["admin", "admin123", "Admin"])
        writer.writerow(["user", "user123", "User"])

# Run the application
root = tk.Tk()
app = LibraryApp(root)
root.mainloop()
'''







'''


import tkinter as tk
from tkinter import ttk, messagebox
from tkcalendar import DateEntry
import csv
import os

# File paths for CSV data
BOOKS_FILE = "books.csv"
MEMBERS_FILE = "members.csv"
TRANSACTIONS_FILE = "transactions.csv"
USERS_FILE = "users.csv"

# Initialize data files if not present
def initialize_files():
    for file, headers in [
        (BOOKS_FILE, ["Book ID", "Title", "Author", "Available"]),
        (MEMBERS_FILE, ["Member ID", "First Name", "Last Name", "Contact Name", "Contact Address", "Aadhaar Card No", "Start Date", "End Date", "Membership Duration"]),
        (TRANSACTIONS_FILE, ["Transaction ID", "Book ID", "Member ID", "Date", "Type"]),
        (USERS_FILE, ["Username", "Password", "Role"]),
    ]:
        if not os.path.exists(file):
            with open(file, mode="w", newline="") as f:
                writer = csv.writer(f)
                writer.writerow(headers)

# GUI Application class
class LibraryApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Library Management System")
        self.current_role = None
        self.show_login_screen()

    def show_login_screen(self):
        self.clear_screen()

        ttk.Label(self.root, text="Login", font=("Arial", 18)).pack(pady=20)

        form_frame = ttk.Frame(self.root)
        form_frame.pack(pady=20)

        ttk.Label(form_frame, text="Username:").grid(row=0, column=0, padx=5, pady=5)
        self.username_entry = ttk.Entry(form_frame)
        self.username_entry.grid(row=0, column=1, padx=5, pady=5)

        ttk.Label(form_frame, text="Password:").grid(row=1, column=0, padx=5, pady=5)
        self.password_entry = ttk.Entry(form_frame, show="*")
        self.password_entry.grid(row=1, column=1, padx=5, pady=5)

        ttk.Button(form_frame, text="Login", command=self.handle_login).grid(row=2, column=0, pady=10)
        ttk.Button(form_frame, text="Register", command=self.show_register_screen).grid(row=2, column=1, pady=10)

    def handle_login(self):
        username = self.username_entry.get()
        password = self.password_entry.get()

        if not username or not password:
            messagebox.showerror("Error", "Both fields are required")
            return

        with open(USERS_FILE, mode="r") as f:
            reader = csv.DictReader(f)
            for row in reader:
                if row["Username"] == username and row["Password"] == password:
                    self.current_role = row["Role"]
                    if self.current_role == "Admin":
                        self.show_admin_homepage()
                    elif self.current_role == "User":
                        self.show_user_homepage()
                    return

        messagebox.showerror("Error", "Invalid credentials")

    def show_register_screen(self):
        self.clear_screen()

        ttk.Label(self.root, text="Register", font=("Arial", 18)).pack(pady=20)

        form_frame = ttk.Frame(self.root)
        form_frame.pack(pady=20)

        ttk.Label(form_frame, text="Username:").grid(row=0, column=0, padx=5, pady=5)
        self.reg_username_entry = ttk.Entry(form_frame)
        self.reg_username_entry.grid(row=0, column=1, padx=5, pady=5)

        ttk.Label(form_frame, text="Password:").grid(row=1, column=0, padx=5, pady=5)
        self.reg_password_entry = ttk.Entry(form_frame, show="*")
        self.reg_password_entry.grid(row=1, column=1, padx=5, pady=5)

        ttk.Label(form_frame, text="Role:").grid(row=2, column=0, padx=5, pady=5)
        self.reg_role_combo = ttk.Combobox(form_frame, values=["Admin", "User"], state="readonly")
        self.reg_role_combo.grid(row=2, column=1, padx=5, pady=5)

        ttk.Button(form_frame, text="Register", command=self.handle_register).grid(row=3, columnspan=2, pady=10)
        ttk.Button(form_frame, text="Back", command=self.show_login_screen).grid(row=4, columnspan=2, pady=10)

    def handle_register(self):
        username = self.reg_username_entry.get()
        password = self.reg_password_entry.get()
        role = self.reg_role_combo.get()

        if not username or not password or not role:
            messagebox.showerror("Error", "All fields are required")
            return

        with open(USERS_FILE, mode="r") as f:
            reader = csv.DictReader(f)
            for row in reader:
                if row["Username"] == username:
                    messagebox.showerror("Error", "Username already exists")
                    return

        with open(USERS_FILE, mode="a", newline="") as f:
            writer = csv.writer(f)
            writer.writerow([username, password, role])

        messagebox.showinfo("Success", "Registration successful")
        self.show_login_screen()

    def show_admin_homepage(self):
        self.clear_screen()
        ttk.Label(self.root, text="Admin Homepage", font=("Arial", 18)).pack(pady=20)
        ttk.Button(self.root, text="Maintenance Menu", command=self.show_maintenance_menu).pack(pady=10)
        ttk.Button(self.root, text="Report Menu", command=self.show_report_menu).pack(pady=10)
        ttk.Button(self.root, text="Transaction Menu", command=self.show_transaction_menu).pack(pady=10)
        ttk.Button(self.root, text="Logout", command=self.show_login_screen).pack(pady=10)

    def show_user_homepage(self):
        self.clear_screen()
        ttk.Label(self.root, text="User Homepage", font=("Arial", 18)).pack(pady=20)
        ttk.Button(self.root, text="Report Menu", command=self.show_report_menu).pack(pady=10)
        ttk.Button(self.root, text="Transaction Menu", command=self.show_transaction_menu).pack(pady=10)
        ttk.Button(self.root, text="Logout", command=self.show_login_screen).pack(pady=10)

    def show_maintenance_menu(self):
        self.clear_screen()
        ttk.Label(self.root, text="Maintenance Menu", font=("Arial", 18)).pack(pady=20)
        ttk.Button(self.root, text="Membership Add", command=self.show_add_membership).pack(pady=10)
        ttk.Button(self.root, text="Membership Update", command=self.show_update_membership).pack(pady=10)
        ttk.Button(self.root, text="Books/Movies Add", command=self.show_add_books).pack(pady=10)
        ttk.Button(self.root, text="Books/Movies Update", command=self.show_update_books).pack(pady=10)
        ttk.Button(self.root, text="User Management Add", command=self.show_add_user).pack(pady=10)
        ttk.Button(self.root, text="User Management Update", command=self.show_update_user).pack(pady=10)
        ttk.Button(self.root, text="Log Out", command=self.show_login_screen).pack(pady=10)

    def show_report_menu(self):
        messagebox.showinfo("Info", "Report Menu is under development.")

    def show_transaction_menu(self):
        messagebox.showinfo("Info", "Transaction Menu is under development.")

    def show_add_membership(self):
        self.clear_screen()
        ttk.Label(self.root, text="Add Membership", font=("Arial", 18)).pack(pady=20)

        form_frame = ttk.Frame(self.root)
        form_frame.pack(pady=10)

        ttk.Label(form_frame, text="First Name:").grid(row=0, column=0, padx=5, pady=5)
        first_name_entry = ttk.Entry(form_frame)
        first_name_entry.grid(row=0, column=1, padx=5, pady=5)

        ttk.Label(form_frame, text="Last Name:").grid(row=1, column=0, padx=5, pady=5)
        last_name_entry = ttk.Entry(form_frame)
        last_name_entry.grid(row=1, column=1, padx=5, pady=5)

        ttk.Label(form_frame, text="Contact Name:").grid(row=2, column=0, padx=5, pady=5)
        contact_name_entry = ttk.Entry(form_frame)
        contact_name_entry.grid(row=2, column=1, padx=5, pady=5)

        ttk.Label(form_frame, text="Contact Address:").grid(row=3, column=0, padx=5, pady=5)
        contact_address_entry = ttk.Entry(form_frame)
        contact_address_entry.grid(row=3, column=1, padx=5, pady=5)

        ttk.Label(form_frame, text="Aadhaar Card No:").grid(row=4, column=0, padx=5, pady=5)
        aadhaar_entry = ttk.Entry(form_frame)
        aadhaar_entry.grid(row=4, column=1, padx=5, pady=5)

        ttk.Label(form_frame, text="Start Date:").grid(row=5, column=0, padx=5, pady=5)
        start_date_entry = DateEntry(form_frame, date_pattern='y-mm-dd')
        start_date_entry.grid(row=5, column=1, padx=5, pady=5)

        ttk.Label(form_frame, text="End Date:").grid(row=6, column=0, padx=5, pady=5)
        end_date_entry = DateEntry(form_frame, date_pattern='y-mm-dd')
        end_date_entry.grid(row=6, column=1, padx=5, pady=5)

        ttk.Label(form_frame, text="Membership Duration:").grid(row=7, column=0, padx=5, pady=5)
        membership_var = tk.StringVar()
        ttk.Radiobutton(form_frame, text="Six Months", variable=membership_var, value="6 Months").grid(row=7, column=1, padx=5, pady=5, sticky="w")
        ttk.Radiobutton(form_frame, text="One Year", variable=membership_var, value="1 Year").grid(row=8, column=1, padx=5, pady=5, sticky="w")
        ttk.Radiobutton(form_frame, text="Two Years", variable=membership_var, value="2 Years").grid(row=9, column=1, padx=5, pady=5, sticky="w")

        def confirm_membership():
            first_name = first_name_entry.get()
            last_name = last_name_entry.get()
            contact_name = contact_name_entry.get()
            contact_address = contact_address_entry.get()
            aadhaar = aadhaar_entry.get()
            start_date = start_date_entry.get()
            end_date = end_date_entry.get()
            membership_duration = membership_var.get()

            if not all([first_name, last_name, contact_name, contact_address, aadhaar, start_date, end_date, membership_duration]):
                messagebox.showerror("Error", "All fields are required")
                return

            with open(MEMBERS_FILE, mode="a", newline="") as f:
                writer = csv.writer(f)
                writer.writerow(["M" + str(sum(1 for _ in open(MEMBERS_FILE)) + 1), first_name, last_name, contact_name, contact_address, aadhaar, start_date, end_date, membership_duration])

            messagebox.showinfo("Success", "Membership added successfully")
            self.show_maintenance_menu()

        ttk.Button(form_frame, text="Confirm", command=confirm_membership).grid(row=10, column=0, pady=10)
        ttk.Button(form_frame, text="Cancel", command=self.show_maintenance_menu).grid(row=10, column=1, pady=10)

    def show_update_membership(self):
        messagebox.showinfo("Info", "Update Membership is under development.")

    def show_add_books(self):
        messagebox.showinfo("Info", "Add Books/Movies is under development.")

    def show_update_books(self):
        messagebox.showinfo("Info", "Update Books/Movies is under development.")

    def show_add_user(self):
        messagebox.showinfo("Info", "Add User is under development.")

    def show_update_user(self):
        messagebox.showinfo("Info", "Update User is under development.")

    def clear_screen(self):
        for widget in self.root.winfo_children():
            widget.destroy()

# Initialize files and add sample user data
initialize_files()
if os.stat(USERS_FILE).st_size == 0:  # Add sample users if the file is empty
    with open(USERS_FILE, mode="a", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["admin", "admin123", "Admin"])
        writer.writerow(["user", "user123", "User"])

# Run the application
root = tk.Tk()
app = LibraryApp(root)
root.mainloop()




'''






import tkinter as tk
from tkinter import ttk, messagebox
from tkcalendar import DateEntry
import csv
import os

# File paths for CSV data
BOOKS_FILE = "books.csv"
MEMBERS_FILE = "members.csv"
TRANSACTIONS_FILE = "transactions.csv"
USERS_FILE = "users.csv"

# Initialize data files if not present
def initialize_files():
    for file, headers in [
        (BOOKS_FILE, ["Book ID", "Title", "Author", "Available"]),
        (MEMBERS_FILE, ["Member ID", "First Name", "Last Name", "Contact Name", "Contact Address", "Aadhaar Card No", "Start Date", "End Date", "Membership Duration"]),
        (TRANSACTIONS_FILE, ["Transaction ID", "Book ID", "Member ID", "Date", "Type"]),
        (USERS_FILE, ["Username", "Password", "Role"]),
    ]:
        if not os.path.exists(file):
            with open(file, mode="w", newline="") as f:
                writer = csv.writer(f)
                writer.writerow(headers)

# GUI Application class
class LibraryApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Library Management System")
        self.current_role = None
        self.show_login_screen()

    def show_login_screen(self):
        self.clear_screen()

        ttk.Label(self.root, text="Login", font=("Arial", 18)).pack(pady=20)

        form_frame = ttk.Frame(self.root)
        form_frame.pack(pady=20)

        ttk.Label(form_frame, text="Username:").grid(row=0, column=0, padx=5, pady=5)
        self.username_entry = ttk.Entry(form_frame)
        self.username_entry.grid(row=0, column=1, padx=5, pady=5)

        ttk.Label(form_frame, text="Password:").grid(row=1, column=0, padx=5, pady=5)
        self.password_entry = ttk.Entry(form_frame, show="*")
        self.password_entry.grid(row=1, column=1, padx=5, pady=5)

        ttk.Button(form_frame, text="Login", command=self.handle_login).grid(row=2, column=0, pady=10)
        ttk.Button(form_frame, text="Register", command=self.show_register_screen).grid(row=2, column=1, pady=10)

    def handle_login(self):
        username = self.username_entry.get()
        password = self.password_entry.get()

        if not username or not password:
            messagebox.showerror("Error", "Both fields are required")
            return

        with open(USERS_FILE, mode="r") as f:
            reader = csv.DictReader(f)
            for row in reader:
                if row["Username"] == username and row["Password"] == password:
                    self.current_role = row["Role"]
                    if self.current_role == "Admin":
                        self.show_admin_homepage()
                    elif self.current_role == "User":
                        self.show_user_homepage()
                    return

        messagebox.showerror("Error", "Invalid credentials")

    def show_register_screen(self):
        self.clear_screen()

        ttk.Label(self.root, text="Register", font=("Arial", 18)).pack(pady=20)

        form_frame = ttk.Frame(self.root)
        form_frame.pack(pady=20)

        ttk.Label(form_frame, text="Username:").grid(row=0, column=0, padx=5, pady=5)
        self.reg_username_entry = ttk.Entry(form_frame)
        self.reg_username_entry.grid(row=0, column=1, padx=5, pady=5)

        ttk.Label(form_frame, text="Password:").grid(row=1, column=0, padx=5, pady=5)
        self.reg_password_entry = ttk.Entry(form_frame, show="*")
        self.reg_password_entry.grid(row=1, column=1, padx=5, pady=5)

        ttk.Label(form_frame, text="Role:").grid(row=2, column=0, padx=5, pady=5)
        self.reg_role_combo = ttk.Combobox(form_frame, values=["Admin", "User"], state="readonly")
        self.reg_role_combo.grid(row=2, column=1, padx=5, pady=5)

        ttk.Button(form_frame, text="Register", command=self.handle_register).grid(row=3, columnspan=2, pady=10)
        ttk.Button(form_frame, text="Back", command=self.show_login_screen).grid(row=4, columnspan=2, pady=10)

    def handle_register(self):
        username = self.reg_username_entry.get()
        password = self.reg_password_entry.get()
        role = self.reg_role_combo.get()

        if not username or not password or not role:
            messagebox.showerror("Error", "All fields are required")
            return

        with open(USERS_FILE, mode="r") as f:
            reader = csv.DictReader(f)
            for row in reader:
                if row["Username"] == username:
                    messagebox.showerror("Error", "Username already exists")
                    return

        with open(USERS_FILE, mode="a", newline="") as f:
            writer = csv.writer(f)
            writer.writerow([username, password, role])

        messagebox.showinfo("Success", "Registration successful")
        self.show_login_screen()

    def show_admin_homepage(self):
        self.clear_screen()
        ttk.Label(self.root, text="Admin Homepage", font=("Arial", 18)).pack(pady=20)
        ttk.Button(self.root, text="Maintenance Menu", command=self.show_maintenance_menu).pack(pady=10)
        ttk.Button(self.root, text="Report Menu", command=self.show_report_menu).pack(pady=10)
        ttk.Button(self.root, text="Transaction Menu", command=self.show_transaction_menu).pack(pady=10)
        ttk.Button(self.root, text="Logout", command=self.show_login_screen).pack(pady=10)

    def show_user_homepage(self):
        self.clear_screen()
        ttk.Label(self.root, text="User Homepage", font=("Arial", 18)).pack(pady=20)
        ttk.Button(self.root, text="Report Menu", command=self.show_report_menu).pack(pady=10)
        ttk.Button(self.root, text="Transaction Menu", command=self.show_transaction_menu).pack(pady=10)
        ttk.Button(self.root, text="Logout", command=self.show_login_screen).pack(pady=10)

    def show_maintenance_menu(self):
        self.clear_screen()
        ttk.Label(self.root, text="Maintenance Menu", font=("Arial", 18)).pack(pady=20)
        ttk.Button(self.root, text="Membership Add", command=self.show_add_membership).pack(pady=10)
        ttk.Button(self.root, text="Membership Update", command=self.show_update_membership).pack(pady=10)
        ttk.Button(self.root, text="Books/Movies Add", command=self.show_add_books).pack(pady=10)
        ttk.Button(self.root, text="Books/Movies Update", command=self.show_update_books).pack(pady=10)
        ttk.Button(self.root, text="User Management Add", command=self.show_add_user).pack(pady=10)
        ttk.Button(self.root, text="User Management Update", command=self.show_update_user).pack(pady=10)
        ttk.Button(self.root, text="Log Out", command=self.show_login_screen).pack(pady=10)

    def show_report_menu(self):
        messagebox.showinfo("Info", "Report Menu is under development.")

    def show_transaction_menu(self):
        messagebox.showinfo("Info", "Transaction Menu is under development.")

    def show_add_membership(self):
        self.clear_screen()
        ttk.Label(self.root, text="Add Membership", font=("Arial", 18)).pack(pady=20)
        # Fields for adding membership (not included in this snippet for brevity)
        form_frame = ttk.Frame(self.root)
        form_frame.pack(pady=10)

        ttk.Label(form_frame, text="First Name:").grid(row=0, column=0, padx=5, pady=5)
        first_name_entry = ttk.Entry(form_frame)
        first_name_entry.grid(row=0, column=1, padx=5, pady=5)

        ttk.Label(form_frame, text="Last Name:").grid(row=1, column=0, padx=5, pady=5)
        last_name_entry = ttk.Entry(form_frame)
        last_name_entry.grid(row=1, column=1, padx=5, pady=5)

        ttk.Label(form_frame, text="Contact Name:").grid(row=2, column=0, padx=5, pady=5)
        contact_name_entry = ttk.Entry(form_frame)
        contact_name_entry.grid(row=2, column=1, padx=5, pady=5)

        ttk.Label(form_frame, text="Contact Address:").grid(row=3, column=0, padx=5, pady=5)
        contact_address_entry = ttk.Entry(form_frame)
        contact_address_entry.grid(row=3, column=1, padx=5, pady=5)

        ttk.Label(form_frame, text="Aadhaar Card No:").grid(row=4, column=0, padx=5, pady=5)
        aadhaar_entry = ttk.Entry(form_frame)
        aadhaar_entry.grid(row=4, column=1, padx=5, pady=5)

        ttk.Label(form_frame, text="Start Date:").grid(row=5, column=0, padx=5, pady=5)
        start_date_entry = DateEntry(form_frame, date_pattern='y-mm-dd')
        start_date_entry.grid(row=5, column=1, padx=5, pady=5)

        ttk.Label(form_frame, text="End Date:").grid(row=6, column=0, padx=5, pady=5)
        end_date_entry = DateEntry(form_frame, date_pattern='y-mm-dd')
        end_date_entry.grid(row=6, column=1, padx=5, pady=5)

        ttk.Label(form_frame, text="Membership Duration:").grid(row=7, column=0, padx=5, pady=5)
        membership_var = tk.StringVar()
        ttk.Radiobutton(form_frame, text="Six Months", variable=membership_var, value="6 Months").grid(row=7, column=1, padx=5, pady=5, sticky="w")
        ttk.Radiobutton(form_frame, text="One Year", variable=membership_var, value="1 Year").grid(row=8, column=1, padx=5, pady=5, sticky="w")
        ttk.Radiobutton(form_frame, text="Two Years", variable=membership_var, value="2 Years").grid(row=9, column=1, padx=5, pady=5, sticky="w")

        def confirm_membership():
            first_name = first_name_entry.get()
            last_name = last_name_entry.get()
            contact_name = contact_name_entry.get()
            contact_address = contact_address_entry.get()
            aadhaar = aadhaar_entry.get()
            start_date = start_date_entry.get()
            end_date = end_date_entry.get()
            membership_duration = membership_var.get()

            if not all([first_name, last_name, contact_name, contact_address, aadhaar, start_date, end_date, membership_duration]):
                messagebox.showerror("Error", "All fields are required")
                return

            with open(MEMBERS_FILE, mode="a", newline="") as f:
                writer = csv.writer(f)
                writer.writerow(["M" + str(sum(1 for _ in open(MEMBERS_FILE)) + 1), first_name, last_name, contact_name, contact_address, aadhaar, start_date, end_date, membership_duration])

            messagebox.showinfo("Success", "Membership added successfully")
            self.show_maintenance_menu()

        ttk.Button(form_frame, text="Confirm", command=confirm_membership).grid(row=10, column=0, pady=10)
        ttk.Button(form_frame, text="Cancel", command=self.show_maintenance_menu).grid(row=10, column=1, pady=10)

    def show_update_membership(self):
        self.clear_screen()
        ttk.Label(self.root, text="Update Membership", font=("Arial", 18)).pack(pady=20)

        form_frame = ttk.Frame(self.root)
        form_frame.pack(pady=10)

        ttk.Label(form_frame, text="Membership Number :").grid(row=0, column=0, padx=5, pady=5)
        membership_id_entry = ttk.Entry(form_frame)
        membership_id_entry.grid(row=0, column=1, padx=5, pady=5)

        ttk.Label(form_frame, text="Start Date:").grid(row=1, column=0, padx=5, pady=5)
        start_date_entry = DateEntry(form_frame, date_pattern='y-mm-dd')
        start_date_entry.grid(row=1, column=1, padx=5, pady=5)

        ttk.Label(form_frame, text="End Date:").grid(row=2, column=0, padx=5, pady=5)
        end_date_entry = DateEntry(form_frame, date_pattern='y-mm-dd')
        end_date_entry.grid(row=2, column=1, padx=5, pady=5)

        membership_duration_var = tk.StringVar()
        ttk.Radiobutton(form_frame, text="Six Months", variable=membership_duration_var, value="6 Months").grid(row=3, column=1, padx=5, pady=5, sticky="w")
        ttk.Radiobutton(form_frame, text="One Year", variable=membership_duration_var, value="1 Year").grid(row=4, column=1, padx=5, pady=5, sticky="w")
        ttk.Radiobutton(form_frame, text="Two Years", variable=membership_duration_var, value="2 Years").grid(row=5, column=1, padx=5, pady=5, sticky="w")
        ttk.Label(form_frame, text="Membership Type :").grid(row=6, column=0, padx=5, pady=5)

        membership_type_var = tk.StringVar()
        ttk.Radiobutton(form_frame, text="Book", variable=membership_type_var, value="Book").grid(row=7, column=1, padx=5, pady=5, sticky="w")
        ttk.Radiobutton(form_frame, text="Movie", variable=membership_type_var, value="Movie").grid(row=8, column=1, padx=5, pady=5, sticky="w")

        def confirm_update_membership():
            membership_id = membership_id_entry.get()
            start_date = start_date_entry.get()
            end_date = end_date_entry.get()
            membership_duration = membership_duration_var.get()
            membership_type = membership_type_var.get()

            if not all([membership_id, start_date, end_date, membership_duration, membership_type]):
                messagebox.showerror("Error", "All fields are required")
                return

            # Implement membership update logic here
            # For this example, we're simply printing the data
            messagebox.showinfo("Success", f"Membership {membership_id} updated successfully")

            self.show_maintenance_menu()

        ttk.Button(form_frame, text="Confirm", command=confirm_update_membership).grid(row=9, column=0, pady=10)
        ttk.Button(form_frame, text="Cancel", command=self.show_maintenance_menu).grid(row=9, column=1, pady=10)

    def show_add_books(self):
        self.clear_screen()
        ttk.Label(self.root, text="Add Book/Movie", font=("Arial", 18)).pack(pady=20)

        form_frame = ttk.Frame(self.root)
        form_frame.pack(pady=10)

        ttk.Label(form_frame, text="Book/Movie Name:").grid(row=0, column=0, padx=5, pady=5)
        book_movie_name_entry = ttk.Entry(form_frame)
        book_movie_name_entry.grid(row=0, column=1, padx=5, pady=5)

        ttk.Label(form_frame, text="Quantity/Copies:").grid(row=1, column=0, padx=5, pady=5)
        quantity_entry = ttk.Entry(form_frame)
        quantity_entry.insert(0, "1")  # Default to 1
        quantity_entry.grid(row=1, column=1, padx=5, pady=5)

        ttk.Label(form_frame, text="Date of Procurement:").grid(row=2, column=0, padx=5, pady=5)
        procurement_date_entry = DateEntry(form_frame, date_pattern='y-mm-dd')
        procurement_date_entry.grid(row=2, column=1, padx=5, pady=5)

        type_var = tk.StringVar()
        ttk.Radiobutton(form_frame, text="Book", variable=type_var, value="Book").grid(row=3, column=1, padx=5, pady=5, sticky="w")
        ttk.Radiobutton(form_frame, text="Movie", variable=type_var, value="Movie").grid(row=4, column=1, padx=5, pady=5, sticky="w")

        def confirm_add_book_movie():
            name = book_movie_name_entry.get()
            quantity = quantity_entry.get()
            procurement_date = procurement_date_entry.get()
            type_value = type_var.get()

            if not all([name, quantity, procurement_date, type_value]):
                messagebox.showerror("Error", "All fields are required")
                return

            with open(BOOKS_FILE, mode="a", newline="") as f:
                writer = csv.writer(f)
                writer.writerow([str(sum(1 for _ in open(BOOKS_FILE)) + 1), name, type_value, quantity])

            messagebox.showinfo("Success", "Book/Movie added successfully")
            self.show_maintenance_menu()

        ttk.Button(form_frame, text="Confirm", command=confirm_add_book_movie).grid(row=5, column=0, pady=10)
        ttk.Button(form_frame, text="Cancel", command=self.show_maintenance_menu).grid(row=5, column=1, pady=10)

    def show_update_books(self):
        self.clear_screen()

        ttk.Label(self.root, text="Update Books/Movies", font=("Arial", 18)).pack(pady=20)

        # Frame for the form
        form_frame = ttk.Frame(self.root)
        form_frame.pack(pady=10)

       

        # Radio buttons for Book or Movie
        media_type_var = tk.StringVar()
        ttk.Radiobutton(form_frame, text="Book", variable=media_type_var, value="Book").grid(row=1, column=0, padx=5, pady=5, sticky="w")
        ttk.Radiobutton(form_frame, text="Movie", variable=media_type_var, value="Movie").grid(row=2, column=0, padx=5, pady=5, sticky="w")

        # Dropdown for Book/Movie Name
        ttk.Label(form_frame, text="Book/Movie Name:").grid(row=3, column=0, padx=5, pady=5)
        media_name_combobox = ttk.Combobox(form_frame, state="readonly")
        media_name_combobox.grid(row=3, column=1, padx=5, pady=5)

        # Populate media_name_combobox with data from CSV (Books/Movies)
        with open(BOOKS_FILE, mode="r") as f:
            reader = csv.DictReader(f)
            media_names = [row["Title"] for row in reader]
        media_name_combobox["values"] = media_names

        # Status dropdown (for Book or Movie)
        ttk.Label(form_frame, text="Status:").grid(row=4, column=0, padx=5, pady=5)
        status_combobox = ttk.Combobox(form_frame, state="readonly", values=["Available", "Checked Out", "Damaged"])
        status_combobox.grid(row=4, column=1, padx=5, pady=5)

        # Date of Procurement calendar
        ttk.Label(form_frame, text="Date of Procurement:").grid(row=5, column=0, padx=5, pady=5)
        procurement_date_entry = DateEntry(form_frame, date_pattern='y-mm-dd')
        procurement_date_entry.grid(row=5, column=1, padx=5, pady=5)

        # Submit button
        def confirm_update_book():
            media_type = media_type_var.get()
            media_name = media_name_combobox.get()
            status = status_combobox.get()
            procurement_date = procurement_date_entry.get()

            if not all([media_type, media_name, status, procurement_date]):
                messagebox.showerror("Error", "All fields are required")
                return

            # Update the relevant CSV file (Books or Movies)
            file = BOOKS_FILE if media_type == "Book" else MOVIES_FILE
            updated = False

            # Update logic
            temp_rows = []
            with open(file, mode="r") as f:
                reader = csv.DictReader(f)
                for row in reader:
                    if row["Title"] == media_name:
                        row["Status"] = status
                        row["Procurement Date"] = procurement_date
                        updated = True
                    temp_rows.append(row)

            # If updated, write changes back to the file
            if updated:
                with open(file, mode="w", newline="") as f:
                    writer = csv.DictWriter(f, fieldnames=["Title", "Author", "Status", "Procurement Date"])
                    writer.writeheader()
                    writer.writerows(temp_rows)

                messagebox.showinfo("Success", f"{media_type} {media_name} updated successfully")
                self.show_maintenance_menu()  # Go back to Maintenance Menu
            else:
                messagebox.showerror("Error", f"{media_name} not found")

        ttk.Button(form_frame, text="Confirm", command=confirm_update_book).grid(row=6, column=0, pady=10)
        ttk.Button(form_frame, text="Cancel", command=self.show_maintenance_menu).grid(row=6, column=1, pady=10)


 



    def show_add_user(self):
        self.clear_screen()

        ttk.Label(self.root, text="User Management", font=("Arial", 18)).pack(pady=20)

        # Frame for the form
        form_frame = ttk.Frame(self.root)
        form_frame.pack(pady=10)

        # Radio buttons for New User or Existing User
        user_type_var = tk.StringVar()
        ttk.Radiobutton(form_frame, text="New User", variable=user_type_var, value="New User").grid(row=1, column=0, padx=5, pady=5, sticky="w")
        ttk.Radiobutton(form_frame, text="Existing User", variable=user_type_var, value="Existing User").grid(row=2, column=0, padx=5, pady=5, sticky="w")

        # Name entry field
        ttk.Label(form_frame, text="Name:").grid(row=3, column=0, padx=5, pady=5)
        user_name_entry = ttk.Entry(form_frame)
        user_name_entry.grid(row=3, column=1, padx=5, pady=5)

        # Admin checkbox (for New or Existing User)
        ttk.Label(form_frame, text="Admin:").grid(row=4, column=0, padx=5, pady=5)
        admin_checkbox = ttk.Checkbutton(form_frame)
        admin_checkbox.grid(row=4, column=1, padx=5, pady=5)

        # Active checkbox (for New or Existing User)
        ttk.Label(form_frame, text="Active:").grid(row=5, column=0, padx=5, pady=5)
        active_checkbox = ttk.Checkbutton(form_frame)
        active_checkbox.grid(row=5, column=1, padx=5, pady=5)

        # Submit button
        def confirm_add_user():
            # Get values from the form
            user_type = user_type_var.get()
            user_name = user_name_entry.get()
            is_admin = admin_checkbox.instate(["selected"])
            is_active = active_checkbox.instate(["selected"])

            # Debug: Print the values for verification
            print(f"User Type: {user_type}")
            print(f"User Name: {user_name}")
            print(f"Admin: {is_admin}")
            print(f"Active: {is_active}")

            # Validate fields
            if not user_name:
                messagebox.showerror("Error", "Name field is required")
                return

            # Logic for adding new user or updating existing user
            if user_type == "New User":
                # Add new user logic
                self.add_new_user(user_name, is_admin, is_active)
            elif user_type == "Existing User":
                # Update existing user logic
                self.update_existing_user(user_name, is_admin, is_active)

        def add_new_user(user_name, is_admin, is_active):
            # Example logic for adding a new user
            with open(USERS_FILE, mode="a", newline="") as f:
                writer = csv.writer(f)
                writer.writerow([user_name, "Password", "Email", "Phone", "Date", "Admin" if is_admin else "User", "Active" if is_active else "Inactive"])

            messagebox.showinfo("Success", f"New user {user_name} added successfully")
            self.show_maintenance_menu()  # Go back to Maintenance Menu

        def update_existing_user(user_name, is_admin, is_active):
            # Update the user data in the file
            updated = False
            temp_rows = []
            with open(USERS_FILE, mode="r") as f:
                reader = csv.reader(f)
                for row in reader:
                    if row[0] == user_name:
                        row[5] = "Admin" if is_admin else "User"
                        row[6] = "Active" if is_active else "Inactive"
                        updated = True
                    temp_rows.append(row)

            if updated:
                with open(USERS_FILE, mode="w", newline="") as f:
                    writer = csv.writer(f)
                    writer.writerows(temp_rows)
                messagebox.showinfo("Success", f"User {user_name} updated successfully")
            else:
                messagebox.showerror("Error", f"User {user_name} not found")

            self.show_maintenance_menu()  # Go back to Maintenance Menu

        # Ensure confirm button calls confirm_add_user() correctly
        confirm_button = ttk.Button(form_frame, text="Confirm", command=confirm_add_user)
        confirm_button.grid(row=6, column=0, pady=10)

        cancel_button = ttk.Button(form_frame, text="Cancel", command=self.show_maintenance_menu)
        cancel_button.grid(row=6, column=1, pady=10)

    def home_button_action(self):
        if self.current_role == "Admin":
            self.show_admin_homepage()
        else:
            self.show_user_homepage()



    
    def show_update_user(self):
        self.clear_screen()

        ttk.Label(self.root, text="User Management", font=("Arial", 18)).pack(pady=20)

        # Frame for the form
        form_frame = ttk.Frame(self.root)
        form_frame.pack(pady=10)

        # Radio buttons for New User or Existing User
        user_type_var = tk.StringVar(value="New User")
        ttk.Radiobutton(form_frame, text="New User", variable=user_type_var, value="New User").grid(row=1, column=0, padx=5, pady=5, sticky="w")
        ttk.Radiobutton(form_frame, text="Existing User", variable=user_type_var, value="Existing User").grid(row=2, column=0, padx=5, pady=5, sticky="w")

        # Name entry field
        ttk.Label(form_frame, text="Name:").grid(row=3, column=0, padx=5, pady=5)
        user_name_entry = ttk.Entry(form_frame)
        user_name_entry.grid(row=3, column=1, padx=5, pady=5)

        # Admin checkbox (for New or Existing User)
        ttk.Label(form_frame, text="Admin:").grid(row=4, column=0, padx=5, pady=5)
        admin_checkbox = ttk.Checkbutton(form_frame)
        admin_checkbox.grid(row=4, column=1, padx=5, pady=5)

        # Active checkbox (for New or Existing User)
        ttk.Label(form_frame, text="Active:").grid(row=5, column=0, padx=5, pady=5)
        active_checkbox = ttk.Checkbutton(form_frame)
        active_checkbox.grid(row=5, column=1, padx=5, pady=5)

        # Submit button
        def confirm_update_user():
            # Get values from the form
            user_type = user_type_var.get()
            user_name = user_name_entry.get()
            is_admin = admin_checkbox.instate(["selected"])
            is_active = active_checkbox.instate(["selected"])

            # Validate fields
            if not user_name:
                messagebox.showerror("Error", "Name field is required")
                return

            # Logic for adding new user or updating existing user
            if user_type == "New User":
                # Add new user logic
                self.add_new_user(user_name, is_admin, is_active)
            elif user_type == "Existing User":
                # Update existing user logic
                self.update_existing_user(user_name, is_admin, is_active)

        def add_new_user(user_name, is_admin, is_active):
            # Example logic for adding a new user
            with open('users.csv', mode="a", newline="") as f:
                writer = csv.writer(f)
                writer.writerow([user_name, "Password", "Email", "Phone", "Date", "Admin" if is_admin else "User", "Active" if is_active else "Inactive"])

            messagebox.showinfo("Success", f"New user {user_name} added successfully")
            self.show_maintenance_menu()  # Go back to Maintenance Menu

        def update_existing_user(user_name, is_admin, is_active):
            # Update the user data in the file
            updated = False
            temp_rows = []
            with open('users.csv', mode="r") as f:
                reader = csv.reader(f)
                for row in reader:
                    if row[0] == user_name:
                        row[5] = "Admin" if is_admin else "User"
                        row[6] = "Active" if is_active else "Inactive"
                        updated = True
                    temp_rows.append(row)

            if updated:
                with open('users.csv', mode="w", newline="") as f:
                    writer = csv.writer(f)
                    writer.writerows(temp_rows)
                messagebox.showinfo("Success", f"User {user_name} updated successfully")
            else:
                messagebox.showerror("Error", f"User {user_name} not found")

            self.show_maintenance_menu()  # Go back to Maintenance Menu

        confirm_button = ttk.Button(form_frame, text="Confirm", command=confirm_update_user)
        confirm_button.grid(row=6, column=0, pady=10)

        cancel_button = ttk.Button(form_frame, text="Cancel", command=self.show_maintenance_menu)
        cancel_button.grid(row=6, column=1, pady=10)


    

    def clear_screen(self):
        for widget in self.root.winfo_children():
            widget.destroy()

# Initialize files and add sample user data
initialize_files()
if os.stat(USERS_FILE).st_size == 0:  # Add sample users if the file is empty
    with open(USERS_FILE, mode="a", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["admin", "admin123", "Admin"])
        writer.writerow(["user", "user123", "User"])

# Run the application
root = tk.Tk()
app = LibraryApp(root)
root.mainloop()


