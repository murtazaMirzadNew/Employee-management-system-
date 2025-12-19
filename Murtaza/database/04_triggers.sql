-- Trigger: Auto-set net_salary on insert/update in salary
CREATE OR REPLACE TRIGGER trg_calculate_net_salary
BEFORE INSERT OR UPDATE OF base_salary, bonus, deductions ON salary
FOR EACH ROW
BEGIN
    :NEW.net_salary := calculate_net_salary(:NEW.base_salary, :NEW.bonus, :NEW.deductions);
END;
/

-- Trigger: Prevent deletion of active employees
CREATE OR REPLACE TRIGGER trg_prevent_active_delete
BEFORE DELETE ON employees
FOR EACH ROW
BEGIN
    IF :OLD.status = 'Active' THEN
        RAISE_APPLICATION_ERROR(-20001, 'Cannot delete active employee. Set status to Inactive first.');
    END IF;
END;
/