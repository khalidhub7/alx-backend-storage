-- reset valid_email if email changes
DELIMITER ..

CREATE TRIGGER clear_email_valid
BEFORE UPDATE ON users
FOR EACH ROW
BEGIN
    IF NEW.email != OLD.email THEN
        UPDATE users
        SET valid_email = 0
        WHERE id = NEW.id;
    END IF;
END ..
DELIMITER ;
