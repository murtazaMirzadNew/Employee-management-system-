-- Function to calculate net salary
CREATE OR REPLACE FUNCTION calculate_net_salary(
    p_base IN NUMBER,
    p_bonus IN NUMBER DEFAULT 0,
    p_deductions IN NUMBER DEFAULT 0
) RETURN NUMBER IS
BEGIN
    RETURN p_base + p_bonus - p_deductions;
END calculate_net_salary;
/

-- Function to get employee full name
CREATE OR REPLACE FUNCTION get_employee_fullname(p_emp_id IN NUMBER)
RETURN VARCHAR2 IS
    v_name VARCHAR2(100);
BEGIN
    SELECT first_name || ' ' || last_name INTO v_name
    FROM employees WHERE emp_id = p_emp_id;
    RETURN v_name;
EXCEPTION
    WHEN NO_DATA_FOUND THEN
        RETURN 'Unknown Employee';
END get_employee_fullname;
/