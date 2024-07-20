# Read Morphett's syntax from https://morphett.info/turing/turing.html and
# compute statistics for programs.

import sys

def go(lines):
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

def main(argv):
    for arg in argv[1:]:
        with open(arg, "r") as handle: lines = handle.read().split("\n")
        states, symbols = go(lines)
        print("File:", arg,
              "Number of states:", len(states),
              "Number of symbols:", len(symbols))
        # print("States:", *states); print("Symbols:", *symbols)
    return 0

if __name__ == "__main__": raise SystemExit(main(sys.argv))
