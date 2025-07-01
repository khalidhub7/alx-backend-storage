-- add new correction row
DELIMITER ..

CREATE PROCEDURE AddBonus(
    IN user_id INT, IN project_name VARCHAR(255), IN score INT
)
BEGIN
    DECLARE project_id INT;

    -- get project_id if project exists
    SELECT id INTO project_id FROM projects 
    WHERE name = project_name LIMIT 1;

    IF project_id IS NULL THEN
        -- insert new project if not found
        INSERT INTO projects (name) VALUES (project_name);

        -- retrieve last inserted project_id
        SET project_id = LAST_INSERT_ID();
    END IF;

    -- insert correction with the score
    INSERT INTO corrections (user_id, project_id, score)
    VALUES (user_id, project_id, score);

END
..

DELIMITER ;
