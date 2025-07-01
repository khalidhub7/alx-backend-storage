-- Add new row correction
DELIMITER ..

CREATE PROCEDURE AddBonus(
    IN user_id INT, 
    IN project_name VARCHAR(255), 
    IN score INT
)
BEGIN
    DECLARE project_id INT;

    DECLARE CONTINUE HANDLER FOR NOT FOUND
    BEGIN
        -- Insert project if it doesn't exist
        INSERT INTO projects (name) 
        VALUES (project_name);

        -- Get the project ID
        SELECT id 
        INTO project_id 
        FROM projects 
        WHERE name = project_name;

        -- Insert correction
        INSERT INTO corrections (user_id, project_id) 
        VALUES (user_id, project_id);
    END;

    -- Get the project ID
    SELECT id 
    INTO project_id 
    FROM projects 
    WHERE name = project_name;

    -- Insert correction with score
    INSERT INTO corrections (user_id, project_id, score)
    VALUES (user_id, project_id, score);

END
..

DELIMITER ;
