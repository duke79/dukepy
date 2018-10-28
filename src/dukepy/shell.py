import os
import sys
# import cmd2
import cmd


class Shell(cmd.Cmd):
    intro = 'Welcome to shell\n'

    def __init__(self):
        super().__init__()
        self.prompt = os.path.abspath(os.path.curdir) + ">"

    def default(self, line):  # this method will catch all commands
        # subprocess.call(line, shell=True)
        os.system(line)

    def completedefault(self, text, line, begidx, endidx):
        return [filename for filename in os.listdir('.') if filename.startswith(text)]

    def completenames(self, text, *ignored):
        dotext = 'do_' + text
        commands = [a[3:] for a in self.get_names() if a.startswith(dotext)]
        files = [filename for filename in os.listdir('.') if filename.startswith(text)]
        return commands + files

    def do_cd(self, line):
        args = str(line).split(" ")
        try:
            os.chdir(args[0])
        except Exception as e:
            print(os.path.abspath(os.path.curdir))
        self.prompt = os.path.abspath(os.path.curdir) + ">"

    def complete_cd(self, text, line, begidx, endidx):
        return [filename for filename in os.listdir('.') if filename.startswith(text)]


if __name__ == '__main__':
    if len(sys.argv) > 1:
        Shell().cmdloop()
    else:
        os.system("start cmd /k python " + __file__ + " new")
