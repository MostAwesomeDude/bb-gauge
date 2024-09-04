# Steps

This article covers the uncomputable function BB. BB(n,k) is the maximum
number of steps taken by any n-state k-symbol halting Turing machine. As a
historically-important special case, BB(n,2) is [OEIS
A60843](https://oeis.org/A060843), also known as S(n).

Some machines require a non-zero initial tape, which can be accounted for by
appending the length of the initial tape to the symbol count: we treat them as
shorthand for machines which use one state per symbol to write the initial tape
before jumping to their main algorithm.

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

{{#include turing.md}}
