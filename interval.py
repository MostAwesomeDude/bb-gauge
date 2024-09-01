# Draw a 1D interval tree.

from collections import deque
import json
import math
import sys
from xml.etree import ElementTree as ET

with open(sys.argv[-1], "r") as handle: d = json.load(handle)

HEIGHT = 100 * (len(d) + 1)
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
MAX = max(max(v.values()) for v in d.values()) + (max(map(len, d)) >> 1)
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

def arrowAt(g, x, y, pointsLeft=False):
    i = 10 if pointsLeft else -10
    o = -15 if pointsLeft else 15
    ET.SubElement(g, "polygon", attrib={
        "points": f"{x},{y} {x + i},{y - 15} {x + o},{y} {x + i},{y + 15}",
        "stroke-width": "1",
    })

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
    mid = (scaleEnd + scaleStart) >> 1
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
for i, (k, v) in enumerate(sorted(d.items(),
                                  key=lambda t: t[1].get("start", 0))):
    ci = i % len(COLORS)
    addInterval(i + 1, k, COLORS[ci], bg=BG_COLORS[ci], **v)

ET.ElementTree(root).write(sys.stdout, encoding="unicode")
