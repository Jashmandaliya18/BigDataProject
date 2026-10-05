#!/usr/bin/env python3
"""Driver performance mapper. Input: RaceTimeData CSV. Output: driver <TAB> sum,sumsq,n,min,max"""
import sys, os, re

def counter(name):
    sys.stderr.write("reporter:counter:F1Driver,%s,1\n" % name)

with open("participants.txt") as fh:
    next(fh)
    parts = {}
    for l in fh:
        r = l.strip().split(",")
        if len(r) == 4:
            parts[(r[0], r[1])] = r[2]

path = os.environ.get("mapreduce_map_input_file") or os.environ.get("map_input_file", "")
m = re.search(r"RaceTimeData_(\d+)\.csv", path)
sid = m.group(1) if m else None

for line in sys.stdin:
    if sid is None or line.startswith("frameIdentifierStart"):
        continue
    f = line.rstrip("\r\n").split(",")
    try:
        t = float(f[3])
    except (ValueError, IndexError):
        counter("parse_error"); continue
    if not (30 <= t <= 300):
        counter("invalid_laptime"); continue
    driver = parts.get((sid, f[2]))
    if driver is None:
        counter("unknown_driver"); continue
    print("%s\t%r,%r,1,%r,%r" % (driver, t, t * t, t, t))
    counter("laps_emitted")
