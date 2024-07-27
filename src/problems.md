# Problems

In order to calibrate any busy beaver gauge, we must first define a common
set of problems. A problem must be:

* Semidecidable: either proof search or disproof search must terminate once
  the first theorem or counterexample is found
* Arithmetic: it is either true or false of the natural numbers
* Encodable: we know how to express it as a low-level bookkeeping computation
* Meaningful: an affirmative or negative answer to the problem would advance
  the art of mathematics

## Solved problems

Some problems are no longer open, but they are still useful as gauges since
they can give bounds for busy beavers.

### Pólya's problem

Let *n* be some upper bound. Do more than half of the natural numbers less
than *n* have an odd number of prime factors? Pólya noticed in 1919 that, if
true, this statement would imply the Riemann hypothesis. Haselgrove showed in
1958 that the statement is false, and Tanaka found that it is first false for
*n* = 906,150,257 in [Tanaka
1980](https://doi.org/10.3836%2Ftjm%2F1270216093).

See also [WP](https://en.wikipedia.org/wiki/P%C3%B3lya_conjecture).

## Natural Numbers

We will always have open questions about the natural numbers.

### Catalan–Mersenne conjecture

Are there a finite number of Catalan–Mersenne primes; does [OEIS
A7013](https://oeis.org/A007013) contain any composite numbers? Catalan
conjectured this in 1876 while editing a letter from Lucas.

See also [WP](https://en.wikipedia.org/wiki/Double_Mersenne_number).

### Collatz conjecture

Does the graph of the [Collatz
function](https://en.wikipedia.org/wiki/Collatz_conjecture) have multiple
[strongly-connected
components](https://en.wikipedia.org/wiki/Strongly_connected_component)?
Equivalently, does every natural number map to one under some number of
iterations of the Collatz function? Collatz may have first introduced the
function in 1937.

See also [WP](https://en.wikipedia.org/wiki/Collatz_conjecture).

### Erdős–Lagarias conjecture

Let *k* > 8. Can any *k*'th power of two be written as a sum of distinct
powers of three; is any *k*'th power of two expressible in ternary with only
the digits 0 and 1? Erdős conjectured that there is no such *k* and Lagarias
studied the problem in [Lagarias 2005](https://arxiv.org/abs/math/0512006).

### Fermat prime conjecture

Is there a sixth Fermat prime? Fermat conjectured that all Fermat numbers are
prime, but Euler showed that the sixth Fermat number *F*₅ is composite in
1732.

See also [WP](https://en.wikipedia.org/wiki/Fermat_number).

### Goldbach conjecture

Aside from two, is every even number a sum of two prime numbers? Goldbach
claimed this in a 1742 letter to Euler.

See also [WP](https://en.wikipedia.org/wiki/Goldbach%27s_conjecture).

#### Weak Goldbach conjecture

Aside from one, three, and five; is every odd number a sum of three prime
numbers? This statement is a strict weakening of the Goldbach conjecture. A
proof was proposed in [Helfgott 2013](https://arxiv.org/abs/1312.7748) but has
not yet been accepted by the community.

### Legendre conjecture

For all positive *n*, is there a prime number between *n*² and (*n* + 1)²?
Legendre investigated this question.

See also [WP](https://en.wikipedia.org/wiki/Legendre%27s_conjecture).

### Odd perfect number

Are any perfect numbers odd? The earliest examination of this question is
unknown but may have been by Euclid or Nicomachus of Gerasa.

See also [WP](https://en.wikipedia.org/wiki/Perfect_number).

### Period 32 Laver table

Is there a Laver table with period 32; does 32 appear in [OEIS
A98820](https://oeis.org/A098820)? Laver showed in [Laver
1995](https://doi.org/10.1006%2Faima.1995.1014) that a Laver table exists for
any power-of-two period, given ZFC plus the axiom that an I3 rank-into-rank
cardinal exists.

See also [WP](https://en.wikipedia.org/wiki/Laver_table). A collection of
attempts at encoding this problem can be found at [Code Golf Stack
Exchange](https://codegolf.stackexchange.com/q/79620/123693).

### Riemann hypothesis

Do all non-trivial zeros of Riemann's zeta function have real part 1/2?
Riemann guessed that all non-trivial zeros are real in 1859, and it is known
that all non-trivial zeros have real parts in [0,1].

Equivalently, as given by Robin in 1984 and explained by [Lagarias
2001](https://arxiv.org/abs/math/0008177), let H(*n*) denote the *n*'th
harmonic number; is the sum of divisors of *n* always smaller than H(*n*) +
exp(H(*n*)) × ln(H(*n*))?

See also [WP](https://en.wikipedia.org/wiki/Riemann_hypothesis),
[nLab](https://ncatlab.org/nlab/show/Riemann+hypothesis).

## Consistency

For any formal system with a notion of negation, antimony, or contradiction;
we may ask whether it is **consistent**: whether the system fails to prove any
pair of mutually-exclusive statements. When phrased in terms of
semidecidability, consistency problems are often a form of proof search, since
it can be shown that searching for one specific sort of contradiction can be
sufficient to find all contradictions.

Theories which have been investigated include:

* PA ([WP](https://en.wikipedia.org/wiki/Peano_axioms),
  [nLab](https://ncatlab.org/nlab/show/Peano+arithmetic))
* ZF, ZFC
  ([WP](https://en.wikipedia.org/wiki/Zermelo%E2%80%93Fraenkel_set_theory),
  [nLab](https://ncatlab.org/nlab/show/ZFC))

## Notes

### Style

* We denote open conjectures and hypotheses with non-possessive labels. This
  is both to recognize a lack of primacy, as anybody can speculate on
  interesting matters, and a lack of proof, as we normally celebrate the
  effort required to prove a statement above the effort required merely to
  state it.
