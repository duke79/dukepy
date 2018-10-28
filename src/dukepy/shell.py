import os
import subprocess
import sys
import cmd2
import cmd


class Shell(cmd.Cmd):
    intro = 'Welcome to shell\n'
    prompt = os.path.abspath(os.path.curdir) + ">"

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
        Shell.prompt = os.path.abspath(os.path.curdir) + ">"


if __name__ == '__main__':
    if len(sys.argv) > 1:
        Shell().cmdloop()
    else:
        os.system("start cmd /k python " + __file__ + " new")
