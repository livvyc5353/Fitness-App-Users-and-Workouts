"""Defines the MySQLPersistenceWrapper class."""

import json
from mysql import connector
from mysql.connector.pooling import MySQLConnectionPool

from fitness_app_users_and_workouts.application_base import ApplicationBase


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

        # Build config dict for DB connection
        self.DB_CONFIG = {
            "database": self.DATABASE["connection"]["config"]["database"],
            "user": self.DATABASE["connection"]["config"]["user"],
            "host": self.DATABASE["connection"]["config"]["host"],
            "port": self.DATABASE["connection"]["config"]["port"],
            "password": self.DATABASE["connection"]["config"].get("password", "")
        }

        self._logger.log_debug(f"DB Connection Config Dict: {self.DB_CONFIG}")

        # Create connection pool
        self._connection_pool = self._initialize_database_connection_pool(self.DB_CONFIG)

        # ============================================================
        #               FITNESS APP SQL QUERY CONSTANTS
        # ============================================================

        self.SELECT_ALL_USERS = """
            SELECT id, first_name, middle_name, last_name, birthday, gender
            FROM users;
        """

        self.SELECT_ALL_WORKOUTS = """
            SELECT id, title, description
            FROM workouts;
        """

        self.SELECT_WORKOUT_EXERCISES = """
            SELECT e.id, e.name, e.instructions
            FROM exercises e
            JOIN workout_exercises we ON we.exercise_id = e.id
            WHERE we.workout_id = %s;
        """

        self.SELECT_USER_FAVORITES = """
            SELECT w.id, w.title, w.description
            FROM workouts w
            JOIN user_favorite_workouts f ON f.workout_id = w.id
            WHERE f.user_id = %s;
        """

        self.SELECT_USER_COMPLETED = """
            SELECT w.id, w.title, w.description, c.date_completed
            FROM workouts w
            JOIN user_completed_workouts c ON c.workout_id = w.id
            WHERE c.user_id = %s;
        """

    # ============================================================
    #           PUBLIC METHODS — FITNESS APP DATABASE OPS
    # ============================================================

    def select_all_users(self) -> list:
        """Returns all users."""
        return self._run_select_query(self.SELECT_ALL_USERS)

    def select_all_workouts(self) -> list:
        """Returns all workouts."""
        return self._run_select_query(self.SELECT_ALL_WORKOUTS)

    def select_workout_exercises(self, workout_id: int) -> list:
        """Returns all exercises in a given workout."""
        return self._run_select_query(self.SELECT_WORKOUT_EXERCISES, (workout_id,))

    def select_user_favorites(self, user_id: int) -> list:
        """Returns all workouts a user has favorited."""
        return self._run_select_query(self.SELECT_USER_FAVORITES, (user_id,))

    def select_user_completed(self, user_id: int) -> list:
        """Returns all workouts a user has completed."""
        return self._run_select_query(self.SELECT_USER_COMPLETED, (user_id,))

    # ============================================================
    #                   PRIVATE HELPER METHODS
    # ============================================================

    def _run_select_query(self, query: str, params: tuple = None) -> list:
        """Runs a SELECT query with optional parameters and returns results."""
        try:
            connection = self._connection_pool.get_connection()
            with connection.cursor() as cursor:
                cursor.execute(query, params)
                return cursor.fetchall()
        except Exception as e:
            self._logger.log_error(f"Error running query: {e}")
            return []

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
