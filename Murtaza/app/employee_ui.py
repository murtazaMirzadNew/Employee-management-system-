import tkinter as tk
from tkinter import ttk, messagebox
from db import get_connection

class EmployeeUI:
    def __init__(self, parent, main_app):
        self.parent = parent
        self.main_app = main_app
        self.frame = tk.Frame(parent, bg="#F5F5F5")
        self.frame.pack(fill="both", expand=True)

        # Header
        header = tk.Label(
            self.frame,
            text="Employee Management",
            font=("Arial", 16, "bold"),
            fg="#2C3E50",
            bg="#F5F5F5"
        )
        header.pack(pady=15)

        # Form Frame
        form_frame = tk.Frame(self.frame, bg="#F5F5F5")
        form_frame.pack(pady=10)

        # Input Fields
        tk.Label(form_frame, text="First Name:", bg="#F5F5F5", fg="#2C3E50").grid(row=0, column=0, sticky="w", padx=10, pady=5)
        self.first_name = tk.Entry(form_frame)
        self.first_name.grid(row=0, column=1, padx=10, pady=5, ipadx=5)

        tk.Label(form_frame, text="Last Name:", bg="#F5F5F5", fg="#2C3E50").grid(row=1, column=0, sticky="w", padx=10, pady=5)
        self.last_name = tk.Entry(form_frame)
        self.last_name.grid(row=1, column=1, padx=10, pady=5, ipadx=5)

        tk.Label(form_frame, text="Email:", bg="#F5F5F5", fg="#2C3E50").grid(row=2, column=0, sticky="w", padx=10, pady=5)
        self.email = tk.Entry(form_frame)
        self.email.grid(row=2, column=1, padx=10, pady=5, ipadx=5)

        tk.Label(form_frame, text="Phone:", bg="#F5F5F5", fg="#2C3E50").grid(row=3, column=0, sticky="w", padx=10, pady=5)
        self.phone = tk.Entry(form_frame)
        self.phone.grid(row=3, column=1, padx=10, pady=5, ipadx=5)

        tk.Label(form_frame, text="Job Title:", bg="#F5F5F5", fg="#2C3E50").grid(row=4, column=0, sticky="w", padx=10, pady=5)
        self.job_title = tk.Entry(form_frame)
        self.job_title.grid(row=4, column=1, padx=10, pady=5, ipadx=5)

        tk.Label(form_frame, text="Department:", bg="#F5F5F5", fg="#2C3E50").grid(row=5, column=0, sticky="w", padx=10, pady=5)
        self.department = tk.Entry(form_frame)
        self.department.grid(row=5, column=1, padx=10, pady=5, ipadx=5)

        tk.Label(form_frame, text="Salary:", bg="#F5F5F5", fg="#2C3E50").grid(row=6, column=0, sticky="w", padx=10, pady=5)
        self.salary = tk.Entry(form_frame)
        self.salary.grid(row=6, column=1, padx=10, pady=5, ipadx=5)

        # Centered Button
        btn = tk.Button(
            form_frame,
            text="Add Employee",
            bg="#3498DB",
            fg="white",
            font=("Arial", 10, "bold"),
            relief="raised",
            bd=2,
            activebackground="#2980B9",
            activeforeground="white",
            command=self.add_employee
        )
        btn.grid(row=7, column=0, columnspan=2, pady=15, sticky="ew", padx=20)

        # List Header
        list_header = tk.Label(
            self.frame,
            text="Active Employees:",
            font=("Arial", 12, "bold"),
            fg="#2C3E50",
            bg="#F5F5F5"
        )
        list_header.pack(pady=5)

        # Treeview
        self.tree = ttk.Treeview(
            self.frame,
            columns=("ID", "Name", "Email", "Dept", "Salary"),
            show="headings"
        )
        self.tree.heading("ID", text="ID")
        self.tree.heading("Name", text="Name")
        self.tree.heading("Email", text="Email")
        self.tree.heading("Dept", text="Department")
        self.tree.heading("Salary", text="Salary")
        self.tree.pack(fill="both", expand=True, padx=15, pady=10)

        # Style Treeview
        style = ttk.Style()
        style.theme_use("default")
        style.configure(
            "Treeview",
            background="#FFFFFF",
            foreground="#2C3E50",
            fieldbackground="#FFFFFF",
            rowheight=25
        )
        style.map('Treeview', background=[('selected', '#3498DB')])

        self.load_employees()

    def add_employee(self):
        try:
            conn = get_connection()
            if not conn:
                messagebox.showerror("Error", "Database connection failed")
                return

            cursor = conn.cursor()
            cursor.callproc('add_employee', [
                self.first_name.get(),
                self.last_name.get(),
                self.email.get(),
                self.phone.get(),
                self.job_title.get(),
                self.department.get(),
                float(self.salary.get())
            ])
            conn.commit()
            cursor.close()
            conn.close()

            messagebox.showinfo("Success", "Employee added successfully!")
            self.load_employees()
            self.clear_form()

        except Exception as e:
            messagebox.showerror("Error", str(e))

    def load_employees(self):
        for item in self.tree.get_children():
            self.tree.delete(item)

        conn = get_connection()
        if not conn:
            return

        cursor = conn.cursor()
        cursor.execute("SELECT emp_id, first_name || ' ' || last_name, email, department, salary FROM active_employees")
        for row in cursor.fetchall():
            self.tree.insert("", "end", values=row)
        cursor.close()
        conn.close()

    def clear_form(self):
        self.first_name.delete(0, tk.END)
        self.last_name.delete(0, tk.END)
        self.email.delete(0, tk.END)
        self.phone.delete(0, tk.END)
        self.job_title.delete(0, tk.END)
        self.department.delete(0, tk.END)
        self.salary.delete(0, tk.END)