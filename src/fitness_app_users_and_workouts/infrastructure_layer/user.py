# Contains the definition for the User class

import json
from typing import List
from fitness_app_users_and_workouts.infrastructure_layer.workout import Workout


class User:
    def __init__(self) -> None:
        self.id: int = 0
        self.first_name: str = ""
        self.middle_name: str = ""
        self.last_name: str = ""
        self.birthday: str = ""
        self.gender: str = ""
        self.workouts: List[Workout] = []

    def __str__(self) -> str:
        return self.to_json()

    def __repr__(self) -> str:
        return self.to_json()

    def to_json(self) -> str:
        user_dict = {
            "id": self.id,
            "first_name": self.first_name,
            "middle_name": self.middle_name,
            "last_name": self.last_name,
            "birthday": self.birthday,
            "gender": self.gender,
            "workouts": [],
        }

        for w in self.workouts:
            user_dict["workouts"].append(w.__dict__)

        return json.dumps(user_dict)
