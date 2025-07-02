-- updates user's average score

DROP PROCEDURE IF EXISTS ComputeAverageScoreForUser;

DELIMITER ..
CREATE PROCEDURE ComputeAverageScoreForUser(IN userid INT)
BEGIN
    DECLARE avg_score FLOAT;

    SET avg_score = (
        SELECT AVG(score) FROM user_id WHERE user_id = userid
    );

    UPDATE users
    SET average_score = avg_score
    WHERE id = user_id;
END ..
DELIMITER ;
