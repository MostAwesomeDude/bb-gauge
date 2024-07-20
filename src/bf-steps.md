# Steps

This article covers the Busy Brain Beaver function BBB(n) counting the maximum
number of steps taken by non-interactive right-unbounded Brainfuck programs of
length n.

## Definition

A non-interactive Brainfuck program has six instructions: move the head left
and right, increment and decrement the highlighted cell, and start and end
loops. A right-unbounded Brainfuck program only moves to the right of the
starting cell, but has access to an unbounded number of cells. Every single
instruction takes a single step, including loop tests.

## Known Values

Lower bounds for small n are established
[here](https://www.iwriteiam.nl/Ha_bf_numb.html) on a variant of Brainfuck
with unbounded cell values, and are identical up to 255.

We include lower bounds for selected n from [this golfing
challenge](https://codegolf.stackexchange.com/q/4813/123693).

n  | BBB(n)
---|-------
1  | 1
2  | 2
3  | 3
4  | 4
5  | ≥ 7
39 | ≥ 31,919,535,558
41 | ≥ 10 ↑ (10 ↑ 28)
63 | ≥ 255 ↑↑ 2
