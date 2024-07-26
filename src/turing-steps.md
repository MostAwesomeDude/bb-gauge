# Steps

This article covers the uncomputable function BB. BB(n,k) is the maximum
number of steps taken by any n-state k-symbol halting Turing machine. As a
historically-important special case, BB(n,2) is [OEIS
A60843](https://oeis.org/A060843), also known as S(n).

## Known Values

BB(1,k) is defined as 1 for all k.

BB(n,k)      | 2 symbols  | 3  | 4
-------------|------------|----|---
**2 states** | 6          | 38 | 3,932,964
**3**        | 21         |    |
**4**        | 107        |    |
**5**        | 47,176,870 |    |

This table is tight in the sense that all unknown cells are bounded by the
hardest open problems in mathematics, known as
[cryptids](https://wiki.bbchallenge.org/wiki/Cryptids).

## Morphett

These machines are given by
[LittlePeng9](https://googology.fandom.com/wiki/User_blog:LittlePeng9/Random_Turing_machines)
and are written for [Morphett's Turing-machine
emulator](https://morphett.info/turing/). Some machines require a non-zero
initial tape, which can be accounted for by appending the length of the
initial tape to the symbol count: we treat them as shorthand for machines
which use one state per symbol to write the initial tape before jumping to
their main algorithm.

Morphett file | Problem | BB(n,k)
---|---|---
catalan-mersenne.tm | Catalan–Mersenne conjecture | 27 + 2, 4
fermat-prime.tm     | Fermat prime conjecture     | 31 + 9, 4
goldbach-ternary.tm | Weak Goldbach conjecture    | 79, 13
goldbach.tm         | Goldbach conjecture         | 54, 4
legendre.tm         | Legendre conjecture         | 30 + 9, 4
odd-perfect.tm      | Odd perfect number          | 79, 13
polya.tm            | Pólya's problem             | 37, 6

## NQL

NQL always compiles to 2-symbol Turing machines.

{{#include nql.md}}
