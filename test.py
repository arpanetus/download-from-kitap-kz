import argparse
parser = argparse.ArgumentParser()
parser.add_argument("--host", default="localhost", help="Name of host for database.  Default is 'localhost'.")
args = parser.parse_args()
print(args)
