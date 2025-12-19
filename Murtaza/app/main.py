import tkinter as tk
from tkinter import ttk
from employee_ui import EmployeeUI
from Salary_ui import SalaryUI          # ✅ lowercase 's'
from attendance_ui import AttendanceUI
from payslip_ui import PayslipUI

class MainApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Employee Management System")
        self.root.geometry("800x600")
        self.root.configure(bg="#F5F5F5")

        # Header
        header_frame = tk.Frame(root, bg="#2C3E50", pady=20)
        header_frame.pack(fill="x")
        tk.Label(
            header_frame,
            text="Employee Management System",
            font=("Arial", 18, "bold"),
            fg="white",
            bg="#2C3E50"
        ).pack()

        # Button Frame at the BOTTOM
        button_frame = tk.Frame(root, bg="#F5F5F5")
        button_frame.pack(side="bottom", pady=40)

        # Button style
        btn_style = {
            "bg": "#3498DB",
            "fg": "white",
            "font": ("Arial", 11, "bold"),
            "width": 18,
            "height": 2,
            "relief": "raised",
            "bd": 2,
            "activebackground": "#2980B9",
            "activeforeground": "white"
        }

        # Buttons - all centered in one row
        tk.Button(button_frame, text="Employees", command=self.show_employee_ui, **btn_style).pack(side="left", padx=10)
        tk.Button(button_frame, text="Salary", command=self.show_salary_ui, **btn_style).pack(side="left", padx=10)  # ✅ fixed typo
        tk.Button(button_frame, text="Attendance", command=self.show_attendance_ui, **btn_style).pack(side="left", padx=10)
        tk.Button(button_frame, text="Payslips", command=self.show_payslip_ui, **btn_style).pack(side="left", padx=10)

        self.content_frame = None

    def show_employee_ui(self):
        self._switch_to(EmployeeUI)

    def show_salary_ui(self):
        self._switch_to(SalaryUI)

    def show_attendance_ui(self):
        self._switch_to(AttendanceUI)

    def show_payslip_ui(self):
        self._switch_to(PayslipUI)

    def _switch_to(self, ui_class):
        # Clear entire window
        for widget in self.root.winfo_children():
            widget.destroy()

        # Back button
        top_frame = tk.Frame(self.root, bg="#F5F5F5")
        top_frame.pack(fill="x", padx=10, pady=10)
        tk.Button(
            top_frame,
            text="← Back",
            command=self.reload_main,
            bg="#E74C3C",
            fg="white",
            font=("Arial", 10, "bold"),
            relief="flat",
            activebackground="#C0392B",
            activeforeground="white"
        ).pack(anchor="w")

        # Content area
        content = tk.Frame(self.root, bg="#F5F5F5")
        content.pack(fill="both", expand=True, padx=20, pady=10)

        # Load UI
        ui_class(content, self)

    def reload_main(self):
        for widget in self.root.winfo_children():
            widget.destroy()
        MainApp(self.root)


if __name__ == "__main__":
    root = tk.Tk()
    app = MainApp(root)
    root.mainloop()