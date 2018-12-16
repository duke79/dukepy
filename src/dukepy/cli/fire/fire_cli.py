import json
import sys
import threading
from io import StringIO

import fire


def json_dump(obj):
    print(json.dumps(obj, indent=4, sort_keys=True, default=str))  # https://stackoverflow.com/a/11875813/973425


class Root():
    """
    Root
    """
    cmd_history = []

    def __init__(self):
        pass

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


def main():
    if len(sys.argv) > 1:
        args = ""
        for arg in sys.argv[1:]:
            args += " " + arg
        fire.Fire(Root, args)
        Root.cmd_history.append(args)
    else:
        print("no args...")

    while True:
        cmd = input()
        fire.Fire(Root, cmd)
        Root.cmd_history.append(cmd)


def fire_task_wrapper(cmd, emit):
    class TeeIn(StringIO):
        def write(self, s):
            emit('my response', {'stdin': s})
            StringIO.write(self, s)
            sys.__stdin__.write(s)

    class TeeOut(StringIO):
        def write(self, s):
            emit('my response', {'stdout': s})
            StringIO.write(self, s)
            sys.__stdout__.write(s)

    class TeeErr(StringIO):
        def write(self, s):
            emit('my response', {'stderr': s})
            StringIO.write(self, s)
            sys.__stderr__.write(s)

    # @processify
    def fire_task(command):
        # Save everything that would otherwise go to stdout.
        stdin = TeeIn()
        sys.stdin = stdin

        stdout = TeeOut()
        sys.stdout = stdout

        stderr = TeeErr()
        sys.stderr = stderr

        fire.Fire(Root, command)

    pass
    # fire_task(cmd)
    t = threading.Thread(name='child procs', target=fire_task(cmd))
    t.start()
    pass


if __name__ == "__main__":
    main()
