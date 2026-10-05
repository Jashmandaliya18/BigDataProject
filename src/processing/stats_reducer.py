#!/usr/bin/env python3
# Combiner (arg "combine") and reducer (no arg). Value format: sum,count,min,max
import sys
mode = sys.argv[1] if len(sys.argv) > 1 else "final"
cur, s, n, mn, mx = None, 0.0, 0, float("inf"), 0.0
def emit():
    if cur is None:
        return
    if mode == "combine":
        print("%s\t%s,%d,%s,%s" % (cur, s, n, mn, mx))
    else:
        print("%s\t%d\t%.3f\t%.3f\t%.3f" % (cur, n, s / n, mn, mx))
for line in sys.stdin:
    k, v = line.rstrip("\n").split("\t")
    a, b, c, d = v.split(",")
    if k != cur:
        emit(); cur, s, n, mn, mx = k, 0.0, 0, float("inf"), 0.0
    s += float(a); n += int(b); mn = min(mn, float(c)); mx = max(mx, float(d))
emit()
