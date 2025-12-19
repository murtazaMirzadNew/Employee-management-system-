-- Create EMPLOYEES table
CREATE TABLE employees (
    emp_id NUMBER PRIMARY KEY,
    first_name VARCHAR2(50) NOT NULL,
    last_name VARCHAR2(50) NOT NULL,
    email VARCHAR2(100) UNIQUE,
    phone VARCHAR2(20),
    hire_date DATE DEFAULT SYSDATE,
    job_title VARCHAR2(50),
    department VARCHAR2(50),
    salary NUMBER(10,2),
    status VARCHAR2(10) DEFAULT 'Active' CHECK (status IN ('Active', 'Inactive'))
);

-- Create ATTENDANCE table
CREATE TABLE attendance (
    att_id NUMBER PRIMARY KEY,
    emp_id NUMBER NOT NULL,
    att_date DATE DEFAULT SYSDATE,
    check_in TIMESTAMP,
    check_out TIMESTAMP,
    FOREIGN KEY (emp_id) REFERENCES employees(emp_id)
);

-- Create SALARY table
CREATE TABLE salary (
    sal_id NUMBER PRIMARY KEY,
    emp_id NUMBER NOT NULL,
    month_year VARCHAR2(7), -- e.g., '2025-12'
    base_salary NUMBER(10,2),
    bonus NUMBER(10,2) DEFAULT 0,
    deductions NUMBER(10,2) DEFAULT 0,
    net_salary NUMBER(10,2),
    FOREIGN KEY (emp_id) REFERENCES employees(emp_id)
);

-- Create PAYSILP table
CREATE TABLE payslip (
    payslip_id NUMBER PRIMARY KEY,
    sal_id NUMBER NOT NULL,
    generated_date DATE DEFAULT SYSDATE,
    pdf_path VARCHAR2(255),
    FOREIGN KEY (sal_id) REFERENCES salary(sal_id)
);