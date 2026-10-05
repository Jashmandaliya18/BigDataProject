#!/usr/bin/env python3
import sys
for line in sys.stdin:
    f = line.rstrip("\n").split(",")
    try:
        s = float(f[6])
    except (ValueError, IndexError):
        continue
    if s <= 0:
        continue
    print("%s\t%s,1,%s,%s" % (f[1], s, s, s))
