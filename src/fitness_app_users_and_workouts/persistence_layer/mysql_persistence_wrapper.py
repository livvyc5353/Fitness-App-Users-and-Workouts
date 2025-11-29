"""Defines the MySQLPersistenceWrapper class."""

import json
import inspect
from enum import Enum
from typing import List, Optional

from mysql import connector
from mysql.connector.pooling import MySQLConnectionPool

from fitness_app_users_and_workouts.application_base import ApplicationBase
import inspect
from typing import List
from fitness_app_users_and_workouts.infrastructure_layer.user import User
from fitness_app_users_and_workouts.infrastructure_layer.workout import Workout
from fitness_app_users_and_workouts.infrastructure_layer.exercise import Exercise



class MySQLPersistenceWrapper(ApplicationBase):
    """Handles MySQL operations for the Fitness App."""

    def __init__(self, config: dict) -> None:
        """Initializes MySQL wrapper."""
        self._config_dict = config
        self.META = config["meta"]
        self.DATABASE = config["database"]

        super().__init__(
            subclass_name=self.__class__.__name__,
            logfile_prefix_name=self.META["log_prefix"]
        )

        # Database Configuration
        self.DB_CONFIG = {}
        self.DB_CONFIG["database"] = self.DATABASE["connection"]["config"]["database"]
        self.DB_CONFIG["user"] = self.DATABASE["connection"]["config"]["user"]
        self.DB_CONFIG["host"] = self.DATABASE["connection"]["config"]["host"]
        self.DB_CONFIG["port"] = self.DATABASE["connection"]["config"]["port"]
        self.DB_CONFIG["password"] = self.DATABASE["connection"]["config"].get(
            "password", ""
        )

        self._logger.log_debug(f"DB Connection Config Dict: {self.DB_CONFIG}")

        # Database Connection Pool
        self._connection_pool = self._initialize_database_connection_pool(
            self.DB_CONFIG
        )

        # User Column ENUMS
        self.UserColumns = Enum(
            "UserColumns",
            [
                ("id", 0),
                ("first_name", 1),
                ("middle_name", 2),
                ("last_name", 3),
                ("birthday", 4),
                ("gender", 5),
            ],
        )

        # Workout Column ENUMS
        self.WorkoutColumns = Enum(
            "WorkoutColumns",
            [
                ("id", 0),
                ("title", 1),
                ("description", 2),
            ],
        )

        # ============================================================
        #                          SQL QUERY CONSTANTS
        # ============================================================

        # All users
        self.SELECT_ALL_USERS = (
            "SELECT id, first_name, middle_name, last_name, birthday, gender "
            "FROM users"
        )

        # All workouts
        self.SELECT_ALL_WORKOUTS = (
            "SELECT id, title, description FROM workouts"
        )

        # All exercises
        self.SELECT_ALL_EXERCISES = (
            "SELECT id, name, instructions FROM exercises"
        )

        # Workouts completed by user (with date)
        self.SELECT_USER_COMPLETED = (
            "SELECT w.id, w.title, w.description, c.date_completed "
            "FROM workouts w "
            "JOIN user_completed_workouts c ON c.workout_id = w.id "
            "WHERE c.user_id = %s"
        )

        # Favorite workouts for user
        self.SELECT_USER_FAVORITES = (
            "SELECT w.id, w.title, w.description "
            "FROM workouts w "
            "JOIN user_favorite_workouts f ON f.workout_id = w.id "
            "WHERE f.user_id = %s"
        )

        # Exercises for a workout
        self.SELECT_WORKOUT_EXERCISES = (
            "SELECT e.id, e.name, e.instructions "
            "FROM exercises e "
            "JOIN workout_exercises we ON we.exercise_id = e.id "
            "WHERE we.workout_id = %s"
        )

    # ============================================================
    # PUBLIC SELECTION METHODS
    # ============================================================

    def select_all_users(self) -> List[User]:
        """Returns all users as User objects (without workouts attached)."""
        cursor = None
        results = None
        user_list: List[User] = []

        try:
            connection = self._connection_pool.get_connection()
            with connection:
                cursor = connection.cursor()
                with cursor:
                    cursor.execute(self.SELECT_ALL_USERS)
                    results = cursor.fetchall()

            user_list = self._populate_user_objects(results)
            return user_list

        except Exception as e:
            self._logger.log_error(
                f"{inspect.currentframe().f_code.co_name}: {e}"
            )
            return []

    def select_all_workouts(self) -> List[Workout]:
        """Returns a list of all workout objects, each with exercises."""
        cursor = None
        results = None
        workout_list: List[Workout] = []
        try:
            connection = self._connection_pool.get_connection()
            with connection:
                cursor = connection.cursor()
                with cursor:
                    cursor.execute(self.SELECT_ALL_WORKOUTS)
                    results = cursor.fetchall()

            workout_list = self._populate_workout_objects(results)

            # Populate exercises for each workout
            for w in workout_list:
                w.exercises = self.select_workout_exercises(w.id)

            return workout_list

        except Exception as e:
            self._logger.log_error(
                f"{inspect.currentframe().f_code.co_name}: {e}"
            )
            return []

    def select_all_exercises(self) -> List[Exercise]:
        """Return all exercises."""
        cursor = None
        results = None
        exercises: List[Exercise] = []
        try:
            connection = self._connection_pool.get_connection()
            with connection:
                cursor = connection.cursor()
                with cursor:
                    cursor.execute(self.SELECT_ALL_EXERCISES)
                    results = cursor.fetchall()

            for row in results:
                ex = Exercise()
                ex.id = row[0]
                ex.name = row[1]
                ex.instructions = row[2]
                exercises.append(ex)

            return exercises

        except Exception as e:
            self._logger.log_error(
                f"{inspect.currentframe().f_code.co_name}: {e}"
            )
            return []

    def select_user_completed(self, user_id: int) -> List[Workout]:
        """Returns completed workouts for a user as Workout objects."""
        cursor = None
        results = None
        completed_workouts: List[Workout] = []

        try:
            connection = self._connection_pool.get_connection()
            with connection:
                cursor = connection.cursor()
                with cursor:
                    cursor.execute(self.SELECT_USER_COMPLETED, (user_id,))
                    results = cursor.fetchall()

            for row in results:
                w = Workout()
                w.id = row[0]
                w.title = row[1]
                w.description = row[2]
                w.date_completed = str(row[3])
                w.exercises = self.select_workout_exercises(w.id)
                completed_workouts.append(w)

            return completed_workouts

        except Exception as e:
            self._logger.log_error(
                f"{inspect.currentframe().f_code.co_name}: {e}"
            )
            return []

    def select_user_favorites(self, user_id: int) -> List[Workout]:
        """Returns favorited workouts by a user as Workout objects."""
        cursor = None
        results = None
        favorite_workouts: List[Workout] = []

        try:
            connection = self._connection_pool.get_connection()
            with connection:
                cursor = connection.cursor()
                with cursor:
                    cursor.execute(self.SELECT_USER_FAVORITES, (user_id,))
                    results = cursor.fetchall()

            for row in results:
                w = Workout()
                w.id = row[0]
                w.title = row[1]
                w.description = row[2]
                w.exercises = self.select_workout_exercises(w.id)
                favorite_workouts.append(w)

            return favorite_workouts

        except Exception as e:
            self._logger.log_error(
                f"{inspect.currentframe().f_code.co_name}: {e}"
            )
            return []

    def select_workout_exercises(self, workout_id: int) -> List[Exercise]:
        """Returns Exercise objects for a workout."""
        cursor = None
        results = None
        exercises: List[Exercise] = []

        try:
            connection = self._connection_pool.get_connection()
            with connection:
                cursor = connection.cursor()
                with cursor:
                    cursor.execute(self.SELECT_WORKOUT_EXERCISES, (workout_id,))
                    results = cursor.fetchall()

            for row in results:
                ex = Exercise()
                ex.id = row[0]
                ex.name = row[1]
                ex.instructions = row[2]
                exercises.append(ex)

            return exercises

        except Exception as e:
            self._logger.log_error(
                f"{inspect.currentframe().f_code.co_name}: {e}"
            )
            return []

    # ============================================================
    # INSERT / LINK METHODS
    # ============================================================

    def insert_user(self, user: User) -> Optional[int]:
        """Insert a new user; return new user id or None."""
        try:
            connection = self._connection_pool.get_connection()
            with connection:
                cursor = connection.cursor()
                with cursor:
                    cursor.execute(
                        """
                        INSERT INTO users
                        (first_name, middle_name, last_name, birthday, gender)
                        VALUES (%s, %s, %s, %s, %s)
                        """,
                        (
                            user.first_name,
                            user.middle_name,
                            user.last_name,
                            user.birthday,
                            user.gender,
                        ),
                    )
                    connection.commit()
                    return cursor.lastrowid
        except Exception as e:
            self._logger.log_error(
                f"{inspect.currentframe().f_code.co_name}: {e}"
            )
            return None

    def insert_workout(self, workout: Workout) -> Optional[int]:
        """Insert a new workout; return new workout id or None."""
        try:
            connection = self._connection_pool.get_connection()
            with connection:
                cursor = connection.cursor()
                with cursor:
                    cursor.execute(
                        """
                        INSERT INTO workouts (title, description)
                        VALUES (%s, %s)
                        """,
                        (workout.title, workout.description),
                    )
                    connection.commit()
                    return cursor.lastrowid
        except Exception as e:
            self._logger.log_error(
                f"{inspect.currentframe().f_code.co_name}: {e}"
            )
            return None

    def insert_exercise(self, exercise: Exercise) -> Optional[int]:
        """Insert a new exercise; return new exercise id or None."""
        try:
            connection = self._connection_pool.get_connection()
            with connection:
                cursor = connection.cursor()
                with cursor:
                    cursor.execute(
                        """
                        INSERT INTO exercises (name, instructions)
                        VALUES (%s, %s)
                        """,
                        (exercise.name, exercise.instructions),
                    )
                    connection.commit()
                    return cursor.lastrowid
        except Exception as e:
            self._logger.log_error(
                f"{inspect.currentframe().f_code.co_name}: {e}"
            )
            return None

    def link_workout_exercise(self, workout_id: int, exercise_id: int) -> bool:
        """Create association between a workout and an exercise."""
        try:
            connection = self._connection_pool.get_connection()
            with connection:
                cursor = connection.cursor()
                with cursor:
                    cursor.execute(
                        """
                        INSERT INTO workout_exercises (workout_id, exercise_id)
                        VALUES (%s, %s)
                        """,
                        (workout_id, exercise_id),
                    )
                    connection.commit()
                    return True
        except Exception as e:
            self._logger.log_error(
                f"{inspect.currentframe().f_code.co_name}: {e}"
            )
            return False

    def insert_user_favorite_workout(
        self, user_id: int, workout_id: int
    ) -> bool:
        """Insert a favorite workout for a user."""
        try:
            connection = self._connection_pool.get_connection()
            with connection:
                cursor = connection.cursor()
                with cursor:
                    cursor.execute(
                        """
                        INSERT INTO user_favorite_workouts (user_id, workout_id)
                        VALUES (%s, %s)
                        """,
                        (user_id, workout_id),
                    )
                    connection.commit()
                    return True
        except Exception as e:
            self._logger.log_error(
                f"{inspect.currentframe().f_code.co_name}: {e}"
            )
            return False

    # ============================================================
    #                   PRIVATE HELPER METHODS
    # ============================================================

   

    def _initialize_database_connection_pool(self, config: dict):
        """Initializes database connection pool."""
        try:
            self._logger.log_debug("Creating connection pool...")
            cnx_pool = MySQLConnectionPool(
                pool_name=self.DATABASE["pool"]["name"],
                pool_size=self.DATABASE["pool"]["size"],
                pool_reset_session=self.DATABASE["pool"]["reset_session"],
                **config,
            )
            self._logger.log_debug("Connection pool successfully created!")
            return cnx_pool
        except connector.Error as err:
            self._logger.log_error(f"Problem creating connection pool: {err}")
            self._logger.log_error(
                f"Check DB config:\n{json.dumps(self.DATABASE, indent=2)}"
            )
        except Exception as e:
            self._logger.log_error(f"Unexpected error: {e}")
            self._logger.log_error(
                f"Check DB config:\n{json.dumps(self.DATABASE, indent=2)}"
            )

    def _populate_user_objects(self, results: List) -> List[User]:
        """Populates and returns a list of User objects."""
        user_list: List[User] = []
        try:
            for row in results:
                user = User()
                user.id = row[self.UserColumns["id"].value]
                user.first_name = row[self.UserColumns["first_name"].value]
                user.middle_name = row[self.UserColumns["middle_name"].value]
                user.last_name = row[self.UserColumns["last_name"].value]
                user.birthday = row[self.UserColumns["birthday"].value]
                user.gender = row[self.UserColumns["gender"].value]
                user_list.append(user)

            return user_list
        except Exception as e:
            self._logger.log_error(
                f"{inspect.currentframe().f_code.co_name}: {e}"
            )
            return []

    def _populate_workout_objects(self, results: List) -> List[Workout]:
        """Populates and returns a list of Workout objects."""
        workout_list: List[Workout] = []
        try:
            for row in results:
                workout = Workout()
                workout.id = row[self.WorkoutColumns["id"].value]
                workout.title = row[self.WorkoutColumns["title"].value]
                workout.description = row[self.WorkoutColumns["description"].value]
                workout_list.append(workout)

            return workout_list
        except Exception as e:
            self._logger.log_error(
                f"{inspect.currentframe().f_code.co_name}: {e}"
            )
            return []


        

