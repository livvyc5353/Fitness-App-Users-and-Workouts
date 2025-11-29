"""Defines the Console User Interface for the Fitness App."""

import sys
from typing import List

from prettytable import PrettyTable

from fitness_app_users_and_workouts.service_layer.app_services import AppServices
from fitness_app_users_and_workouts.application_base import ApplicationBase
from fitness_app_users_and_workouts.infrastructure_layer.user import User
from fitness_app_users_and_workouts.infrastructure_layer.workout import Workout
from fitness_app_users_and_workouts.infrastructure_layer.exercise import Exercise


class UserInterface(ApplicationBase):
    """Console UI for the Fitness App."""

    def __init__(self, config: dict) -> None:
        """Initialize UI."""
        self._config_dict = config
        self.META = config["meta"]

        super().__init__(
            subclass_name=self.__class__.__name__,
            logfile_prefix_name=self.META["log_prefix"],
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
        print("\t4. Favorite Workout(s) for a User")
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
                self.favorite_workout_for_user()
            case "5":
                self.add_workout()
            case "6":
                print("Goodbye!")
                sys.exit(0)
            case _:
                print(f"Invalid menu choice: {menu_choice}")

    # ============================================================
    # MENU OPTION 1: LIST USERS
    # ============================================================
    def list_users(self) -> None:
        """List all users with their completed and favorite workouts."""
        users: List[User] = self.app_services.get_all_users()

        if not users:
            print("\nNo users found.\n")
            return

        table = PrettyTable()
        table.field_names = [
            "ID",
            "First Name",
            "Middle Name",
            "Last Name",
            "Gender",
            "Birthday",
            "Completed Workouts",
            "Favorite Workouts",
        ]
        table.align = "l"

        for user in users:
            completed_str = "None"
            if getattr(user, "completed_workouts", []):
                completed_str = "\n".join(
                    f"- {w.title} (completed: {w.date_completed})"
                    for w in user.completed_workouts
                )

            favorites_str = "None"
            if getattr(user, "favorite_workouts", []):
                favorites_str = "\n".join(
                    f"- {w.title}" for w in user.favorite_workouts
                )

            table.add_row(
                [
                    user.id,
                    user.first_name,
                    user.middle_name,
                    user.last_name,
                    user.gender,
                    user.birthday,
                    completed_str,
                    favorites_str,
                ]
            )

        print("\nUSERS\n")
        print(table)

    # ============================================================
    # MENU OPTION 2: LIST WORKOUTS
    # ============================================================
    def list_workouts(self) -> None:
        """List all workouts with their exercises."""
        workouts: List[Workout] = self.app_services.get_all_workouts()

        if not workouts:
            print("\nNo workouts found.\n")
            return

        table = PrettyTable()
        table.field_names = ["ID", "Title", "Description", "Exercises"]
        table.align = "l"

        for w in workouts:
            if getattr(w, "exercises", []):
                exercises_str = "\n".join(
                    f"- {ex.name}: {ex.instructions}"
                    for ex in w.exercises
                )
            else:
                exercises_str = "None"

            table.add_row(
                [
                    w.id,
                    w.title,
                    w.description,
                    exercises_str,
                ]
            )

        print("\nWORKOUTS\n")
        print(table)

    # ============================================================
    # MENU OPTION 3: ADD USER
    # ============================================================
    def add_user(self) -> None:
        """Prompt the user for info and add a new user."""
        print("\nAdd New User\n")

        first_name = input("First Name: ").strip()
        middle_name = input("Middle Name (optional): ").strip()
        last_name = input("Last Name: ").strip()
        birthday = input("Birthday (e.g., 2007-06-25): ").strip()
        gender = input("Gender (M/F/Other): ").strip()

        if not first_name or not last_name:
            print("First and last name are required. User not added.")
            return

        success = self.app_services.add_user(
            first_name=first_name,
            middle_name=middle_name,
            last_name=last_name,
            birthday=birthday,
            gender=gender,
        )

        if success:
            print("\nUser successfully added.\n")
        else:
            print("\nFailed to add user. See logs for details.\n")

    # ============================================================
    # MENU OPTION 4: FAVORITE WORKOUT(S) FOR A USER
    # ============================================================
    def favorite_workout_for_user(self) -> None:
        """Allow selecting a user and workout(s) to mark as favorite."""
        print("\nFavorite Workout(s) for a User\n")

        users = self.app_services.get_all_users()
        if not users:
            print("No users available.")
            return

        # Show users
        user_table = PrettyTable()
        user_table.field_names = ["ID", "First Name", "Last Name"]
        user_table.align = "l"

        for u in users:
            user_table.add_row([u.id, u.first_name, u.last_name])

        print("Users:")
        print(user_table)
        print()

        try:
            user_id = int(input("Enter the ID of the user: ").strip())
        except ValueError:
            print("Invalid user ID.")
            return

        # Validate user_id exists
        user_ids = [u.id for u in users]
        if user_id not in user_ids:
            print("User ID not found.")
            return

        # Show workouts
        workouts = self.app_services.get_all_workouts()
        if not workouts:
            print("No workouts available.")
            return

        workout_table = PrettyTable()
        workout_table.field_names = ["ID", "Title"]
        workout_table.align = "l"

        for w in workouts:
            workout_table.add_row([w.id, w.title])

        print("\nWorkouts:")
        print(workout_table)
        print()

        ids_str = input(
            "Enter workout ID(s) to favorite for this user (comma-separated): "
        ).strip()

        if not ids_str:
            print("No workouts selected.")
            return

        try:
            workout_ids = [int(x.strip()) for x in ids_str.split(",") if x.strip()]
        except ValueError:
            print("Invalid workout ID list.")
            return

        success_count = 0
        for wid in workout_ids:
            if any(w.id == wid for w in workouts):
                if self.app_services.favorite_workout(user_id, wid):
                    success_count += 1
            else:
                print(f"Workout ID {wid} not found. Skipping.")

        print(f"\n{success_count} workout(s) favorited for user {user_id}.\n")

    # ============================================================
    # MENU OPTION 5: ADD WORKOUT (OPTION B: PICK EXISTING OR ADD NEW)
    # ============================================================
    def add_workout(self) -> None:
        """Add a new workout, selecting existing exercises and/or adding new ones."""
        print("\nAdd New Workout\n")

        title = input("Workout Title: ").strip()
        description = input("Workout Description: ").strip()

        if not title:
            print("Workout title is required. Workout not added.")
            return

        # 1) Show existing exercises to choose from
        existing_exercises: List[Exercise] = self.app_services.get_all_exercises()
        existing_ids: list[int] = []

        if existing_exercises:
            ex_table = PrettyTable()
            ex_table.field_names = ["ID", "Name", "Instructions"]
            ex_table.align = "l"

            for ex in existing_exercises:
                ex_table.add_row([ex.id, ex.name, ex.instructions])

            print("\nExisting Exercises:")
            print(ex_table)
            print()

            ids_str = input(
                "Enter existing exercise ID(s) to include (comma-separated), "
                "or press Enter to skip: "
            ).strip()

            if ids_str:
                try:
                    existing_ids = [
                        int(x.strip()) for x in ids_str.split(",") if x.strip()
                    ]
                except ValueError:
                    print("Invalid exercise ID list. Skipping existing exercises.")
                    existing_ids = []
        else:
            print("\nNo existing exercises found.\n")

        # 2) Optionally add new exercises
        new_exercises_data: list[dict] = []
        while True:
            add_ex = input(
                "Add a NEW exercise to this workout? (y/n): "
            ).strip().lower()
            if add_ex not in ("y", "yes"):
                break

            ex_name = input("  Exercise Name: ").strip()
            ex_instructions = input("  Exercise Instructions: ").strip()

            if not ex_name:
                print("  Exercise name is required. Skipping this exercise.")
                continue

            new_exercises_data.append(
                {
                    "name": ex_name,
                    "instructions": ex_instructions,
                }
            )

        success = self.app_services.add_workout(
            title=title,
            description=description,
            existing_exercise_ids=existing_ids,
            new_exercises_data=new_exercises_data,
        )

        if success:
            print("\nWorkout successfully added.\n")
        else:
            print("\nFailed to add workout. See logs for details.\n")

    # ============================================================
    # START LOOP
    # ============================================================
    def start(self) -> None:
        """Start UI loop."""
        self._logger.log_debug("User interface started!")

        while True:
            self.display_menu()
            self.process_menu_choice()



        
        