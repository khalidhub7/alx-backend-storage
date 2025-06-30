-- new correction
DELIMITER ..

CREATE PROCEDURE AddBonus(IN user_id INT, IN project_name VARCHAR, IN score INT)
BEGIN
    DECLARE project_id INT;
    DECLARE new_score INT;
    SET new_score = score;

    DECLARE CONTINUE HANDLER FOR NOT FOUND
    BEGIN
        INSERT INTO projects (name) VALUES (project_name);
        SELECT id INTO project_id FROM projects WHERE name = project_name;
        INSERT INTO corrections (user_id, project_id) VALUES (user_id, project_id);
    END;

    SELECT id INTO project_id FROM projects WHERE name = project_name;

    UPDATE corrections c
    SET c.score = new_score
    WHERE c.user_id = user_id AND c.project_id = project_id;
END
..

DELIMITER ;
