from collections import defaultdict
import json, os.path, subprocess, sys

# Read Morphett's syntax from https://morphett.info/turing/turing.html and
# compute statistics for programs.
def morphett(lines):
    states = set()
    symbols = set()
    for line in lines:
        if ";" in line: line = line[:line.index(";")]
        line = line.strip()
        if not line: continue
        cstate, csym, nsym, _, nstate = line.split(" ", 4)
        states.add(cstate); states.add(nstate)
        symbols.add(csym); symbols.add(nsym)
    return states, symbols

def countish(s):
    try: return int(s)
    except ValueError: return s.count(b"\n")

def table(label, path, cmd):
    prefix = cmd.pop()

    with open(path, "r") as handle: d = json.load(handle)

    rows = defaultdict(list)
    for f, row in d.items():
        prog = os.path.join(prefix, f)
        offset = row.get("offset", 0)
        if cmd[0] == "morphett":
            with open(prog, "r") as handle:
                n, k = morphett(handle.read().split("\n"))
                l = len(n) + offset, len(k)
        else:
            p = subprocess.run(cmd + [prog], stdout=subprocess.PIPE)
            l = countish(p.stdout) + offset
        r = f, l, row["problem"], row["source"]
        rows[row["problem"]].append(r)

    best = [min(l, key=lambda t: t[1]) for l in rows.values()]
    print(f"File | {label} | Problem | Source")
    print("---|---|---|---")
    for row in sorted(best, key=lambda k: k[1]):
        print(" | ".join(str(x) for x in row))

if __name__ == "__main__": raise SystemExit(table(sys.argv[1], sys.argv[2], sys.argv[3:]))
