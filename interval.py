# Draw a 1D interval tree.

import json
import sys
from xml.etree import ElementTree as ET

with open(sys.argv[-1], "r") as handle: d = json.load(handle)

HEIGHT = 100 * (len(d) + 1)
WIDTH = 500
root = ET.Element("svg", attrib={
    "version": "1.1", "width": str(WIDTH), "height": str(HEIGHT),
    "xmlns": "http://www.w3.org/2000/svg",
})

COLORS = "black", "red", "blue", "green",

# Added term is extra space for positioning text below shortest line.
MAX = max(max(v.values()) for v in d.values()) + (max(map(len, d)) >> 1)

START_PX = 50
END_PX = WIDTH - START_PX
SCALE_PX = END_PX - START_PX
def scale(x): return SCALE_PX * x // MAX + START_PX

def addInterval(i, label, start=None, end=None):
    color = COLORS[i % len(COLORS)]
    g = ET.SubElement(root, "g", attrib={
        "fill": color, "stroke": color,
    })
    y = 100 * i + 50
    def circleAt(x):
        ET.SubElement(g, "circle", attrib={
            "r": "10", "cx": str(scale(x)), "cy": f"{y}",
        })
    def arrowAt(x, pointsLeft=False):
        i = 10 if pointsLeft else -10
        o = -15 if pointsLeft else 15
        ET.SubElement(g, "polygon", attrib={
            "points": f"{x},{y} {x + i},{y - 15} {x + o},{y} {x + i},{y + 15}",
            "stroke-width": "1",
        })

    titleStart = "…" if start is None else f"[{start}"
    titleEnd = "…" if end is None else f"{end}]"
    titleDash = "—" if start is None or end is None else "–"
    ET.SubElement(g, "title").text = " ".join([
        label, titleStart, titleDash, titleEnd,
    ])

    if start is None:
        start = 0
        arrowAt(START_PX, pointsLeft=True)
    else: circleAt(start)
    if end is None:
        end = MAX
        arrowAt(END_PX, pointsLeft=False)
    else: circleAt(end)

    ET.SubElement(g, "line", attrib={
        "x1": str(scale(start)), "y1": f"{y}",
        "x2": str(scale(end)), "y2": f"{y}",
        "stroke-width": "10",
    })
    mid = scale((end + start) >> 1)
    ET.SubElement(g, "text", attrib={
        "x": f"{mid - 4 * len(label)}", "y": f"{y + 30}",
        "stroke-width": "1",
    }).text = label

addInterval(0, "n", start=0)
for i, (k, v) in enumerate(d.items(), start=1): addInterval(i, k, **v)

ET.ElementTree(root).write(sys.stdout, encoding="unicode")
