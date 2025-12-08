
-- Create tables for the fitness_app database.


USE `fitness_app`;


-- USERS TABLE

DROP TABLE IF EXISTS `users`;

CREATE TABLE `users` (
  `id` INT AUTO_INCREMENT PRIMARY KEY,
  `first_name` VARCHAR(25) NOT NULL,
  `middle_name` VARCHAR(25),
  `last_name` VARCHAR(25) NOT NULL,
  `birthday` VARCHAR(25),
  `gender` CHAR(1)
);


-- WORKOUTS TABLE

DROP TABLE IF EXISTS `workouts`;

CREATE TABLE `workouts` (
  `id` INT AUTO_INCREMENT PRIMARY KEY,
  `title` VARCHAR(100) NOT NULL,
  `description` VARCHAR(250) NOT NULL
);


-- EXERCISES TABLE

DROP TABLE IF EXISTS `exercises`;

CREATE TABLE `exercises` (
  `id` INT AUTO_INCREMENT PRIMARY KEY,
  `name` VARCHAR(100) NOT NULL,
  `instructions` VARCHAR(500)
);


-- WORKOUT_EXERCISES JOIN TABLE

DROP TABLE IF EXISTS `workout_exercises`;

CREATE TABLE `workout_exercises` (
  `workout_id` INT NOT NULL,
  `exercise_id` INT NOT NULL,

  PRIMARY KEY (`workout_id`, `exercise_id`),

  FOREIGN KEY (`workout_id`) REFERENCES workouts(id)
    ON DELETE CASCADE
    ON UPDATE CASCADE,

  FOREIGN KEY (`exercise_id`) REFERENCES exercises(id)
    ON DELETE CASCADE
    ON UPDATE CASCADE
);


-- USER COMPLETED WORKOUTS

DROP TABLE IF EXISTS `user_completed_workouts`;

CREATE TABLE `user_completed_workouts` (
  `id` INT AUTO_INCREMENT PRIMARY KEY,
  `user_id` INT NOT NULL,
  `workout_id` INT NOT NULL,
  `date_completed` DATE NOT NULL,

  FOREIGN KEY (`user_id`) REFERENCES users(id)
    ON DELETE CASCADE,

  FOREIGN KEY (`workout_id`) REFERENCES workouts(id)
    ON DELETE CASCADE
);

-- USER FAVORITE WORKOUTS

DROP TABLE IF EXISTS `user_favorite_workouts`;

CREATE TABLE `user_favorite_workouts` (
  `user_id` INT NOT NULL,
  `workout_id` INT NOT NULL,

  PRIMARY KEY (`user_id`, `workout_id`),

  FOREIGN KEY (`user_id`) REFERENCES users(id)
    ON DELETE CASCADE,

  FOREIGN KEY (`workout_id`) REFERENCES workouts(id)
    ON DELETE CASCADE
);
