"""Defines the Console User Interface for the Fitness App."""

import sys
from fitness_app_users_and_workouts.service_layer.app_services import AppServices
from fitness_app_users_and_workouts.application_base import ApplicationBase
from prettytable import PrettyTable

class UserInterface(ApplicationBase):
    """Console UI for the Fitness App."""

    def __init__(self, config: dict) -> None:
        """Initialize UI."""
        self._config_dict = config
        self.META = config["meta"]

        super().__init__(
            subclass_name=self.__class__.__name__,
            logfile_prefix_name=self.META["log_prefix"]
        )

        self.app_services = AppServices(config)
        self._logger.log_debug("User Interface initialized!")

    # ============================================================
    # DISPLAY MENU
    # ============================================================
    def display_menu(self) -> None:
        """Display the Fitness App menu."""
        print("\n\t\tFitness App Menu\n")
        print("\t1. List Users")
        print("\t2. List Workouts")
        print("\t3. Add User")
        print("\t4. Favorite Workout")
        print("\t5. Add Workout")
        print("\t6. Exit\n")

    # ============================================================
    # PROCESS MENU CHOICE
    # ============================================================
    def process_menu_choice(self) -> None:
        """Process user menu choice."""
        menu_choice = input("\tMenu Choice: ").strip()

        match menu_choice:
            case "1":
                self.list_users()
            case "2":
                self.list_workouts()
            case "3":
                self.add_user()
            case "4":
                self.favorite_workout()
            case "5":
                self.add_workout()
            case "6":
                print("Goodbye!")
                sys.exit(0)
            case _:
                print(f"Invalid menu choice: {menu_choice}")

    # ============================================================
    # MENU OPTION: LIST USERS
    # ============================================================
    def list_users(self) -> None:
        """List all users with their completed workouts and exercises."""
        users = self.app_services.get_all_users()
        user_table = PrettyTable()
        user_table.field_names = [
            "ID", "First Name", "Middle Name", "Last Name",
            "Gender", "Birthday", "Completed Workouts"
        ]

        workout_table = PrettyTable()
        workout_table.field_names = ["Workout", "Exercise", "Completed On"]
        workout_table.align = "l"

        for user in users:
            # Build workout table for this user
            for workout in user.workouts:
                workout_table.add_row([
                    workout.title,
                    ", ".join(ex.name for ex in workout.exercises),
                    workout.date_completed
                ])

            user_table.add_row([
                user.id,
                user.first_name,
                user.middle_name,
                user.last_name,
                user.gender,
                user.birthday,
                workout_table.get_string()
            ])

            user_table.add_divider()
            workout_table.clear_rows()

        print(user_table)

    # ============================================================
    # OTHER MENU STUBS
    # ============================================================
    def list_workouts(self):
        print("list_workouts() called...")
        print(self.app_services.get_all_workouts_as_json())

    def add_user(self):
        print("add_user() called...")
        # implement later

    def favorite_workout(self):
        print("favorite_workout() called...")
        # implement later

    def add_workout(self):
        print("add_workout() called...")
        # implement later

    # ============================================================
    # START LOOP
    # ============================================================
    def start(self) -> None:
        """Start UI loop."""
        self._logger.log_debug("User interface started!")

        while True:
            self.display_menu()
            self.process_menu_choice()


        
        