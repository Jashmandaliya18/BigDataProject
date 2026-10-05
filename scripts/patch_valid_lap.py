import re
FUNC = '''
def valid_lap(f, t):
    """Complete lap: 3 sectors > 0 and sector sum matches LapTime (+-0.1 s)."""
    try:
        s1, s2, s3 = int(f[4]), int(f[5]), int(f[6])
    except (ValueError, IndexError):
        return False
    return (30 <= t <= 300 and s1 > 0 and s2 > 0 and s3 > 0
            and abs((s1 + s2 + s3) / 1000.0 - t) <= 0.1)
'''
base = "/project/src/processing/"
for name in ["driver_mapper.py", "laptime_mapper.py", "circuit_laptime_mapper.py"]:
    src = open(base + name).read()
    if "def valid_lap" in src:
        print(name, "already patched"); continue
    src = src.replace("if not (30 <= t <= 300):", "if not valid_lap(f, t):")
    src = src.replace("if 30 <= t <= 300:", "if valid_lap(f, t):")
    src = re.sub(r"(^import sys[^\n]*\n)", lambda m: m.group(1) + FUNC, src, count=1, flags=re.M)
    open(base + name, "w").write(src)
    print(name, "patched")
