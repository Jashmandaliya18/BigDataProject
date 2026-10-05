#!/usr/bin/env python3
"""Usage: laptime_mapper.py trend|fastest
trend   -> key track|lap(3 digits)
fastest -> key track|driver
value   -> sum,count,min,max (compatible with stats_reducer.py)"""
import sys, os, re

def valid_lap(f, t):
    """Complete lap: 3 sectors > 0 and sector sum matches LapTime (+-0.1 s)."""
    try:
        s1, s2, s3 = int(f[4]), int(f[5]), int(f[6])
    except (ValueError, IndexError):
        return False
    return (30 <= t <= 300 and s1 > 0 and s2 > 0 and s3 > 0
            and abs((s1 + s2 + s3) / 1000.0 - t) <= 0.1)

mode = sys.argv[1] if len(sys.argv) > 1 else "trend"

def counter(name):
    sys.stderr.write("reporter:counter:F1LapTime,%s,1\n" % name)

def load(p):
    with open(p) as fh:
        next(fh)
        return [l.strip().split(",") for l in fh if l.strip()]

tracks = {r[0]: r[1] for r in load("sessions.txt")}
drivers = {(r[0], r[1]): r[2] for r in load("participants.txt")}
path = os.environ.get("mapreduce_map_input_file") or os.environ.get("map_input_file", "")
m = re.search(r"RaceTimeData_(\d+)\.csv", path)
sid = m.group(1) if m else None
track = tracks.get(sid)

for line in sys.stdin:
    if track is None or line.startswith("frameIdentifierStart"):
        continue
    f = line.rstrip("\r\n").split(",")
    try:
        t = float(f[3]); lap = int(f[8])
    except (ValueError, IndexError):
        counter("parse_error"); continue
    if not valid_lap(f, t):
        counter("invalid_laptime"); continue
    if mode == "trend":
        key = "%s|%03d" % (track, lap)
    else:
        d = drivers.get((sid, f[2]))
        if d is None:
            counter("unknown_driver"); continue
        key = "%s|%s" % (track, d)
    print("%s\t%r,1,%r,%r" % (key, t, t, t))
