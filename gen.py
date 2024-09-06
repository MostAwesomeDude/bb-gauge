from collections import defaultdict, deque
import json
import math
from operator import itemgetter
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

def synthRows(db):
    problems = defaultdict(list)
    for problem, rows in db.items():
        if problem.startswith("Interp("): problems["Universality"].extend(rows)
        else: problems[problem] = rows
    return problems

def makeIntervals1(db, known):
    d = {k: {"start": min(map(itemgetter("value"), l))} for k, l in db.items()}
    d["Known values"] = {"start": 0, "end": known}
    return d

def better(node, candidate):
    nx, ny = node
    cx, cy = candidate
    return (nx == cx and ny < cy) or (nx < cx and ny == cy)
def frontier(nodes):
    ns = list(sorted(nodes))
    return list(filter(lambda node: not any(better(n, node) for n in ns), ns))

def makeIntervals2(db, known):
    d = {k: frontier(map(itemgetter("value"), l)) for k, l in db.items()}
    d["Known values"] = known
    return d

COLORS = "purple", "teal", "peru", "darkslateblue", "seagreen", "saddlebrown",
BG_COLORS = "lavender", "lightcyan", "cornsilk", "lavender", "lightcyan", "cornsilk",
assert len(COLORS) == len(BG_COLORS)

class Canvas:
    def __init__(self, elt): self.elt = elt

    def group(self, attrib):
        return Canvas(ET.SubElement(self.elt, "g", attrib=attrib))

    def entitle(self, s): ET.SubElement(self.elt, "title").text = s

    def circleAt(self, x, y):
        ET.SubElement(self.elt, "circle", attrib={
            "r": "10", "cx": f"{x}", "cy": f"{y}",
        })

    def lineAt(self, x1, y1, x2, y2):
        ET.SubElement(self.elt, "line", attrib={
            "x1": f"{x1}", "y1": f"{y1}",
            "x2": f"{x2}", "y2": f"{y2}",
            "stroke-width": "10",
        })

    def rectAt(self, attrib): ET.SubElement(self.elt, "rect", attrib=attrib)

    def textAt(self, s, attrib):
        ET.SubElement(self.elt, "text", attrib=attrib).text = s

    def arrowAt(self, x, y, pointsLeft=False):
        i = 10 if pointsLeft else -10
        o = -15 if pointsLeft else 15
        ET.SubElement(self.elt, "polygon", attrib={
            "points": f"{x},{y} {x + i},{y - 15} {x + o},{y} {x + i},{y + 15}",
            "stroke-width": "1",
        })

    @classmethod
    def ofSize(cls, width, height):
        return cls(ET.Element("svg", attrib={
            "version": "1.1", "width": str(width), "height": str(height),
            "xmlns": "http://www.w3.org/2000/svg",
        }))

    def finish(self, path):
        with open(path, "w") as handle:
            ET.ElementTree(self.elt).write(handle, encoding="unicode")

# Draw a 1D interval tree.
def writeDiagram1(path, intervals):
    HEIGHT = 100 * (len(intervals) + 1)
    WIDTH = 500
    canvas = Canvas.ofSize(WIDTH, HEIGHT)

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

    def addInterval(i, label, color, bg=None, start=None, end=None):
        g = canvas.group(attrib={
            "transform": f"translate(0 {100 * i})",
            "fill": color, "stroke": color,
        })

        titleStart = "…" if start is None else f"[{start}"
        titleEnd = "…" if end is None else f"{end}]"
        titleDash = "—" if start is None or end is None else "–"
        g.entitle(" ".join([label, titleStart, titleDash, titleEnd]))

        leftOpen = start is None; rightOpen = end is None
        scaleStart = scale(start or 0); scaleEnd = scale(end or MAX)

        if bg is not None:
            width = END_PX if rightOpen else scaleEnd - scaleStart + 100
            g.rectAt(attrib={
                "x": f"{scaleStart - 50}", "y": "5",
                "width": f"{width}", "height": "90",
                "rx": "50", "fill": bg,
            })

        # Delayed in order to put them in front of background.
        g.arrowAt(START_PX, 50, pointsLeft=True) if leftOpen else g.circleAt(scale(start), 50)
        g.arrowAt(END_PX, 50, pointsLeft=False) if rightOpen else g.circleAt(scale(end), 50)

        g.lineAt(scaleStart, 50, scaleEnd, 50)
        labelAbove, labelBelow = splitLabel(label)
        g.textAt(labelAbove, attrib={
            "x": f"{scaleStart}", "y": "25",
            "stroke-width": "1",
        })
        g.textAt(labelBelow, attrib={
            "x": f"{scaleStart}", "y": "80",
            "stroke-width": "1",
        })

    addInterval(0, "n", "black", start=0)
    for i, (k, v) in enumerate(sorted(intervals.items(),
                                      key=lambda t: t[1].get("start", 0))):
        ci = i % len(COLORS)
        addInterval(i + 1, k, COLORS[ci], bg=BG_COLORS[ci], **v)

    canvas.finish(path)

# Draw a 2D interval tree.
def writeDiagram2(path, intervals):
    MAXW = max(t[0] for p in intervals.values() for t in p)
    MAXH = max(t[1] for p in intervals.values() for t in p)
    # Enforce a border of 50 and space for axes.
    WIDTH = 500 + 100
    HEIGHT = int((WIDTH - 200) * math.log(MAXW) / math.log(MAXH)) + 200
    canvas = Canvas.ofSize(WIDTH, HEIGHT)

    def scale(x, y):
        sx = int((WIDTH - 200) * math.log(x) / math.log(MAXW))
        sy = int((HEIGHT - 200) * math.log(y) / math.log(MAXH))
        return sx, sy

    def addInterval(i, nodes, label, color):
        g = canvas.group(attrib={
            # Move inside the border.
            "transform": "translate(150 150)",
            "fill": color, "stroke": color,
        })

        g.entitle(label)

        sx, sy = scale(*nodes[0])
        g.circleAt(sx, sy)
        for x, y in nodes[1:]:
            sx2, sy2 = scale(x, y)
            g.lineAt(sx, sy, sx2, sy2)
            g.circleAt(sx2, sy2)
            sx, sy = sx2, sy2

    for i, (k, v) in enumerate(intervals.items()):
        ci = i % len(COLORS)
        addInterval(i, v, k, COLORS[ci])

    canvas.finish(path)

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
        print("## Tables of Values", file=handle)
        for problem, rows in db.items():
            print("###", problem, file=handle)
            print(f"Source | {label}", file=handle)
            print("---|---", file=handle)
            for d in sorted(rows, key=itemgetter("value", "source")):
                source = d["source"]
                if "url" in d:
                    source = f"[{source}]({d['url']})"
                value = d["value"]
                print(f"{source} | {value}", file=handle)

def loadDB(path):
    with open(path, "r") as handle: d = json.load(handle)
    rows = defaultdict(list)
    for program in d["programs"]:
        problem = program.pop("problem")
        strategy = STRATEGIES[program["strategy"]]
        program["value"] = strategy(program)
        rows[problem].append(program)
    return d["label"], d["known"], rows

def detectDims(db):
    value = next(iter(db.values()))[0]["value"]
    return 1 if isinstance(value, int) else len(value)

def main(argv):
    if len(argv) != 4:
        print("Usage: gen.py <db.json> <table.md> <diagram.svg>")
        return 1
    label, known, db = loadDB(argv[1])
    print("Got DB from", argv[1], f"({label})")
    writeTable(argv[2], label, db)
    print("Wrote table to", argv[2])
    dims = detectDims(db)
    if dims == 1:
        intervals = makeIntervals1(synthRows(db), known)
        writeDiagram1(argv[3], intervals)
        print("Wrote 1D diagram to", argv[3])
    elif dims == 2:
        intervals = makeIntervals2(synthRows(db), known)
        writeDiagram2(argv[3], intervals)
        print("Wrote 2D diagram to", argv[3])
    else:
        print("Can't handle", dims, "dimensions")
        return 1
    return 0

if __name__ == "__main__": raise SystemExit(main(sys.argv))
