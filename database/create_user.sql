/* ******************************************
   Drop and recreate the fitness_app_user
******************************************** */

-- Drop user if exists
DROP USER IF EXISTS 'fitness_app_user'@'%';

-- Create user with password
CREATE USER 'fitness_app_user'@'%' IDENTIFIED BY 'StrongPassword123!';

-- Grant privileges ONLY on the fitness_app database
GRANT SELECT, INSERT, UPDATE, DELETE
ON `fitness_app`.*
TO 'fitness_app_user'@'%';

-- Optional: If you want the user to be able to create tables
-- GRANT CREATE, ALTER, DROP
-- ON `fitness_app`.*
-- TO 'fitness_app_user'@'%';

-- Resource limits (0 = unlimited)
ALTER USER 'fitness_app_user'@'%'
  REQUIRE NONE
  WITH
    MAX_QUERIES_PER_HOUR 0
    MAX_CONNECTIONS_PER_HOUR 0
    MAX_UPDATES_PER_HOUR 0
    MAX_USER_CONNECTIONS 0;

FLUSH PRIVILEGES;

