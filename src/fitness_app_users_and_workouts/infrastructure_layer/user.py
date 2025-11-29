"""Contains the definition for the User class."""

import json
from fitness_app_users_and_workouts.infrastructure_layer import Workout
from typing import List


class Employee():
        """Implements an User entity."""
        def __init__(self)->None:
            self.id:int = 0
            self.first_name:str = ""
            self.middle_name:str = ""
            self.last_name:str = ""
            self.birthday:str = ""
            self.gender:str = ""
            self.training:List[Workout] = []

        def __str__(self)->str:
            return self.to_json()


        def __repr__(self)->str:
            return self.to_json()


        def to_json(self)->str:
            user_dict = {}
            user_dict['id'] = self.id
            user_dict['first_name'] = self.first_name
            user_dict['middle_name'] = self.middle_name
            user_dict['last_name'] = self.last_name
            user_dict['birthday'] = self.birthday
            user_dict['gender'] = self.gender
            user_dict['workout'] = []

            for item in self.workout:
                user_dict['workout'].append(item.__dict__)

            return json.dumps(user_dict)