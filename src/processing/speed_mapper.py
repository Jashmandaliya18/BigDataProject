#!/usr/bin/env python3
"""Usage: speed_mapper.py driver|band|tyre
Input: cleaned telemetry (17 columns): 1 track, 2 driver, 6 speed, 12 tyre.
driver -> key track|driver ; band -> key track|50 km/h band ; tyre -> key compound
Value: sum,count,min,max (compatible with stats_reducer.py). Stationary frames are ignored."""
import sys
mode = sys.argv[1] if len(sys.argv) > 1 else "driver"

def counter(name):
    sys.stderr.write("reporter:counter:F1Speed,%s,1\n" % name)

for line in sys.stdin:
    f = line.rstrip("\n").split(",")
    if len(f) != 17:
        counter("bad_columns"); continue
    try:
        s = float(f[6])
    except ValueError:
        counter("parse_error"); continue
    if s <= 0:
        continue
    if mode == "driver":
        key, v = "%s|%s" % (f[1], f[2]), s
    elif mode == "band":
        key, v = "%s|%03d" % (f[1], int(s // 50) * 50), 1.0
    else:
        key, v = f[12], s
    print("%s\t%r,1,%r,%r" % (key, v, v, v))
