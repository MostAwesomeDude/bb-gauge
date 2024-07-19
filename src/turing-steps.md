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
hardest open problems in mathematics.

## NQL

NQL always compiles to 2-symbol Turing machines.

NQL file | BB(n,2)
---|---
