import getpass
import os
import socket
from os.path import expanduser


def config_defaults():
	defaults = dict()

	home_config = os.path.join(expanduser("~"), "devassist")
	sqlite_path = os.path.join(home_config, os.path.normpath("sqlite.db"))
	dev_home = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))

	defaults["home"] = home_config
  
	defaults["server"] = {
		"host": "0.0.0.0",
		"port": "5555"
	}
	
	return defaults
