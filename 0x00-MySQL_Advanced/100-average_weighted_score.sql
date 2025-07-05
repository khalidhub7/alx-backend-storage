-- update user's weighted average score
DROP PROCEDURE IF EXISTS ComputeAverageWeightedScoreForUser;
DELIMITER ..

CREATE PROCEDURE ComputeAverageWeightedScoreForUser(IN userid INT)
BEGIN
    DECLARE avg_score FLOAT;
    SET avg_score = (
        SELECT (SUM(c.score * p.weight) / SUM(p.weight))
        FROM projects p
        INNER JOIN corrections c ON p.id = c.project_id
        WHERE c.user_id = userid
    );
    UPDATE users SET average_score = avg_score
    WHERE id = userid;
END ..
DELIMITER ;
