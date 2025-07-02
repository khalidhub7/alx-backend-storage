-- students needing a meeting

-- returns 1 if no recent meeting
DELIMITER ..
CREATE FUNCTION is_met_recently(last_meeting DATE)
RETURNS BOOLEAN DETERMINISTIC
BEGIN
    IF last_meeting IS NULL 
    OR last_meeting < NOW() - INTERVAL 1 MONTH 
    THEN
        RETURN 1;
    END IF;

    RETURN 0;
END ..
DELIMITER ;

-- view of students with low score and no recent meeting
DROP VIEW IF EXISTS need_meeting;
CREATE VIEW need_meeting AS
SELECT name FROM students
WHERE score < 80 AND is_met_recently(last_meeting);
