#!/usr/bin/env python3
"""Usage: laptime_mapper.py trend|fastest. Value: sum,count,min,max"""
import sys, os, re

mode = sys.argv[1] if len(sys.argv) > 1 else "trend"

def counter(name):
    sys.stderr.write("reporter:counter:F1LapTime,%s,1\n" % name)

def complete(f, t):
    try:
        s1, s2, s3 = int(f[4]), int(f[5]), int(f[6])
    except (ValueError, IndexError):
        return False
    return (30 <= t <= 300 and min(s1, s2, s3) >= 10000
            and abs((s1 + s2 + s3) / 1000.0 - t) <= 0.1)

def median_of_complete(rows):
    vals = []
    for f in rows:
        try:
            t = float(f[3])
        except (ValueError, IndexError):
            continue
        if complete(f, t):
            vals.append(t)
    vals.sort()
    return vals[len(vals) // 2] if vals else None

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

rows = [l.rstrip("\r\n").split(",") for l in sys.stdin
        if not l.startswith("frameIdentifierStart") and l.strip()]
med = median_of_complete(rows)

for f in rows:
    if track is None:
        break
    try:
        t = float(f[3]); lap = int(f[8])
    except (ValueError, IndexError):
        counter("parse_error"); continue
    if not complete(f, t):
        counter("invalid_laptime"); continue
    if med is not None and abs(t - med) > 0.15 * med:
        counter("outlier_laptime"); continue
    if mode == "trend":
        key = "%s|%03d" % (track, lap)
    else:
        d = drivers.get((sid, f[2]))
        if d is None:
            counter("unknown_driver"); continue
        key = "%s|%s" % (track, d)
    print("%s\t%r,1,%r,%r" % (key, t, t, t))
