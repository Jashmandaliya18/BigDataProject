#!/usr/bin/env python3
"""Map-only cleaning job for TelemetryData.
Joins session/participant lookups (shipped via -files), validates rows,
keeps 17 useful columns. Output CSV columns:
0 session,1 track,2 driver,3 team,4 pilot,5 lapNum,6 speed,7 throttle,8 brake,
9 gear,10 rpm,11 drs,12 tyreCompound,13 pitStatus,14 carPosition,15 lapDistance,16 currentLapTime
"""
import sys, os, re

def counter(name):
    sys.stderr.write("reporter:counter:F1Clean,%s,1\n" % name)

def load(path):
    with open(path) as fh:
        next(fh)
        return [l.strip().split(",") for l in fh if l.strip()]

sessions = {r[0]: r[1] for r in load("sessions.txt")}
parts = {(r[0], r[1]): (r[2], r[3]) for r in load("participants.txt")}

path = os.environ.get("mapreduce_map_input_file") or os.environ.get("map_input_file", "")
m = re.search(r"TelemetryData_(\d+)\.csv", path)
sid = m.group(1) if m else None
track = sessions.get(sid)

for line in sys.stdin:
    if line.startswith("sessionTime"):
        continue
    if track is None:
        counter("no_session_match"); continue
    f = line.rstrip("\r\n").split(",")
    if len(f) != 56:
        counter("bad_column_count"); continue
    try:
        speed, thr, brk = float(f[21]), float(f[22]), float(f[24])
        lap = int(f[49]); float(f[26]); float(f[27]); float(f[48]); float(f[50])
    except ValueError:
        counter("parse_error"); continue
    if not (0 <= speed <= 400 and 0 <= thr <= 1 and 0 <= brk <= 1 and lap >= 1):
        counter("out_of_range"); continue
    driver, team = parts.get((sid, f[2]), ("Unknown", "Unknown"))
    pit = f[52] if f[52] else "none"
    print(",".join([sid, track, driver, team, f[2], f[49], f[21], f[22], f[24],
                    f[26], f[27], f[28], f[40] or "unknown", pit, f[47], f[50], f[48]]))
    counter("rows_kept")
