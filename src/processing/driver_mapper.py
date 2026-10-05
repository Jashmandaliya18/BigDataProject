#!/usr/bin/env python3
"""Driver performance mapper. Output: driver <TAB> sum,sumsq,n,min,max"""
import sys, os, re

def counter(name):
    sys.stderr.write("reporter:counter:F1Driver,%s,1\n" % name)

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

parts = {}
with open("participants.txt") as fh:
    next(fh)
    for l in fh:
        r = l.strip().split(",")
        if len(r) == 4:
            parts[(r[0], r[1])] = r[2]

path = os.environ.get("mapreduce_map_input_file") or os.environ.get("map_input_file", "")
m = re.search(r"RaceTimeData_(\d+)\.csv", path)
sid = m.group(1) if m else None

rows = [l.rstrip("\r\n").split(",") for l in sys.stdin
        if not l.startswith("frameIdentifierStart") and l.strip()]
med = median_of_complete(rows)

for f in rows:
    if sid is None:
        break
    try:
        t = float(f[3])
    except (ValueError, IndexError):
        counter("parse_error"); continue
    if not complete(f, t):
        counter("invalid_laptime"); continue
    if med is not None and abs(t - med) > 0.15 * med:
        counter("outlier_laptime"); continue
    driver = parts.get((sid, f[2]))
    if driver is None:
        counter("unknown_driver"); continue
    print("%s\t%r,%r,1,%r,%r" % (driver, t, t * t, t, t))
    counter("laps_emitted")
