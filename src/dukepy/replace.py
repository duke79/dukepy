import os
import re
import sys
from shutil import move
from tempfile import mkstemp


def is_valid(file_path):
    if str(file_path).lower().endswith(".py"):
        return True
    else:
        return False


def replace_in_file(file_path):
    fh, abs_path = mkstemp()
    with os.fdopen(fh, 'w') as new_file:
        with open(file_path) as f:
            p = re.compile("(dukepy.)([^ ]* )(.*)", re.IGNORECASE)
            # print(f.read())
            for idx, line in enumerate(f):
                m = p.search(line)
                if m:
                    groups = m.group(0, 1)
                    # print(str(groups) + " | " + file_path)
                    replacement = p.sub("duka.\\2\\3", line)
                    print("Line " + str(idx) + "| " + line + " -> " + replacement + "   | " + file_path)
                    new_file.write(replacement)
                    pass
                else:
                    new_file.write(line)
                    pass
    os.remove(file_path)
    move(abs_path, file_path)


path = sys.argv[1]
if os.path.isdir(path):
    for (root, dirs, files) in os.walk(path, topdown=True):
        for file in files:
            if is_valid(file):
                replace_in_file(os.path.join(root, file))
else:
    replace_in_file(path)
