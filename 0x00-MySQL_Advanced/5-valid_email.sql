-- Script to create a trigger that resets 'valid_email' to 0 only when the email has been changed.

-- Drop the trigger if it already exists
DROP TRIGGER IF EXISTS reset_valid_email_on_change;

-- Create the trigger for resetting 'valid_email'
CREATE TRIGGER reset_valid_email_on_change
BEFORE UPDATE ON users
FOR EACH ROW
BEGIN
    -- Reset 'valid_email' to 0 if the email has been changed
    IF NEW.email <> OLD.email THEN
        SET NEW.valid_email = 0;
    END IF;
END;
