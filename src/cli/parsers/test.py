from BaseSubparserHandler import BaseSubparserHandler

class TestSubparserHandler(BaseSubparserHandler):
	def __init__(self):
		BaseSubparserHandler.__init__(self)
		self.parsers = []
		self.parsers.append(["test", "For testing purposes (not for general use)"])

	def listSubparsers(self):
		return self.parsers

	def populateSubparser(self, subparser, name=""):
		BaseSubparserHandler.populateSubparser(self, subparser, name)
		if name == self.parsers[0][0]:  # test (this name may change, confirm from self.parsers)
			subparser.add_argument("-l", "--logs", nargs="?",
								   help="print the log type examples")

	def handleSubparser(self, args, name=""):
		if name == self.parsers[0][0]:
			if args.logs:
				from lib.Logger import Logger
				# Logger.level = Logger.Levels.SUCCESS
				Logger().info(args.logs)
				Logger().debug(args.logs)
				Logger().error(args.logs)
				print(args.logs)
