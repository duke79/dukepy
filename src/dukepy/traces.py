from __future__ import print_function

import traceback

import sys
import json as JSON

import os


def eprint(*args, **kwargs):
	print(*args, file=sys.stderr, **kwargs)


def print_exception_traces(e):
	try:
		if os.environ.get("stacktrace"):
			eprint(traceback.format_exc())
		elif sys.argv["stacktrace"]:
			eprint(e)
	except Exception as ee:  # LOL !
		eprint(e)
		pass


def print_for_cli(e, json=False):
	try:
		if os.environ["print_for_cli"]:
			if not json:
				print(e)
			else:
				print(
					JSON.dumps(e, indent=4, sort_keys=True, default=str))  # https://stackoverflow.com/a/11875813/973425
	except Exception as e:
		# print_exception_traces(e)
		pass


class TracePrints(object):
	def __init__(self):
		self.stdout = sys.stdout

	def write(self, s):
		self.stdout.write("Writing %r\n" % s)
		import traceback
		traceback.print_stack(file=self.stdout)

# sys.stdout = TracePrints()
