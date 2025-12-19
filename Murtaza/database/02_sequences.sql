-- Sequences for auto-increment
CREATE SEQUENCE emp_seq START WITH 1 INCREMENT BY 1;
CREATE SEQUENCE att_seq START WITH 1 INCREMENT BY 1;
CREATE SEQUENCE sal_seq START WITH 1 INCREMENT BY 1;
CREATE SEQUENCE payslip_seq START WITH 1 INCREMENT BY 1;

-- Indexes for performance
CREATE INDEX idx_emp_dept ON employees(department);
CREATE INDEX idx_att_emp ON attendance(emp_id);
CREATE INDEX idx_sal_emp_month ON salary(emp_id, month_year);