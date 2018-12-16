class BaseSubparserHandler:
	"""
	Interface to be implemented by sub-parser providers.
	"""

	def __init__(self):
		pass

	def listSubparsers(self):
		"""
		Return the list of subparsers for which [populateSubparser] & [handleSubparser] will be called.
		:return: The list of subparsers in the format [name,help_message].
		"""
		return [
			# ["sub1", "sub1 help"],
			# ["sub2", "sub2 help"],
		]

	def populateSubparser(self, subparser, name=""):
		"""
		Populate the sub-parser arguments.
		:param subparser: The sub-parser that is to be populated.
		:param name: Name of the sub-parser (for identification purposes), required only if provider handles more than one sub-parsers.
		:return:
		"""
		parsers = self.listSubparsers()
		for parser in parsers:
			if name == parser[0]:
				subparser.set_defaults(which=parser[0] )  # To distinguish between subparsers

	def handleSubparser(self, args, name=""):
		"""
		Sub-parser has been invoked from the command line. Rest of the handling goes here.
		:param name: Name of the sub-parser (for identification purposes), required only if provider handles more than one sub-parsers.
		:return:
		"""
		raise Exception("NotImplementedException")
