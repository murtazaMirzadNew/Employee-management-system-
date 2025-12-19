import tkinter as tk
from tkinter import ttk, messagebox
from db import get_connection

class PayslipUI:
    def __init__(self, parent, main_app):
        self.parent = parent
        self.main_app = main_app
        self.frame = tk.Frame(parent, bg="#F5F5F5")
        self.frame.pack(fill="both", expand=True)

        header = tk.Label(self.frame, text="Payslip Generation", font=("Arial", 16, "bold"),
                          fg="#2C3E50", bg="#F5F5F5")
        header.pack(pady=15)

        form_frame = tk.Frame(self.frame, bg="#F5F5F5")
        form_frame.pack(pady=10)

        tk.Label(form_frame, text="Salary ID:", bg="#F5F5F5", fg="#2C3E50").grid(row=0, column=0, sticky="w", padx=10, pady=5)
        self.sal_id = tk.Entry(form_frame)
        self.sal_id.grid(row=0, column=1, padx=10, pady=5, ipadx=5)

        tk.Label(form_frame, text="PDF Path (e.g., C:/payslips/slip.pdf):", bg="#F5F5F5", fg="#2C3E50").grid(row=1, column=0, sticky="w", padx=10, pady=5)
        self.pdf_path = tk.Entry(form_frame, width=50)
        self.pdf_path.grid(row=1, column=1, padx=10, pady=5, ipadx=5)

        btn = tk.Button(form_frame, text="Generate Payslip", bg="#3498DB", fg="white",
                        font=("Arial", 10, "bold"), relief="raised", bd=2,
                        activebackground="#2980B9", activeforeground="white",
                        command=self.generate_payslip)
        btn.grid(row=2, column=0, columnspan=2, pady=15, sticky="ew", padx=20)

        list_header = tk.Label(self.frame, text="Generated Payslips:", font=("Arial", 12, "bold"),
                               fg="#2C3E50", bg="#F5F5F5")
        list_header.pack(pady=5)

        self.tree = ttk.Treeview(self.frame, columns=("ID", "Sal ID", "Generated Date", "PDF Path"), show="headings")
        self.tree.heading("ID", text="ID")
        self.tree.heading("Sal ID", text="Salary ID")
        self.tree.heading("Generated Date", text="Generated Date")
        self.tree.heading("PDF Path", text="PDF Path")
        self.tree.pack(fill="both", expand=True, padx=15, pady=10)

        style = ttk.Style()
        style.theme_use("default")
        style.configure("Treeview", background="#FFFFFF", foreground="#2C3E50", fieldbackground="#FFFFFF")
        style.map('Treeview', background=[('selected', '#3498DB')])

        self.load_payslips()

    def generate_payslip(self):
        try:
            conn = get_connection()
            if not conn:
                messagebox.showerror("Error", "Database connection failed")
                return

            cursor = conn.cursor()
            cursor.callproc('generate_payslip', [int(self.sal_id.get()), self.pdf_path.get()])
            conn.commit()
            cursor.close()
            conn.close()

            messagebox.showinfo("Success", "Payslip generated!")
            self.load_payslips()
            self.clear_form()

        except Exception as e:
            messagebox.showerror("Error", str(e))

    def load_payslips(self):
        for item in self.tree.get_children():
            self.tree.delete(item)

        conn = get_connection()
        if not conn:
            return

        cursor = conn.cursor()
        cursor.execute("""
            SELECT payslip_id, sal_id, TO_CHAR(generated_date, 'YYYY-MM-DD HH24:MI:SS'), pdf_path
            FROM payslip
        """)
        for row in cursor.fetchall():
            self.tree.insert("", "end", values=row)
        cursor.close()
        conn.close()

    def clear_form(self):
        self.sal_id.delete(0, tk.END)
        self.pdf_path.delete(0, tk.END)