-- Drop and recreate the fitness_app_user

DROP USER IF EXISTS 'fitness_app_user'@'%';

CREATE USER 'fitness_app_user'@'%';

ALTER USER 'fitness_app_user'@'%'
  REQUIRE NONE
  WITH
    MAX_QUERIES_PER_HOUR 0
    MAX_CONNECTIONS_PER_HOUR 0
    MAX_UPDATES_PER_HOUR 0
    MAX_USER_CONNECTIONS 0;

GRANT SELECT, INSERT, UPDATE, DELETE
ON `fitness_app`.*
TO 'fitness_app_user'@'%';

FLUSH PRIVILEGES;
