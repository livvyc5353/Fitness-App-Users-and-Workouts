"""Implements the application service layer for the Fitness App."""

import json
import inspect
from typing import List, Dict
from fitness_app_users_and_workouts.application_base import ApplicationBase
from fitness_app_users_and_workouts.persistence_layer.mysql_persistence_wrapper import MySQLPersistenceWrapper


class AppServices(ApplicationBase):
    """AppServices class for interacting with the Fitness App database."""

    def __init__(self, config: dict) -> None:
        """Initializes object."""
        self._config_dict = config
        self.META = config["meta"]

        super().__init__(
            subclass_name=self.__class__.__name__,
            logfile_prefix_name=self.META["log_prefix"]
        )

        self.DB = MySQLPersistenceWrapper(config)

    # ============================================================
    # USER METHODS
    # ============================================================

    def get_all_users_as_json(self) -> str:
        """Returns all users as JSON string."""
        self._logger.log_debug(f"In {inspect.currentframe().f_code.co_name}()...")
        try:
            results = self.DB.select_all_users()
            return json.dumps(results)
        except Exception as e:
            self._logger.log_error(f"{inspect.currentframe().f_code.co_name}: {e}")
            return "[]"

    # ============================================================
    # WORKOUT METHODS
    # ============================================================

    def get_all_workouts_as_json(self) -> str:
        """Returns all workouts as JSON string."""
        self._logger.log_debug(f"In {inspect.currentframe().f_code.co_name}()...")
        try:
            results = self.DB.select_all_workouts()
            return json.dumps(results)
        except Exception as e:
            self._logger.log_error(f"{inspect.currentframe().f_code.co_name}: {e}")
            return "[]"

    def get_workout_exercises_as_json(self, workout_id: int) -> str:
        """Returns all exercises for a workout in JSON format."""
        self._logger.log_debug(f"In {inspect.currentframe().f_code.co_name}()...")
        try:
            results = self.DB.select_workout_exercises(workout_id)
            return json.dumps(results)
        except Exception as e:
            self._logger.log_error(f"{inspect.currentframe().f_code.co_name}: {e}")
            return "[]"

    # ============================================================
    # USER WORKOUT RELATIONSHIP METHODS
    # ============================================================

    def get_user_favorites_as_json(self, user_id: int) -> str:
        """Returns user's favorite workouts as JSON."""
        self._logger.log_debug(f"In {inspect.currentframe().f_code.co_name}()...")
        try:
            results = self.DB.select_user_favorites(user_id)
            return json.dumps(results)
        except Exception as e:
            self._logger.log_error(f"{inspect.currentframe().f_code.co_name}: {e}")
            return "[]"

    def get_user_completed_as_json(self, user_id: int) -> str:
        """Returns completed workouts for a user as JSON."""
        self._logger.log_debug(f"In {inspect.currentframe().f_code.co_name}()...")
        try:
            results = self.DB.select_user_completed(user_id)
            return json.dumps(results)
        except Exception as e:
            self._logger.log_error(f"{inspect.currentframe().f_code.co_name}: {e}")
            return "[]"

