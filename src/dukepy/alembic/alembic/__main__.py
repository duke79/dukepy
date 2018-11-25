"""
Ref: https://stackoverflow.com/a/35211383/973425
"""

import os

import alembic.config

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


if __name__ == "__main__":
	migrate()
