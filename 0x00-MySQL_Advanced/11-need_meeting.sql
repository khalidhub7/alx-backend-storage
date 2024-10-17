-- No table for a meeting 
-- SQL script that creates a view need_meeting
CREATE VIEW need_meeting AS
SELECT name FROM students
WHERE score < 80
AND (last_meeting < DATE_SUB(CURDATE(), INTERVAL 1 MONTH) OR last_meeting IS NULL) 
