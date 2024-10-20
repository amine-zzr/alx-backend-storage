-- Drop the procedure if it already exists
DROP PROCEDURE IF EXISTS ComputeAverageWeightedScoreForUser;
DELIMITER $$

-- Create the ComputeAverageWeightedScoreForUser procedure
CREATE PROCEDURE ComputeAverageWeightedScoreForUser(
    IN user_id INT
)
BEGIN
    DECLARE weighted_avg_score FLOAT;
    DECLARE total_weight INT;

    -- Calculate the total weighted score for the user
    SET weighted_avg_score = (SELECT SUM(C.score * P.weight)
                              FROM corrections C
                              JOIN projects P ON C.project_id = P.id
                              WHERE C.user_id = user_id);

    -- Calculate the total weight of the projects the user has corrections for
    SET total_weight = (SELECT SUM(P.weight)
                        FROM corrections C
                        JOIN projects P ON C.project_id = P.id
                        WHERE C.user_id = user_id);

    -- Calculate the weighted average score by dividing the total weighted score by total weight
    -- If the total weight is 0 (just in case), set the weighted average score to 0
    IF total_weight > 0 THEN
        SET weighted_avg_score = weighted_avg_score / total_weight;
    ELSE
        SET weighted_avg_score = 0;
    END IF;

    -- Update the user's average_score in the users table
    UPDATE users 
    SET average_score = weighted_avg_score 
    WHERE id = user_id;
END
$$
DELIMITER ;

-- Reset DELIMITER back to the default
DELIMITER ;
