#!/usr/bin/env python3
import sys, os, re

def valid_lap(f, t):
    """Complete lap: 3 sectors > 0 and sector sum matches LapTime (+-0.1 s)."""
    try:
        s1, s2, s3 = int(f[4]), int(f[5]), int(f[6])
    except (ValueError, IndexError):
        return False
    return (30 <= t <= 300 and s1 > 0 and s2 > 0 and s3 > 0
            and abs((s1 + s2 + s3) / 1000.0 - t) <= 0.1)
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
    if valid_lap(f, t):
        print("%s\t%s,1,%s,%s" % (track, t, t, t))
