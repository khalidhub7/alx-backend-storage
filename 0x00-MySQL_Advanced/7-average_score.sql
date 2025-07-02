-- updates user's average score

DROP PROCEDURE IF EXISTS ComputeAverageScoreForUser;

DELIMITER ..
CREATE PROCEDURE ComputeAverageScoreForUser(IN userid INT)
BEGIN
    UPDATE users
    SET average_score = (
        SELECT AVG(score) FROM corrections WHERE user_id = userid
        )
    WHERE id = userid;
END ..
DELIMITER ;
