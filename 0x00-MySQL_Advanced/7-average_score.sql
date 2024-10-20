-- implement a stored procedure that computes and stores the average weighted score for a student

-- Drop the procedure if it already exists
DROP PROCEDURE IF EXISTS ComputeAverageScoreForUser;
DELIMITER $$

-- Create the ComputeAverageScoreForUser procedure
CREATE PROCEDURE ComputeAverageScoreForUser(
    IN user_id INT
)
BEGIN
    DECLARE avg_score FLOAT;
    SET avg_score = (SELECT AVG(score) FROM corrections AS C WHERE C.user_id=user_id);
    UPDATE users SET average_score = avg_score WHERE id=user_id;
END
$$
DELIMITER ;
