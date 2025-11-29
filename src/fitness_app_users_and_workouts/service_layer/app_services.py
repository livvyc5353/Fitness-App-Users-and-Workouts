"""Implements AppServices Class."""

import json
import inspect
from typing import List

from fitness_app_users_and_workouts.application_base import ApplicationBase
from fitness_app_users_and_workouts.persistence_layer.mysql_persistence_wrapper import (
    MySQLPersistenceWrapper,
)
from fitness_app_users_and_workouts.infrastructure_layer.user import User
from fitness_app_users_and_workouts.infrastructure_layer.workout import Workout
from fitness_app_users_and_workouts.infrastructure_layer.exercise import Exercise


class AppServices(ApplicationBase):
    """AppServices class for interacting with the Fitness App database."""

    def __init__(self, config: dict) -> None:
        """Initializes object."""
        self._config_dict = config
        self.META = config["meta"]
        super().__init__(
            subclass_name=self.__class__.__name__,
            logfile_prefix_name=self.META["log_prefix"],
        )
        self.DB = MySQLPersistenceWrapper(config)

    # ============================================================
    # USER READ METHODS
    # ============================================================

    def get_all_users(self) -> List[User]:
        """Return all users with completed and favorite workouts populated."""
        self._logger.log_debug(
            f"In {inspect.currentframe().f_code.co_name}()..."
        )
        try:
            users = self.DB.select_all_users()

            for user in users:
                user.completed_workouts = self.DB.select_user_completed(user.id)
                user.favorite_workouts = self.DB.select_user_favorites(user.id)

            return users

        except Exception as e:
            self._logger.log_error(
                f"{inspect.currentframe().f_code.co_name}: {e}"
            )
            return []

    def get_all_users_as_json(self) -> str:
        """Returns all users (with workouts) as JSON string."""
        self._logger.log_debug(
            f"In {inspect.currentframe().f_code.co_name}()..."
        )
        try:
            users = self.get_all_users()
            return json.dumps([json.loads(u.to_json()) for u in users])
        except Exception as e:
            self._logger.log_error(
                f"{inspect.currentframe().f_code.co_name}: {e}"
            )
            return "[]"

    # ============================================================
    # WORKOUT READ METHODS
    # ============================================================

    def get_all_workouts(self) -> List[Workout]:
        """Returns all workouts with exercises."""
        self._logger.log_debug(
            f"In {inspect.currentframe().f_code.co_name}()..."
        )
        try:
            workouts = self.DB.select_all_workouts()
            return workouts
        except Exception as e:
            self._logger.log_error(
                f"{inspect.currentframe().f_code.co_name}: {e}"
            )
            return []

    def get_all_workouts_as_json(self) -> str:
        """Returns all workouts as JSON string."""
        self._logger.log_debug(
            f"In {inspect.currentframe().f_code.co_name}()..."
        )
        try:
            workouts = self.get_all_workouts()
            return json.dumps([json.loads(w.to_json()) for w in workouts])
        except Exception as e:
            self._logger.log_error(
                f"{inspect.currentframe().f_code.co_name}: {e}"
            )
            return "[]"

    def get_workout_exercises_as_json(self, workout_id: int) -> str:
        """Returns all exercises for a workout in JSON format."""
        self._logger.log_debug(
            f"In {inspect.currentframe().f_code.co_name}()..."
        )
        try:
            results = self.DB.select_workout_exercises(workout_id)
            return json.dumps([json.loads(ex.to_json()) for ex in results])
        except Exception as e:
            self._logger.log_error(
                f"{inspect.currentframe().f_code.co_name}: {e}"
            )
            return "[]"

    def get_all_exercises(self) -> List[Exercise]:
        """Return all exercises."""
        self._logger.log_debug(
            f"In {inspect.currentframe().f_code.co_name}()..."
        )
        try:
            return self.DB.select_all_exercises()
        except Exception as e:
            self._logger.log_error(
                f"{inspect.currentframe().f_code.co_name}: {e}"
            )
            return []

    # ============================================================
    # USER WORKOUT RELATIONSHIP METHODS (JSON UTILITIES)
    # ============================================================

    def get_user_favorites_as_json(self, user_id: int) -> str:
        """Returns user's favorite workouts as JSON."""
        self._logger.log_debug(
            f"In {inspect.currentframe().f_code.co_name}()..."
        )
        try:
            results = self.DB.select_user_favorites(user_id)
            return json.dumps([json.loads(w.to_json()) for w in results])
        except Exception as e:
            self._logger.log_error(
                f"{inspect.currentframe().f_code.co_name}: {e}"
            )
            return "[]"

    def get_user_completed_as_json(self, user_id: int) -> str:
        """Returns completed workouts for a user as JSON."""
        self._logger.log_debug(
            f"In {inspect.currentframe().f_code.co_name}()..."
        )
        try:
            results = self.DB.select_user_completed(user_id)
            return json.dumps([json.loads(w.to_json()) for w in results])
        except Exception as e:
            self._logger.log_error(
                f"{inspect.currentframe().f_code.co_name}: {e}"
            )
            return "[]"

    # ============================================================
    # WRITE METHODS (ADD USER / WORKOUT / FAVORITE)
    # ============================================================

    def add_user(
        self,
        first_name: str,
        middle_name: str,
        last_name: str,
        birthday: str,
        gender: str,
    ) -> bool:
        """Create and persist a new user."""
        self._logger.log_debug(
            f"In {inspect.currentframe().f_code.co_name}()..."
        )
        try:
            user = User()
            user.first_name = first_name
            user.middle_name = middle_name
            user.last_name = last_name
            user.birthday = birthday
            user.gender = gender

            user_id = self.DB.insert_user(user)
            return user_id is not None
        except Exception as e:
            self._logger.log_error(
                f"{inspect.currentframe().f_code.co_name}: {e}"
            )
            return False

    def add_workout(
        self,
        title: str,
        description: str,
        existing_exercise_ids: list[int],
        new_exercises_data: list[dict],
    ) -> bool:
        """
        Create and persist a new workout with exercises.

        existing_exercise_ids: list of exercise IDs to link
        new_exercises_data: list of dicts like:
          {"name": "Push-Up", "instructions": "Do 10 reps"}
        """
        self._logger.log_debug(
            f"In {inspect.currentframe().f_code.co_name}()..."
        )
        try:
            workout = Workout()
            workout.title = title
            workout.description = description

            workout_id = self.DB.insert_workout(workout)
            if workout_id is None:
                return False

            # Link existing exercises
            for ex_id in existing_exercise_ids:
                self.DB.link_workout_exercise(workout_id, ex_id)

            # Insert and link new exercises
            for ex_data in new_exercises_data:
                ex = Exercise()
                ex.name = ex_data.get("name", "")
                ex.instructions = ex_data.get("instructions", "")
                ex_id = self.DB.insert_exercise(ex)
                if ex_id is not None:
                    self.DB.link_workout_exercise(workout_id, ex_id)

            return True

        except Exception as e:
            self._logger.log_error(
                f"{inspect.currentframe().f_code.co_name}: {e}"
            )
            return False

    def favorite_workout(self, user_id: int, workout_id: int) -> bool:
        """Mark a workout as favorite for a given user."""
        self._logger.log_debug(
            f"In {inspect.currentframe().f_code.co_name}()..."
        )
        try:
            return self.DB.insert_user_favorite_workout(user_id, workout_id)
        except Exception as e:
            self._logger.log_error(
                f"{inspect.currentframe().f_code.co_name}: {e}"
            )
            return False

