-- update weighted average score for all users

DROP PROCEDURE IF EXISTS ComputeAverageWeightedScoreForUsers;
DELIMITER ..

CREATE PROCEDURE ComputeAverageWeightedScoreForUsers()
BEGIN

    -- create indexes if missing to improve performance
    /* CREATE INDEX idx_corrections_user_id ON corrections(user_id);
    CREATE INDEX idx_corrections_project_id ON corrections(project_id);
    CREATE INDEX idx_projects_id ON projects(id); */

    -- declare variables for user loop
    DECLARE current_id INT;
    DECLARE avg_score FLOAT;
    DECLARE done INT DEFAULT FALSE;
    DECLARE cur CURSOR FOR SELECT id FROM users;
    DECLARE CONTINUE HANDLER FOR NOT FOUND SET done = TRUE;

    -- iterate over users and update average score
    OPEN cur;
    read_loop: LOOP
        FETCH cur INTO current_id;
        IF done THEN
            LEAVE read_loop;
        END IF;

        SET avg_score = (
            SELECT SUM(c.score * p.weight) / SUM(p.weight)
            FROM projects p
            INNER JOIN corrections c ON p.id = c.project_id
            WHERE c.user_id = current_id
        );

        UPDATE users SET average_score = avg_score 
        WHERE id = current_id;
    END LOOP;
    CLOSE cur;
END ..
DELIMITER ;
