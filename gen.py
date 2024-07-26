from collections import defaultdict
import json, os.path, subprocess, sys

def countish(s):
    try: return int(s)
    except ValueError: return s.count(b"\n")

def table(label, path, cmd):
    prefix = cmd.pop()

    with open(path, "r") as handle: d = json.load(handle)

    rows = defaultdict(list)
    for k, row in d.items():
        prog = os.path.join(prefix, k)
        p = subprocess.run(cmd + [prog], stdout=subprocess.PIPE)
        n = countish(p.stdout)
        rows[row["problem"]].append((k, n, row["problem"], row["source"]))

    best = [min(l, key=lambda t: t[1]) for l in rows.values()]
    print(f"File | {label} | Problem | Source")
    print("---|---|---|---")
    for row in sorted(best, key=lambda k: k[1]):
        print(" | ".join(str(x) for x in row))

if __name__ == "__main__": raise SystemExit(table(sys.argv[1], sys.argv[2], sys.argv[3:]))
