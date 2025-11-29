"""Defines the MySQLPersistenceWrapper class."""

import json
from mysql import connector
from mysql.connector.pooling import MySQLConnectionPool

from fitness_app_users_and_workouts.application_base import ApplicationBase
import inspect
from typing import List
from fitness_app_users_and_workouts.infrastructure_layer.user import User
from fitness_app_users_and_workouts.infrastructure_layer.workout import Workout
from enum import Enum


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
        self.DB_CONFIG["password"] = self.DATABASE["connection"]["config"].get("password", "")

        self._logger.log_debug(f"DB Connection Config Dict: {self.DB_CONFIG}")
        

        self._logger.log_debug(f"DB Connection Config Dict: {self.DB_CONFIG}")

        # Database Connection
        self._connection_pool = self._initialize_database_connection_pool(self.DB_CONFIG)

        #User Column ENUMS
        self.UserColumns = \
            Enum('UserColumns', [('id', 0), ('first_name', 1),
                ('middle_name', 2), ('last_name', 3), ('birthday', 4),
                ('gender', 5)])
        
        #Workout Column ENUMS
        self.WorkoutColumns = \
            Enum('WorkoutColumns', [('id', 0), ('title', 1),
                    ('description', 2)])

        # ============================================================
        #                          SQL QUERY CONSTANTS
        # ============================================================

         # 1. All users
        self.SELECT_ALL_USERS = (
            "SELECT id, first_name, middle_name, last_name, birthday, gender "
            "FROM users"
        )

        # 2. All workouts
        self.SELECT_ALL_WORKOUTS = (
            "SELECT id, title, description FROM workouts"
        )

        # 3. Workouts completed by user
        self.SELECT_USER_COMPLETED = (
            "SELECT w.title, w.description, c.date_completed "
            "FROM workouts w, user_completed_workouts c "
            "WHERE c.user_id = %s AND w.id = c.workout_id"
        )    

        # 4. Favorite workouts for user
        self.SELECT_USER_FAVORITES = (
            "SELECT w.title, w.description "
            "FROM workouts w, user_favorite_workouts f "
            "WHERE f.user_id = %s AND w.id = f.workout_id"
        )

        # 5. Exercises for a workout
        self.SELECT_WORKOUT_EXERCISES = (
            "SELECT e.name, e.instructions "
            "FROM exercises e, workout_exercises we "
            "WHERE we.workout_id = %s AND we.exercise_id = e.id"
        )


    def select_all_users(self) -> list[User]:
        """Returns all users."""
        cursor = None
        results = None
        user_list = []
        try:
            connection = self.connection_pool.get_connection()
            with connection:
                cursor = connection.cursor()
                with cursor:
                    cursor.execute(self.SELECT_ALL_USERS)
                    results = cursor.fetchall()
                    user_list = self._populate_user_objects(results)
            
            for user in user_list:
                workout_list = \
                    self.select_all_workouts(user.id)
                self._logger.log_debug(f'{inspect.currentframe().f_code.co_name}: \
                    {workout_list}')
                user.workouts = self._populate_workout_objects(workout_list)
                
            return user_list
        
        except Exception as e:
            self._logger.log_error(f'{inspect.currentrame().f_code.co_name}: {e}')



def select_workout_exercises(self) -> List[Workout]:
    """Returns all workouts with their exercises."""
    cursor = None
    results = None
    workout_list = []

    try:
        connection = self._connection_pool.get_connection()
        with connection:
            cursor = connection.cursor()
            with cursor:
                cursor.execute(self.SELECT_WORKOUT_EXERCISES)
                results = cursor.fetchall()
                workout_list = self._populate_workout_objects(results)

        # Load all exercises for each workout
        for workout in workout_list:
            exercise_list = \
                self.select_workout_exercises(workout.id)

            self._logger.log_debug(
                f"{inspect.currentframe().f_code.co_name}: {exercise_list}"
            )

            workout.exercises = \
                self._populate_exercise_objects(exercise_list)

        return workout_list

    except Exception as e:
        self._logger.log_error(
            f"{inspect.currentframe().f_code.co_name}: {e}"
        )

        

    def select_user_completed(self, user_id: int) -> List[Workout]:
        """Returns workouts completed by a user."""
        cursor = None
        results = None
        try:
            connection = self._connection_pool.get_connection()
            with connection:
                cursor = connection.cursor()
                with cursor:
                    cursor.execute(self.SELECT_USER_COMPLETED, ([user_id]))
                    results = cursor.fetchall()

            return results

        except Exception as e:
            self._logger.log_error(f"{inspect.currentframe().f_code.co_name}: {e}")
        
    def select_user_favorites(self, user_id: int) -> List[Workout]:
        """Returns favorited workouts by a user."""
        cursor = None
        results = None
        try:
            connection = self._connection_pool.get_connection()
            with connection:
                cursor = connection.cursor()
                with cursor:
                    cursor.execute(self.SELECT_USER_FAVORITES, ([user_id]))
                    results = cursor.fetchall()

            return results

        except Exception as e:
            self._logger.log_error(f"{inspect.currentframe().f_code.co_name}: {e}")


        
    def select_all_workouts(self) -> List[Workout]:
        """Returns a list of all workout objects."""
        cursor = None
        results = None
        workout_list = []
        try:
            connection = self._connection_pool.get_connection()
            with connection:
                cursor = connection.cursor()
                with cursor:
                    cursor.execute(self.SELECT_ALL_WORKOUTS)
                    results = cursor.fetchall()
                    workout_list = self.populate_workout_objects(results)

            return workout_list

        except Exception as e:
            self._logger.log_error(f"{inspect.currentframe().f_code.co_name}: {e}")


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
                **config
            )
            self._logger.log_debug("Connection pool successfully created!")
            return cnx_pool
        except connector.Error as err:
            self._logger.log_error(f"Problem creating connection pool: {err}")
            self._logger.log_error(f"Check DB config:\n{json.dumps(self.DATABASE, indent=2)}")
        except Exception as e:
            self._logger.log_error(f"Unexpected error: {e}")
            self._logger.log_error(f"Check DB config:\n{json.dumps(self.DATABASE, indent=2)}")



def _populate_user_objects(self, results: List) -> List[User]:
    """Populates and returns a list of User objects."""
    user_list = []
    try:
        for row in results:
            user = User()
            user.id = row[self.UserColumns['id'].value]
            user.first_name = row[self.UserColumns['first_name'].value]
            user.middle_name = row[self.UserColumns['middle_name'].value]
            user.last_name = row[self.UserColumns['last_name'].value]
            user.birthday = row[self.UserColumns['birthday'].value]
            user.gender = row[self.UserColumns['gender'].value]
            user_list.append(user)

        return user_list

    except Exception as e:
        self._logger.log_error(f'{inspect.currentframe().f_code.co_name}: {e}')


def _populate_workout_objects(self, results: List) -> List[Workout]:
    """Populates and returns a list of Workout objects."""
    workout_list = []
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


        

