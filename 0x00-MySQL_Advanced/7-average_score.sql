-- Drop the procedure if it already exists
DROP PROCEDURE IF EXISTS ComputeAverageScoreForUser;
DELIMITER $$

-- Create the ComputeAverageScoreForUser procedure
CREATE PROCEDURE ComputeAverageScoreForUser(
    IN user_id INT
)
BEGIN
    DECLARE avg_score FLOAT;

    -- Calculate the average score for the given user_id
    SET avg_score = (SELECT IFNULL(AVG(score), 0) 
                     FROM corrections 
                     WHERE user_id = user_id);

    -- Update the user's average_score in the users table
    UPDATE users 
    SET average_score = avg_score 
    WHERE id = user_id;
END
$$
DELIMITER ;

-- Reset DELIMITER back to the default
DELIMITER ;
