-- This script creates a stored procedure that adds a bonus to a user for a project.
-- The procedure first checks if the project exists in the projects table.
-- If it does not exist, it creates a new project and retrieves its id.
DELIMITER //
CREATE PROCEDURE IF NOT EXISTS addBonus (user_id INT, project_name VARCHAR(255), score INT)
BEGIN
    DECLARE project_id INT;

    SELECT id FROM projects WHERE name = project_name;
    IF project_id IS NULL THEN
        INSERT INTO projects (name) VALUES (project_name);
        SET project_id = LAST_INSERT_ID();
    END IF;

    INSERT INTO corrections(user_id, project_id, score) VALUES (user_id, project_id, score);
END //
DELIMITER ;
