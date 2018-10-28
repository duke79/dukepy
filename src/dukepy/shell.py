import os
import subprocess
import sys
from cmd import Cmd


class Pirate(Cmd):
    intro = 'Welcome to shell\n'
    prompt = 'platform> '

    def default(self, line):  # this method will catch all commands
        # subprocess.call(line, shell=True)
        args = str(line).split(" ")
        if args[0] == "cd":
            try:
                os.chdir(args[1])
            except Exception as e:
                os.system(line)
        else:
            os.system(line)
        pass


if __name__ == '__main__':
    if len(sys.argv) > 1:
        Pirate().cmdloop()
    else:
        os.system("start cmd /k python " + __file__ + " new")
