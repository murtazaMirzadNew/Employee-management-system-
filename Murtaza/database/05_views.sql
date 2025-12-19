-- View: Active Employees
CREATE OR REPLACE VIEW active_employees AS
SELECT emp_id, first_name, last_name, email, job_title, department, salary
FROM employees
WHERE status = 'Active';

-- View: Monthly Salary Summary
CREATE OR REPLACE VIEW monthly_salary_summary AS
SELECT e.emp_id, e.first_name, e.last_name, s.month_year, s.net_salary
FROM employees e
JOIN salary s ON e.emp_id = s.emp_id;

-- View: Attendance Report
CREATE OR REPLACE VIEW attendance_report AS
SELECT e.emp_id, e.first_name, e.last_name, a.att_date, a.check_in, a.check_out,
       ROUND((CAST(a.check_out AS DATE) - CAST(a.check_in AS DATE)) * 24, 2) AS hours_worked
FROM employees e
JOIN attendance a ON e.emp_id = a.emp_id
WHERE a.check_in IS NOT NULL AND a.check_out IS NOT NULL;