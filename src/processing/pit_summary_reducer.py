#!/usr/bin/env python3
"""Job 5b reducer. Merges pit-lane frames on consecutive laps into one stop.
Visits < MIN_FRAMES are noise; visits > MAX_FRAMES are cars parked in the pit area (not stops).
Output: track|driver <TAB> stops <TAB> avg_frames <TAB> min_frames <TAB> max_frames"""
import sys
MIN_FRAMES, MAX_FRAMES = 10, 2000
cur, visits = None, []

def counter(n):
    sys.stderr.write("reporter:counter:F1Pit,%s,1\n" % n)

def emit():
    if cur is None:
        return
    visits.sort()
    stops, last = [], None
    for lap, fr in visits:
        if last is not None and lap - last == 1:
            stops[-1] += fr
        else:
            stops.append(fr)
        last = lap
    good = []
    for s in stops:
        if s < MIN_FRAMES:
            counter("short_visit_ignored")
        elif s > MAX_FRAMES:
            counter("stuck_in_pit_ignored")
        else:
            good.append(s)
    if good:
        print("%s\t%d\t%.3f\t%d\t%d" % (cur, len(good), sum(good) / len(good), min(good), max(good)))

for line in sys.stdin:
    k, v = line.rstrip("\n").split("\t")
    lap, fr = v.split(",")
    if k != cur:
        emit()
        cur, visits = k, []
    visits.append((int(lap), int(fr)))
emit()
