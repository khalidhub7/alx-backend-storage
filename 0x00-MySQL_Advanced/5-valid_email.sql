-- trigger if an email changed
DELIMITER //
DROP TRIGGER IF EXISTS reset_email //
CREATE TRIGGER reset_email
BEFORE UPDATE ON users
FOR EACH ROW
BEGIN
    IF NEW.email <> OLD.email THEN
        SET NEW.valid_email = 0;
    ELSE
        SET NEW.valid_email = 1;
    END IF;
END;
//
DELIMITER ;
