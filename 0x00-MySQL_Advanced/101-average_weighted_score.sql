-- Average weighted score 
-- SQL script that creates a stored procedure ComputeAverageWeightedScoreForUsers

DELIMITER //

CREATE FUNCTION GetAverage(user_id INT)
RETURNS FLOAT
DETERMINISTIC
BEGIN
    RETURN (SELECT
            SUM(corrections.score * projects.weight) / SUM(projects.weight)
            FROM corrections
            INNER JOIN projects
            ON projects.id = corrections.project_id
            WHERE corrections.user_id = user_id);
END //

DELIMITER ;

DELIMITER //




CREATE PROCEDURE ComputeAverageWeightedScoreForUsers ()
BEGIN
    UPDATE users SET average_score = (SELECT GetAverage(id)); 
END //

DELIMITER ;
