"""Entry point for the Employee Training Application."""

import json
from argparse import ArgumentParser
from fitness_app_users_and_workouts.persistence_layer.mysql_persistence_wrapper \
	  import MySQLPersistenceWrapper



def main():
	"""Entry point."""
	args = configure_and_parse_commandline_arguments()

	if args.configfile:
		config = None
		with open(args.configfile, 'r') as f:
			config = json.loads(f.read())

		db = MySQLPersistenceWrapper(config)


def configure_and_parse_commandline_arguments():
	"""Configure and parse command-line arguments."""
	parser = ArgumentParser(
	prog='main.py',
	description='Start the application with a configuration file.',
	epilog='POC: Your Name | your@email')

	parser.add_argument('-c','--configfile',
					help="Configuration file to load.",
					required=True)
	args = parser.parse_args()
	return args



if __name__ == "__main__":
	main()