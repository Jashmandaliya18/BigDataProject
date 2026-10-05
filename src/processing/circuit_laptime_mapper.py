#!/usr/bin/env python3
import sys, os, re
with open("sessions.txt") as fh:
    next(fh)
    sessions = {l.split(",")[0]: l.split(",")[1] for l in fh if l.strip()}
path = os.environ.get("mapreduce_map_input_file") or os.environ.get("map_input_file", "")
m = re.search(r"RaceTimeData_(\d+)\.csv", path)
track = sessions.get(m.group(1)) if m else None
for line in sys.stdin:
    if track is None or line.startswith("frameIdentifierStart"):
        continue
    f = line.rstrip("\r\n").split(",")
    try:
        t = float(f[3])
    except (ValueError, IndexError):
        continue
    if 30 <= t <= 300:
        print("%s\t%s,1,%s,%s" % (track, t, t, t))
