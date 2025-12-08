"""Implements behavior common to all application classes.."""

from abc import ABC, abstractmethod
from fitness_app_users_and_workouts.logging import LoggingService
from fitness_app_users_and_workouts.settings import Settings

class ApplicationBase(ABC):
    
    def __init__(self, subclass_name:str, logfile_prefix_name:str)->None:
        self._settings = Settings().read_settings_file_from_location()
        self._logger = LoggingService(subclass_name, logfile_prefix_name)
        
       
    



    