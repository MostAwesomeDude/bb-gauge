from collections import defaultdict, deque
import json
import math
import os.path
import subprocess
import sys
from xml.etree import ElementTree as ET

import framework, nqlast, nqlgrammar

# Split a label into two roughly-equal halves for two rows of text.
def splitLabel(s):
    pieces = deque(s.split())
    l = []; r = []; ll = 0; lr = 0
    while pieces:
        if ll < lr:
            p = pieces.popleft()
            l.append(p)
            ll += len(p) + 1
        else:
            p = pieces.pop()
            r.append(p)
            lr += len(p) + 1
    r.reverse()
    return " ".join(l), " ".join(r)

def arrowAt(g, x, y, pointsLeft=False):
    i = 10 if pointsLeft else -10
    o = -15 if pointsLeft else 15
    ET.SubElement(g, "polygon", attrib={
        "points": f"{x},{y} {x + i},{y - 15} {x + o},{y} {x + i},{y + 15}",
        "stroke-width": "1",
    })

# Draw a 1D interval tree.
def writeDiagram(path, intervals):
    HEIGHT = 100 * (len(intervals) + 1)
    WIDTH = 500
    root = ET.Element("svg", attrib={
        "version": "1.1", "width": str(WIDTH), "height": str(HEIGHT),
        "xmlns": "http://www.w3.org/2000/svg",
    })

    # COLORS = "plum", "paleturquoise", "palegoldenrod", "palegreen", "cornflowerblue",
    # BG_COLORS = "darkslategrey", "dimgrey", "dimgrey", "dimgrey", "black",
    COLORS = "purple", "teal", "peru", "darkslateblue", "seagreen", "saddlebrown",
    BG_COLORS = "lavender", "lightcyan", "cornsilk", "lavender", "lightcyan", "cornsilk",
    assert len(COLORS) == len(BG_COLORS)

    # Added term is extra space for positioning text on shortest line.
    MAX = max(max(v.values()) for v in intervals.values()) + (max(map(len, intervals)) >> 1)
    # Multiplied factor is to get an extra order-of-magnitude-ish space on the
    # right of the diagram.
    MAX = int(MAX * math.e * math.e)

    START_PX = 50
    END_PX = WIDTH - START_PX
    SCALE_PX = END_PX - START_PX
    def scale(x):
        offset = 0 if x == 0 else int(SCALE_PX * math.log(x) / math.log(MAX))
        return offset + START_PX

    def circleAt(g, x, y):
        ET.SubElement(g, "circle", attrib={
            "r": "10", "cx": f"{scale(x)}", "cy": f"{y}",
        })

    def addInterval(i, label, color, bg=None, start=None, end=None):
        g = ET.SubElement(root, "g", attrib={
            "fill": color, "stroke": color,
        })
        y = 100 * i + 50

        titleStart = "…" if start is None else f"[{start}"
        titleEnd = "…" if end is None else f"{end}]"
        titleDash = "—" if start is None or end is None else "–"
        ET.SubElement(g, "title").text = " ".join([
            label, titleStart, titleDash, titleEnd,
        ])

        leftOpen = start is None; rightOpen = end is None
        scaleStart = scale(start or 0); scaleEnd = scale(end or MAX)

        if bg is not None:
            width = END_PX if rightOpen else scaleEnd - scaleStart + 100
            ET.SubElement(g, "rect", attrib={
                "x": f"{scaleStart - 50}", "y": f"{y - 45}",
                "width": f"{width}", "height": "90",
                "rx": "50", "fill": bg,
            })

        # Delayed in order to put them in front of background.
        arrowAt(g, START_PX, y, pointsLeft=True) if leftOpen else circleAt(g, start, y)
        arrowAt(g, END_PX, y, pointsLeft=False) if rightOpen else circleAt(g, end, y)

        ET.SubElement(g, "line", attrib={
            "x1": f"{scaleStart}", "y1": f"{y}",
            "x2": f"{scaleEnd}", "y2": f"{y}",
            "stroke-width": "10",
        })
        # mid = (scaleEnd + scaleStart) >> 1
        # xText = max(START_PX, mid - 2 * len(label))
        labelAbove, labelBelow = splitLabel(label)
        ET.SubElement(g, "text", attrib={
            "x": f"{scaleStart}", "y": f"{y - 25}",
            "stroke-width": "1",
        }).text = labelAbove
        ET.SubElement(g, "text", attrib={
            "x": f"{scaleStart}", "y": f"{y + 30}",
            "stroke-width": "1",
        }).text = labelBelow

    addInterval(0, "n", "black", start=0)
    for i, (k, v) in enumerate(sorted(intervals.items(),
                                      key=lambda t: t[1].get("start", 0))):
        ci = i % len(COLORS)
        addInterval(i + 1, k, COLORS[ci], bg=BG_COLORS[ci], **v)

    with open(path, "w") as handle:
        ET.ElementTree(root).write(handle, encoding="unicode")

def countBLC(d):
    cmd = ["blc", "size", os.path.join("blc", d["params"])]
    return int(subprocess.run(cmd, stdout=subprocess.PIPE).stdout)

def countBF(d):
    path = os.path.join("bf-clean", d["params"])
    with open(path, "r") as handle: s = handle.read()
    return sum(c in "+-<>[].," for c in s)

# Read Morphett's syntax from https://morphett.info/turing/turing.html and
# compute statistics for programs.
def countMorphett(d):
    path, offset = d["params"]
    with open(os.path.join("turing-morphett", path), "r") as handle:
        lines = handle.read().split("\n")
    states = set()
    symbols = set()
    for line in lines:
        if ";" in line: line = line[:line.index(";")]
        line = line.strip()
        if not line: continue
        cstate, csym, nsym, _, nstate = line.split(" ", 4)
        states.add(cstate); states.add(nstate)
        symbols.add(csym); symbols.add(nsym)
    return len(states) + offset, len(symbols)

class NQLArgs:
    def __getattr__(self, attr): return False
NQL_ARGS = NQLArgs()

def countNQL(d):
    path = os.path.join("nql", d["params"])
    # The following sequence is just an expansion of NQL's top-level harness.
    ast, = nqlgrammar.grammar.parseFile(path, parseAll=True)
    # Estimate required order.
    mast = nqlast.AstMachine(ast, NQL_ARGS)
    # XXX magic number
    mast.pc_bits = 50
    order = mast.main().order
    # Use estimate for actual compilation.
    mast = nqlast.AstMachine(ast, NQL_ARGS)
    mast.pc_bits = order
    machine = framework.Machine(mast)
    machine.compress()
    return len(machine.reachable()), 2

STRATEGIES = {
    "blc": countBLC,
    "brainfuck": countBF,
    "morphett": countMorphett,
    "nql": countNQL,
    "params": lambda d: tuple(d["params"]),
}

def writeTable(path, label, db):
    with open(path, "w") as handle:
        print(f"Problem | Source | {label}", file=handle)
        print("---|---|---", file=handle)
        for problem, rows in db.items():
            for d in rows:
                source = d["source"]
                if "url" in d:
                    source = f"[{source}]({d['url']})"
                value = d["value"]
                print(f"{problem} | {source} | {value}", file=handle)

def makeIntervals(db, known):
    # Synthetic rows.
    problems = defaultdict(list)
    for problem, rows in db.items():
        if problem.startswith("Interp("): problems["Universality"].extend(rows)
        else: problems[problem] = rows

    key = lambda t: t["value"]
    d = {}
    d["Known values"] = {"start": 0, "end": known}
    d.update({k: {"start": min(map(key, l))} for k, l in problems.items()})
    return d

def loadDB(path):
    with open(path, "r") as handle: d = json.load(handle)
    rows = defaultdict(list)
    for program in d["programs"]:
        problem = program.pop("problem")
        strategy = STRATEGIES[program["strategy"]]
        program["value"] = strategy(program)
        rows[problem].append(program)
    return d["label"], d["known"], rows

def main(argv):
    if len(argv) != 4:
        print("Usage: gen.py <db.json> <table.md> <diagram.svg>")
        return 1
    label, known, db = loadDB(argv[1])
    print("Got DB from", argv[1], f"({label})")
    writeTable(argv[2], label, db)
    print("Wrote table to", argv[2])
    intervals = makeIntervals(db, known)
    # XXX
    if "turing" not in argv[3]: writeDiagram(argv[3], intervals)
    print("Wrote diagram to", argv[3])
    return 0

if __name__ == "__main__": raise SystemExit(main(sys.argv))
