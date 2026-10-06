#!/usr/bin/env python3
"""Job 5a mapper. Input: cleaned telemetry. Emits only frames with pitStatus != none.
Key track|driver|session|lap(3 digits), value tyre compound."""
import sys
for line in sys.stdin:
    f = line.rstrip("\n").split(",")
    if len(f) != 17 or f[13] == "none":
        continue
    try:
        lap = int(f[5])
    except ValueError:
        continue
    print("%s|%s|%s|%03d\t%s" % (f[1], f[2], f[0], lap, f[12]))
