-- add new correction row
DELIMITER ;
DROP PROCEDURE IF EXISTS AddBonus;

DELIMITER ..
CREATE PROCEDURE AddBonus(
    IN user_id INT, IN project_name VARCHAR(255), IN score INT
)
BEGIN
    DECLARE project_id INT;

    SET project_id = (
        SELECT id FROM projects WHERE name = project_name LIMIT 1
    );

    IF project_id IS NULL THEN
        INSERT INTO projects (name) VALUES (project_name);
        SET project_id = LAST_INSERT_ID();
    END IF;

    INSERT INTO corrections (user_id, project_id, score)
    VALUES (user_id, project_id, score);
END
..
DELIMITER ;
