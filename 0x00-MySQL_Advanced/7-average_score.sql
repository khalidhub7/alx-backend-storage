-- Average score 
-- SQL script that creates a stored procedure
DELIMITER //

CREATE PROCEDURE ComputeAverageScoreForUser(IN user_id INT)
BEGIN
    SET @user_avg = (SELECT AVG(score) FROM corrections WHERE corrections.user_id=user_id);
    UPDATE users SET average_score=@user_avg WHERE id=user_id;
END//
DELIMITER ;
