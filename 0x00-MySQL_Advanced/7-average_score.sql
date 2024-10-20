-- Script to create the ComputeAverageScoreForUser stored procedure

-- Drop the procedure if it already exists
DROP PROCEDURE IF EXISTS ComputeAverageScoreForUser;

-- Create the ComputeAverageScoreForUser procedure
DELIMITER $$

CREATE PROCEDURE ComputeAverageScoreForUser(
    IN user_id INT
)
BEGIN
    DECLARE avg_score FLOAT;

    -- Compute the average score for the user
    SELECT AVG(score) INTO avg_score
    FROM corrections
    WHERE user_id = user_id;

    -- Update the user's average_score in the users table
    UPDATE users
    SET average_score = IFNULL(avg_score, 0)
    WHERE id = user_id;

END $$

DELIMITER ;
