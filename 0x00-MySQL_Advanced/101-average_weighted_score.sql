-- Drop the procedure if it already exists
DROP PROCEDURE IF EXISTS ComputeAverageWeightedScoreForUsers;
DELIMITER $$

-- Create the ComputeAverageWeightedScoreForUsers procedure
CREATE PROCEDURE ComputeAverageWeightedScoreForUsers()
BEGIN
    DECLARE finished INT DEFAULT 0;
    DECLARE current_user_id INT;

    -- Declare a cursor to iterate through all users
    DECLARE user_cursor CURSOR FOR
        SELECT id FROM users;

    -- Declare a handler to detect the end of the user list
    DECLARE CONTINUE HANDLER FOR NOT FOUND SET finished = 1;

    -- Open the cursor
    OPEN user_cursor;

    -- Start the loop to go through each user
    user_loop: LOOP
        -- Fetch the current user ID
        FETCH user_cursor INTO current_user_id;

        -- Exit the loop if there are no more users
        IF finished = 1 THEN 
            LEAVE user_loop; 
        END IF;

        -- Call ComputeAverageWeightedScoreForUser for the current user
        CALL ComputeAverageWeightedScoreForUser(current_user_id);
    END LOOP;

    -- Close the cursor
    CLOSE user_cursor;
END
$$
DELIMITER ;

-- Reset DELIMITER back to the default
DELIMITER ;
