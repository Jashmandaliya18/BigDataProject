#!/usr/bin/env python3
"""Job 5b mapper. Input: output of job 5a (track|driver|session|lap <TAB> frames <TAB> tyres).
Emits key track|driver, value lap,frames so the reducer can merge consecutive laps into one stop."""
import sys
for line in sys.stdin:
    p = line.rstrip("\n").split("\t")
    if len(p) != 3:
        continue
    k = p[0].split("|")
    try:
        lap, frames = int(k[3]), int(p[1])
    except (ValueError, IndexError):
        continue
    print("%s|%s\t%d,%d" % (k[0], k[1], lap, frames))
