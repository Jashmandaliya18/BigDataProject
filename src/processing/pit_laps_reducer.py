#!/usr/bin/env python3
"""Job 5a reducer. Output: key <TAB> pit_frames <TAB> tyres seen (joined by /)"""
import sys
cur, n, tyres = None, 0, set()
def emit():
    if cur is not None:
        print("%s\t%d\t%s" % (cur, n, "/".join(sorted(tyres))))
for line in sys.stdin:
    k, t = line.rstrip("\n").split("\t")
    if k != cur:
        emit(); cur, n, tyres = k, 0, set()
    n += 1
    tyres.add(t)
emit()
