-- store the average weighted score for a student
DROP PROCEDURE IF EXISTS ComputeAverageWeightedScoreForUser;
DELIMITER ..

CREATE PROCEDURE ComputeAverageWeightedScoreForUser(IN userid INT)
BEGIN
    UPDATE users
    SET average_score = (
        SELECT COALESCE(SUM(c.score * p.weight) / NULLIF(SUM(p.weight), 0), 0)
        FROM corrections c
        JOIN projects p ON c.project_id = p.id
        WHERE c.user_id = userid
    )
    WHERE id = userid;
END ..

DELIMITER ;
