
 USE `fitness_app`;

-- Users
INSERT INTO users (first_name, middle_name, last_name, birthday, gender)
VALUES ('Olivia', 'M', 'Clontz', '2007-06-25', 'F');
SET @olivia = LAST_INSERT_ID();

INSERT INTO users (first_name, last_name, birthday, gender)
VALUES ('Jose', 'Carballov', '2009-05-21', 'M');
SET @jose = LAST_INSERT_ID();

-- Workouts
INSERT INTO workouts (title, description)
VALUES ('Full Body Beginner Workout', 'A simple full-body workout for beginners.');
SET @fullbody = LAST_INSERT_ID();

INSERT INTO workouts (title, description)
VALUES ('Core Strength Builder', 'Strengthen the abdominal and lower back muscles.');
SET @core = LAST_INSERT_ID();

-- Exercises
INSERT INTO exercises (name, instructions)
VALUES ('Push-Ups', 'Keep your back straight and lower yourself to the floor.');
SET @pushups = LAST_INSERT_ID();

INSERT INTO exercises (name, instructions)
VALUES ('Squats', 'Stand with feet shoulder-width apart, bend at the knees.');
SET @squats = LAST_INSERT_ID();

INSERT INTO exercises (name, instructions)
VALUES ('Plank', 'Hold plank position for 30 seconds.');
SET @plank = LAST_INSERT_ID();

-- Assign exercises to workouts
INSERT INTO workout_exercises (workout_id, exercise_id)
VALUES (@fullbody, @pushups),
       (@fullbody, @squats),
       (@core, @plank);

-- User completes workouts
INSERT INTO user_completed_workouts (user_id, workout_id, date_completed)
VALUES (@olivia, @fullbody, '2025-01-15'),
       (@jose, @core, '2025-01-16');

-- User favorites workouts
INSERT INTO user_favorite_workouts (user_id, workout_id)
VALUES (@olivia, @core),
       (@jose, @fullbody);
