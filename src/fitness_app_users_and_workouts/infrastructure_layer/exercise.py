# Contains the definition for the Exercise class

import json


class Exercise:

    def __init__(self) -> None:
        self.id: int = 0
        self.name: str = ""
        self.instructions: str = ""

    def __str__(self) -> str:
        return self.to_json()

    def __repr__(self) -> str:
        return self.to_json()

    def to_json(self) -> str:
        exercise_dict = {
            "id": self.id,
            "name": self.name,
            "instructions": self.instructions,
        }
        return json.dumps(exercise_dict)
