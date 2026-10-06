#!/usr/bin/env python3
"""Load MapReduce outputs from HDFS into MongoDB (db f1db). Run inside master.
Field suffix :s string, :i int, :f float. A name starting with _ is dropped."""
import subprocess
from pymongo import MongoClient

LAP = ["laps:i", "avg_lap:f", "fastest:f", "slowest:f"]
SPD = ["samples:i", "avg_speed:f", "min_speed:f", "max_speed:f"]

SPECS = [
    ("driver_stats",    "/f1/output/driver",          ["driver:s"], ["laps:i", "avg_lap:f", "best_lap:f", "worst_lap:f", "std:f"]),
    ("lap_trend",       "/f1/output/lap_trend",       ["track:s", "lap:i"], LAP),
    ("lap_fastest",     "/f1/output/lap_fastest",     ["track:s", "driver:s"], LAP),
    ("circuit_laptime", "/f1/output/circuit_laptime", ["track:s"], LAP),
    ("circuit_speed",   "/f1/output/circuit_speed",   ["track:s"], SPD),
    ("speed_driver",    "/f1/output/speed_driver",    ["track:s", "driver:s"], SPD),
    ("speed_band",      "/f1/output/speed_band",      ["track:s", "band:i"], ["samples:i", "_a:f", "_b:f", "_c:f"]),
    ("tyre_speed",      "/f1/output/speed_tyre",      ["tyre:s"], SPD),
    ("pit_laps",        "/f1/output/pit_laps",        ["track:s", "driver:s", "session:s", "lap:i"], ["frames:i", "tyres:s"]),
    ("pit_stops",       "/f1/output/pit_summary",     ["track:s", "driver:s"], ["stops:i", "avg_frames:f", "min_frames:f", "max_frames:f"]),
]

def cast(v, t):
    return int(v) if t == "i" else float(v) if t == "f" else v

def read_hdfs(path):
    r = subprocess.run(["hdfs", "dfs", "-cat", path + "/part-*"], capture_output=True)
    return None if r.returncode != 0 else r.stdout.decode("utf-8").splitlines()

db = MongoClient("mongodb://mongodb:27017")["f1db"]
for coll, path, keys, vals in SPECS:
    lines = read_hdfs(path)
    if lines is None:
        print("SKIP %-16s (missing %s)" % (coll, path)); continue
    docs, bad = [], 0
    for line in lines:
        p = line.split("\t")
        k = p[0].split("|")
        if len(k) != len(keys) or len(p) - 1 != len(vals):
            bad += 1; continue
        d = {}
        try:
            for name, v in zip(keys, k):
                n, t = name.split(":"); d[n] = cast(v, t)
            for name, v in zip(vals, p[1:]):
                n, t = name.split(":")
                if not n.startswith("_"):
                    d[n] = cast(v, t)
        except ValueError:
            bad += 1; continue
        docs.append(d)
    db[coll].drop()
    if docs:
        db[coll].insert_many(docs)
        for field in ("driver", "track"):
            if field in docs[0]:
                db[coll].create_index(field)
    print("LOAD %-16s %6d docs (%d bad lines)" % (coll, len(docs), bad))
