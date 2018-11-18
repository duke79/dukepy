import re
import sys

with open(sys.argv[1]) as f:
    p = re.compile("dukepy.([^ ]*) ", re.IGNORECASE)
    # print(f.read())
    for line in f:
        m = p.search(line)
        if m:
            print(m.group(1))
