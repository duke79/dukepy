import json

import os


def json_dump(obj):
    print(json.dumps(obj, indent=4, sort_keys=True, default=str))  # https://stackoverflow.com/a/11875813/973425


def abc(argument=""):
    print(argument)
    return argument


class Root:
    """
    Root
    """
    cmd_history = []

    def __init__(self):
        os.environ["print_for_cli"] = "1"

        self.abc = abc

    def dummy_json(self):
        obj = {
            "key1": [
                "val1",
                {
                    "key2": "val2",
                    "key3": 3.6
                }
            ]
        }
        json_dump(obj)

    def echo(self, arg):
        """
        JSON arg Tested : echo '{"a":"123", "tois":{"moins":12, "hil":["hodor", "mind"]}}'
        :param arg:
        :return:
        """
        json_dump(arg)

    def history(self):
        for cmd in Root.cmd_history:
            json_dump(cmd)
