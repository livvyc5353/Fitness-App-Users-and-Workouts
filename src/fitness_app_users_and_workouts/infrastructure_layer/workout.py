# Contains the definition for the Workout class

import json
from typing import List


class Workout:

    def __init__(self) -> None:
        self.id: int = 0
        self.title: str = ""
        self.description: str = ""

        self.exercises: List = []

        self.date_completed: str = ""

    def __str__(self) -> str:
        return self.to_json()

    def __repr__(self) -> str:
        return self.to_json()

    def to_json(self) -> str:
        workout_dict = {
            "id": self.id,
            "title": self.title,
            "description": self.description,
            "date_completed": self.date_completed,
            "exercises": [],
        }

        for ex in self.exercises:
            workout_dict["exercises"].append(ex.__dict__)

        return json.dumps(workout_dict)
