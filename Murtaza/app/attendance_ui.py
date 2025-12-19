import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime
from db import get_connection

class AttendanceUI:
    def __init__(self, parent, main_app):
        self.parent = parent
        self.main_app = main_app
        self.frame = tk.Frame(parent, bg="#F5F5F5")
        self.frame.pack(fill="both", expand=True)

        header = tk.Label(self.frame, text="Attendance Management", font=("Arial", 16, "bold"),
                          fg="#2C3E50", bg="#F5F5F5")
        header.pack(pady=15)

        form_frame = tk.Frame(self.frame, bg="#F5F5F5")
        form_frame.pack(pady=10)

        tk.Label(form_frame, text="Employee ID:", bg="#F5F5F5", fg="#2C3E50").grid(row=0, column=0, sticky="w", padx=10, pady=5)
        self.emp_id = tk.Entry(form_frame)
        self.emp_id.grid(row=0, column=1, padx=10, pady=5, ipadx=5)

        tk.Label(form_frame, text="Check-In Time:", bg="#F5F5F5", fg="#2C3E50").grid(row=1, column=0, sticky="w", padx=10, pady=5)
        self.check_in = tk.Entry(form_frame)
        self.check_in.grid(row=1, column=1, padx=10, pady=5, ipadx=5)
        self.check_in.insert(0, datetime.now().strftime("%Y-%m-%d %H:%M:%S"))

        tk.Label(form_frame, text="Check-Out Time:", bg="#F5F5F5", fg="#2C3E50").grid(row=2, column=0, sticky="w", padx=10, pady=5)
        self.check_out = tk.Entry(form_frame)
        self.check_out.grid(row=2, column=1, padx=10, pady=5, ipadx=5)
        self.check_out.insert(0, "")  # Optional

        btn = tk.Button(form_frame, text="Record Attendance", bg="#3498DB", fg="white",
                        font=("Arial", 10, "bold"), relief="raised", bd=2,
                        activebackground="#2980B9", activeforeground="white",
                        command=self.record_attendance)
        btn.grid(row=3, column=0, columnspan=2, pady=15, sticky="ew", padx=20)

        list_header = tk.Label(self.frame, text="Attendance Records:", font=("Arial", 12, "bold"),
                               fg="#2C3E50", bg="#F5F5F5")
        list_header.pack(pady=5)

        self.tree = ttk.Treeview(self.frame, columns=("ID", "Emp Name", "Date", "Check-In", "Check-Out", "Hours"), show="headings")
        self.tree.heading("ID", text="ID")
        self.tree.heading("Emp Name", text="Employee")
        self.tree.heading("Date", text="Date")
        self.tree.heading("Check-In", text="Check-In")
        self.tree.heading("Check-Out", text="Check-Out")
        self.tree.heading("Hours", text="Hours Worked")
        self.tree.pack(fill="both", expand=True, padx=15, pady=10)

        style = ttk.Style()
        style.theme_use("default")
        style.configure("Treeview", background="#FFFFFF", foreground="#2C3E50", fieldbackground="#FFFFFF")
        style.map('Treeview', background=[('selected', '#3498DB')])

        self.load_attendance()

    def record_attendance(self):
        try:
            emp_id = int(self.emp_id.get())
        except ValueError:
            messagebox.showerror("Error", "Employee ID must be a number.")
            return

        check_in_str = self.check_in.get().strip()
        if not check_in_str:
            messagebox.showerror("Error", "Check-in time is required.")
            return

        # Parse check-in
        try:
            check_in_dt = datetime.strptime(check_in_str, "%Y-%m-%d %H:%M:%S")
        except ValueError:
            messagebox.showerror("Error", "Invalid Check-In format. Use: YYYY-MM-DD HH:MM:SS")
            return

        # Parse check-out (optional)
        check_out_dt = None
        check_out_str = self.check_out.get().strip()
        if check_out_str:
            try:
                check_out_dt = datetime.strptime(check_out_str, "%Y-%m-%d %H:%M:%S")
            except ValueError:
                messagebox.showerror("Error", "Invalid Check-Out format. Use: YYYY-MM-DD HH:MM:SS")
                return

        conn = get_connection()
        if not conn:
            messagebox.showerror("Error", "Database connection failed")
            return

        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO attendance (att_id, emp_id, att_date, check_in, check_out)
            VALUES (att_seq.NEXTVAL, :emp_id, SYSDATE, :check_in, :check_out)
        """, {
            'emp_id': emp_id,
            'check_in': check_in_dt,
            'check_out': check_out_dt
        })
        conn.commit()
        cursor.close()
        conn.close()

        messagebox.showinfo("Success", "Attendance recorded!")
        self.load_attendance()
        self.clear_form()

        # Clear fields after success
        self.clear_form()

    def load_attendance(self):
        for item in self.tree.get_children():
            self.tree.delete(item)

        conn = get_connection()
        if not conn:
            return

        cursor = conn.cursor()
        cursor.execute("""
            SELECT a.att_id, get_employee_fullname(a.emp_id), TO_CHAR(a.att_date, 'YYYY-MM-DD'),
                   TO_CHAR(a.check_in, 'YYYY-MM-DD HH24:MI:SS'), 
                   TO_CHAR(a.check_out, 'YYYY-MM-DD HH24:MI:SS'),
                   ROUND((CAST(a.check_out AS DATE) - CAST(a.check_in AS DATE)) * 24, 2)
            FROM attendance a
            WHERE a.check_in IS NOT NULL
        """)
        for row in cursor.fetchall():
            self.tree.insert("", "end", values=row)
        cursor.close()
        conn.close()

    def clear_form(self):
        self.emp_id.delete(0, tk.END)
        self.check_in.delete(0, tk.END)
        self.check_in.insert(0, datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
        self.check_out.delete(0, tk.END)
        self.check_out.insert(0, "")