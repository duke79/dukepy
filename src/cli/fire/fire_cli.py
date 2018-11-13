import json
import sys

import fire


class Root():
    """
    Root
    """
    cmd_history = []

    def __init__(self):
        pass

    def history(self):
        for cmd in Root.cmd_history:
            print(json.dumps(cmd, indent=4, sort_keys=True, default=str))  # https://stackoverflow.com/a/11875813/973425


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


if __name__ == "__main__":
    main()
