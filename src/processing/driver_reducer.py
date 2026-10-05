#!/usr/bin/env python3
"""Combiner (arg 'combine') and reducer. Value format: sum,sumsq,count,min,max"""
import sys, math
mode = sys.argv[1] if len(sys.argv) > 1 else "final"
cur, s, q, n, mn, mx = None, 0.0, 0.0, 0, float("inf"), 0.0

def emit():
    if cur is None:
        return
    if mode == "combine":
        print("%s\t%r,%r,%d,%r,%r" % (cur, s, q, n, mn, mx))
    else:
        mean = s / n
        std = math.sqrt(max(0.0, q / n - mean * mean))
        print("%s\t%d\t%.3f\t%.3f\t%.3f\t%.3f" % (cur, n, mean, mn, mx, std))

for line in sys.stdin:
    k, v = line.rstrip("\n").split("\t")
    a, b, c, d, e = v.split(",")
    if k != cur:
        emit(); cur, s, q, n, mn, mx = k, 0.0, 0.0, 0, float("inf"), 0.0
    s += float(a); q += float(b); n += int(c); mn = min(mn, float(d)); mx = max(mx, float(e))
emit()
