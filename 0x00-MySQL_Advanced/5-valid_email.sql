-- Email validation to sent 
-- SQL script that creates a trigger 
DELIMITER //

CREATE TRIGGER check_before_update
BEFORE UPDATE ON users
FOR EACH ROW
SET NEW.valid_email = IF(OLD.email <> NEW.email, 0, NEW.valid_email);

//

DELIMITER ;
