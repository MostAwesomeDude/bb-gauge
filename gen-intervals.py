from collections import defaultdict
import json, os.path, subprocess, sys

def countish(s):
    try: return int(s)
    except ValueError: return s.count(b"\n")

def table(known, path, cmd):
    prefix = cmd.pop()

    with open(path, "r") as handle: d = json.load(handle)

    raw_rows = defaultdict(list)
    for k, row in d.items():
        prog = os.path.join(prefix, k)
        p = subprocess.run(cmd + [prog], stdout=subprocess.PIPE)
        n = countish(p.stdout)
        raw_rows[row["problem"]].append((k, n, row["problem"], row["source"]))
    # Synthetic rows.
    rows = defaultdict(list)
    for row in raw_rows:
        if row.startswith("Interp("): rows["Universality"].extend(raw_rows[row])
        else: rows[row] = raw_rows[row]

    key = lambda t: t[1]
    d = {}
    d["Known values"] = {"start": 0, "end": int(known)}
    d.update({k: {"start": min(map(key, l))} # "end": max(map(key, l))}
              for k, l in rows.items()})
    json.dump(d, sys.stdout)
    return 0

if __name__ == "__main__": raise SystemExit(table(sys.argv[1], sys.argv[2], sys.argv[3:]))
