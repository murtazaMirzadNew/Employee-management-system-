-- Procedure: Add new employee
CREATE OR REPLACE PROCEDURE add_employee(
    p_first_name IN VARCHAR2,
    p_last_name IN VARCHAR2,
    p_email IN VARCHAR2,
    p_phone IN VARCHAR2,
    p_job_title IN VARCHAR2,
    p_department IN VARCHAR2,
    p_salary IN NUMBER
) IS
BEGIN
    INSERT INTO employees (emp_id, first_name, last_name, email, phone, hire_date, job_title, department, salary, status)
    VALUES (emp_seq.NEXTVAL, p_first_name, p_last_name, p_email, p_phone, SYSDATE, p_job_title, p_department, p_salary, 'Active');
    COMMIT;
END add_employee;
/

-- Procedure: Generate Payslip
CREATE OR REPLACE PROCEDURE generate_payslip(
    p_sal_id IN NUMBER,
    p_pdf_path IN VARCHAR2
) IS
BEGIN
    INSERT INTO payslip (payslip_id, sal_id, generated_date, pdf_path)
    VALUES (payslip_seq.NEXTVAL, p_sal_id, SYSDATE, p_pdf_path);
    COMMIT;
END generate_payslip;
/

-- Backup & Recovery Script (Run manually or via scheduler)
-- BACKUP: Export schema
-- Note: This is a conceptual script. Actual backup requires OS-level tools like expdp.
-- You can schedule this via Oracle Scheduler or cron.

-- Example: Export command (run in OS terminal, not SQL*Plus)
-- expdp c##khan1/123 DIRECTORY=DATA_PUMP_DIR DUMPFILE=emp_backup_%U.dmp LOGFILE=emp_backup.log SCHEMAS=c##khan1

-- RECOVERY: Import schema
-- impdp c##khan1/123 DIRECTORY=DATA_PUMP_DIR DUMPFILE=emp_backup_01.dmp LOGFILE=emp_restore.log