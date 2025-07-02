-- safe divide, returns 0 if b is 0
DELIMITER ..
CREATE FUNCTION SafeDiv(IN a INT, IN b INT)
DETERMINISTIC
RETURNS FLOAT
BEGIN
    IF b = 0 THEN 
        RETURN 0;
    END IF;
    RETURN a / b;
END ..
DELIMITER ;
