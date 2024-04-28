-- This script calculates the average score of each student.
-- The output should be a table with two columns: student_id and average_score.
DELIMITER //
DROP PROCEDURE IF EXISTS ComputeAverageScoreForUser;
CREATE PROCEDURE ComputeAverageScoreForUser (user_id INT)
BEGIN
    DECLARE avg_score DECIMAL(10, 2) DEFAULT 0;
    SELECT AVG(score) INTO avg_score FROM corrections WHERE corrections.user_id = user_id;
    UPDATE users SET users.average_score = avg_score WHERE users.id = user_id;
END //
DELIMITER ;
