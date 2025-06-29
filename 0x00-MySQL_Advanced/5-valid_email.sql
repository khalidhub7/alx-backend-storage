-- reset valid_email if email changes
DELIMITER ..

CREATE TRIGGER clear_email_valid
BEFORE UPDATE ON users
FOR EACH ROW
BEGIN
    IF NEW.email != OLD.email THEN
        SET NEW.valid_email = 0;
    END IF;
END;
..
DELIMITER ;
