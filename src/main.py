"""Entry point for the Fitness App Application."""

import json
from argparse import ArgumentParser
from fitness_app_users_and_workouts.persistence_layer.mysql_persistence_wrapper import MySQLPersistenceWrapper
from fitness_app_users_and_workouts.service_layer.app_services \
    import AppServices
from fitness_app_users_and_workouts.presentation_layer.user_interface import UserInterface


def main():
    """Entry point."""
    args = configure_and_parse_commandline_arguments()

    # Load config file
    with open(args.configfile, 'r') as f:
        config = json.loads(f.read())


    ui = UserInterface(config)
    ui.start()

    service_layer = AppServices(config)
    users_list = service_layer.get_all_users_as_json()
    print(users_list)

    db = MySQLPersistenceWrapper(config)

    print("\n=== ALL USERS ===")
    users = db.select_all_users()
    for user in users:
        print(user)

    print("\n=== ALL WORKOUTS ===")
    workouts = db.select_all_workouts()
    for workout in workouts:
        print(workout)

    print("\n=== EXERCISES FOR EACH WORKOUT ===")
    for workout in workouts:
        print(f"\nWorkout: {workout[1]}")
        exercises = db.select_workout_exercises(workout[0])
        for exercise in exercises:
            print(f"  - {exercise[1]}")

    print("\n=== USER FAVORITE WORKOUTS ===")
    for user in users:
        print(f"\nFavorites for {user[1]} {user[3]}:")
        favorites = db.select_user_favorites(user[0])
        for fav in favorites:
            print(f"  💞 {fav[1]}")

    print("\n=== USER COMPLETED WORKOUTS ===")
    for user in users:
        print(f"\nCompleted workouts for {user[1]} {user[3]}:")
        completed = db.select_user_completed(user[0])
        for w in completed:
            print(f"  ✅ {w[1]} on {w[3]}")


def configure_and_parse_commandline_arguments():
    """Configure and parse command-line arguments."""
    parser = ArgumentParser(
        prog='main.py',
        description='Start the Fitness App with a configuration file.',
        epilog='POC: Olivia Clontz | oliviaclontz@gmail.com'
    )

    parser.add_argument('-c', '--configfile',
                        help="Configuration file to load.",
                        required=True)
    return parser.parse_args()


if __name__ == "__main__":
    main()
