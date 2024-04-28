-- This script creates a stored procedure that adds a bonus to a user for a project.
-- The procedure first checks if the project exists in the projects table.
-- If it does not exist, it creates a new project and retrieves its id.
DELIMITER //
DROP PROCEDURE IF EXISTS AddBonus;
CREATE PROCEDURE addBonus (user_id INT, project_name VARCHAR(255), score INT)
BEGIN
    DECLARE project_id INT;

    SELECT id FROM projects WHERE name = project_name INTO project_id;
    IF project_id IS NULL THEN
        INSERT INTO projects (name) VALUES (project_name);
        SELECT LAST_INSERT_ID() INTO project_id;
    END IF;
    SELECT id FROM projects WHERE name = project_name INTO project_id;
    INSERT INTO corrections(user_id, project_id, score) VALUES (user_id, project_id, score);
END //
DELIMITER ;
