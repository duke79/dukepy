"""
Ref: https://stackoverflow.com/a/35211383/973425
"""

import os

import alembic.config
import sys

from core.traces import print_exception_traces
from data.common import db_uri
from data.tables import *  # DON NOT REMOVE | Redundant import kept on purpose


def good_dir(func):
	def good_dir_wrapper(*args, **kwargs):
		cd = os.curdir
		os.chdir(os.path.dirname(__file__))
		# print(os.path.abspath(os.path.curdir))
		func(*args, **kwargs)
		os.chdir(cd)

	return good_dir_wrapper


@good_dir
def upgrade():
	alembicArgs = [
		'--raiseerr',
		'-x', 'dbPath=' + db_uri,
		'upgrade', 'head',
	]
	alembic.config.main(argv=alembicArgs)


@good_dir
def migrate(revision_name="new revision"):
	alembicArgs = [
		'--raiseerr',
		'-x', 'dbPath=' + db_uri,
		"revision", "--autogenerate", "-m", revision_name
	]
	alembic.config.main(argv=alembicArgs)


@good_dir
def print_db_uri(output_file):
	with open(output_file, "w") as f:
		f.write(db_uri[10:])


if __name__ == "__main__":
	try:  # To print the path of sqlite db for sqlite_web
		if "migrate" == sys.argv[1]:
			migrate()
		elif "upgrade" == sys.argv[1]:
			upgrade()
		else:
			output_file = sys.argv[1]
			print_db_uri(output_file)
	except Exception as e:
		print_exception_traces(e)
