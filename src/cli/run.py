""" Main script for cli that runs all other scripts """
import argparse

from parsers.test import TestSubparserHandler


def PopulateSubparsers(subparserHandlers, subparsers):
	for subparserHandler in subparserHandlers:
		for spHandled in subparserHandler.listSubparsers():
			subparser = subparsers.add_parser(spHandled[0], help=spHandled[1])
			subparserHandler.populateSubparser(subparser, spHandled[0])


def HandleSubparsers(subparserHandlers, args):
	for subparserHandler in subparserHandlers:
		for spHandled in subparserHandler.listSubparsers():
			if args.which == spHandled[0]:
				subparserHandler.handleSubparser(args, name=args.which)


def initCLI(subparserHandlers, args=None):
	# Initialize the root parser
	parser = argparse.ArgumentParser(description="ProjectName - command line | "
												 "sub-commands' help can be seen using -h; eg. cr -h")
	subparsers = parser.add_subparsers(help='available commands')

	PopulateSubparsers(subparserHandlers, subparsers)

	# Parse the arguments and delegate to the applicable sub-parser
	parsedArgs = parser.parse_args(args)
	try:
		HandleSubparsers(subparserHandlers, parsedArgs)
	except KeyboardInterrupt:
		pass


def getParsers():
	# --------------------------------Subparsers-------------------------------------- #
	subparserHandlers = []	
	subparserHandlers.append(TestSubparserHandler())
	"""Add more subparsers :)"""
	# -------------------------------------------------------------------------------- #
	return subparserHandlers


if __name__ == "__main__":
	parsers = getParsers()
	initCLI(parsers)
