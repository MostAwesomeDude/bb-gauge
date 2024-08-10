# XXX for testing
import time; before = time.perf_counter()

theorems = [
    ("0", "0"), # id_0
    ("1", "1"), # id_1
    ("N", "N"), # id_N
    ("1", "N"), # zero
]

# XXX would not be in the actual TM
cache = {t: i for i, t in enumerate(theorems)}

# XXX liveness check
counter = 0
def find(x, y):
    # XXX cache
    if (x, y) in cache: return
    cache[x, y] = len(theorems)
    theorems.append((x, y))
    # XXX liveness
    global counter; counter += 1
    if counter == 1000000: counter = 0; print("Most recent:", x, "→", y)
    if x == "1" and y == "0": raise Exception("halt")

def comp(x, y, z, w):
    if y != z: return
    find(x, w)

def ignore(x, y): find(y, "1")
def trivial(x, y): find("0", x)

def pair(x, y, z, w):
    if x != z: return
    find(x, ("p", y, w))

def fst(x, y):
    if y[0] != "p": return
    find(x, y[1])

def snd(x, y):
    if y[0] != "p": return
    find(x, y[2])

def case(x, y, z, w):
    if y != w: return
    find(("s", x, z), y)

def left(x, y):
    if x[0] != "s": return
    find(x[1], y)

def right(x, y):
    if x[0] != "s": return
    find(x[2], y)

def curry(x, y):
    if x[0] != "p": return
    find(x[1], ("f", x[1], y))

def uncurry(x, y):
    if y[0] != "f": return
    find(("p", x, y[1]), y[2])

def choice(x, y, z, w):
    if x != "1" or y != z: return
    find(w, z)

# XXX for testing
rounds = 4
while rounds:
    rounds -= 1
    l = len(theorems)
    for i in range(l):
        x, y = theorems[i]
        ignore(x, y); trivial(x, y); fst(x, y); snd(x, y); left(x, y); right(x, y); curry(x, y); uncurry(x, y)
    for i in range(l):
        for j in range(l):
            x, y = theorems[i]
            z, w = theorems[j]
            comp(x, y, z, w); pair(x, y, z, w); case(x, y, z, w); choice(x, y, z, w)
    print("Ending round with", len(theorems), "signatures")
after = time.perf_counter(); elapsed = after - before
print("Took", elapsed, "seconds;", int(len(theorems) / elapsed), "theorems/s")
