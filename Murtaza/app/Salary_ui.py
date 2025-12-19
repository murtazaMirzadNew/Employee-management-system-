import tkinter as tk
from tkinter import ttk, messagebox
from db import get_connection

class SalaryUI:
    def __init__(self, parent, main_app):
        self.parent = parent
        self.main_app = main_app
        self.frame = tk.Frame(parent, bg="#F5F5F5")
        self.frame.pack(fill="both", expand=True)

        header = tk.Label(self.frame, text="Salary Management", font=("Arial", 16, "bold"),
                          fg="#2C3E50", bg="#F5F5F5")
        header.pack(pady=15)

        form_frame = tk.Frame(self.frame, bg="#F5F5F5")
        form_frame.pack(pady=10)

        tk.Label(form_frame, text="Employee ID:", bg="#F5F5F5", fg="#2C3E50").grid(row=0, column=0, sticky="w", padx=10, pady=5)
        self.emp_id = tk.Entry(form_frame)
        self.emp_id.grid(row=0, column=1, padx=10, pady=5, ipadx=5)

        tk.Label(form_frame, text="Month-Year (YYYY-MM):", bg="#F5F5F5", fg="#2C3E50").grid(row=1, column=0, sticky="w", padx=10, pady=5)
        self.month_year = tk.Entry(form_frame)
        self.month_year.grid(row=1, column=1, padx=10, pady=5, ipadx=5)

        tk.Label(form_frame, text="Base Salary:", bg="#F5F5F5", fg="#2C3E50").grid(row=2, column=0, sticky="w", padx=10, pady=5)
        self.base_salary = tk.Entry(form_frame)
        self.base_salary.grid(row=2, column=1, padx=10, pady=5, ipadx=5)

        tk.Label(form_frame, text="Bonus:", bg="#F5F5F5", fg="#2C3E50").grid(row=3, column=0, sticky="w", padx=10, pady=5)
        self.bonus = tk.Entry(form_frame)
        self.bonus.grid(row=3, column=1, padx=10, pady=5, ipadx=5)

        tk.Label(form_frame, text="Deductions:", bg="#F5F5F5", fg="#2C3E50").grid(row=4, column=0, sticky="w", padx=10, pady=5)
        self.deductions = tk.Entry(form_frame)
        self.deductions.grid(row=4, column=1, padx=10, pady=5, ipadx=5)

        btn = tk.Button(form_frame, text="Add Salary Record", bg="#3498DB", fg="white",
                        font=("Arial", 10, "bold"), relief="raised", bd=2,
                        activebackground="#2980B9", activeforeground="white",
                        command=self.add_salary)
        btn.grid(row=5, column=0, columnspan=2, pady=15, sticky="ew", padx=20)

        list_header = tk.Label(self.frame, text="Salary Records:", font=("Arial", 12, "bold"),
                               fg="#2C3E50", bg="#F5F5F5")
        list_header.pack(pady=5)

        self.tree = ttk.Treeview(self.frame, columns=("ID", "Emp Name", "Month", "Net Salary"), show="headings")
        self.tree.heading("ID", text="ID")
        self.tree.heading("Emp Name", text="Employee")
        self.tree.heading("Month", text="Month-Year")
        self.tree.heading("Net Salary", text="Net Salary")
        self.tree.pack(fill="both", expand=True, padx=15, pady=10)

        style = ttk.Style()
        style.theme_use("default")
        style.configure("Treeview", background="#FFFFFF", foreground="#2C3E50", fieldbackground="#FFFFFF")
        style.map('Treeview', background=[('selected', '#3498DB')])

        self.load_salaries()

    def add_salary(self):
        try:
            conn = get_connection()
            if not conn:
                messagebox.showerror("Error", "Database connection failed")
                return

            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO salary (sal_id, emp_id, month_year, base_salary, bonus, deductions, net_salary)
                VALUES (sal_seq.NEXTVAL, :emp_id, :month_year, :base, :bonus, :deduct, calculate_net_salary(:base, :bonus, :deduct))
            """, {
                'emp_id': int(self.emp_id.get()),
                'month_year': self.month_year.get(),
                'base': float(self.base_salary.get()),
                'bonus': float(self.bonus.get()),
                'deduct': float(self.deductions.get())
            })
            conn.commit()
            cursor.close()
            conn.close()

            messagebox.showinfo("Success", "Salary record added!")
            self.load_salaries()
            self.clear_form()

        except Exception as e:
            messagebox.showerror("Error", str(e))

    def load_salaries(self):
        for item in self.tree.get_children():
            self.tree.delete(item)

        conn = get_connection()
        if not conn:
            return

        cursor = conn.cursor()
        cursor.execute("""
            SELECT s.sal_id, get_employee_fullname(s.emp_id), s.month_year, s.net_salary
            FROM salary s
        """)
        for row in cursor.fetchall():
            self.tree.insert("", "end", values=row)
        cursor.close()
        conn.close()

    def clear_form(self):
        self.emp_id.delete(0, tk.END)
        self.month_year.delete(0, tk.END)
        self.base_salary.delete(0, tk.END)
        self.bonus.delete(0, tk.END)
        self.deductions.delete(0, tk.END)