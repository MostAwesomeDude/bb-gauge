# Future Directions

What should we document next?

## Problems

Found by surveying Wikipedia and also from [Code Golf Stack
Exchange](https://codegolf.stackexchange.com/q/97004/123693).

* [Brocard conjecture](https://en.wikipedia.org/wiki/Brocard's_conjecture):
  For all prime numbers *p* ≥ 5 and *q* the next prime after *p*, is it the
  case that there are at least four prime numbers between *p*² and *q*²? Note
  that while Brocard's name is attached to this, I don't have evidence that
  they are the conjecturer. There is a clear similarity to the Legendre
  conjecture, although they are not directly connected.
* [Brocard–Ramanujan
  conjecture](https://en.wikipedia.org/wiki/Brocard%27s_problem), also called
  "Brocard's problem": Is there a fourth solution to the factorial equation
  *n*! + 1 = *m*²? Erdős thought not.
* Erdős–Mollin–Walsh conjecture: Are there any triples of consecutive
  [powerful numbers](https://en.wikipedia.org/wiki/Powerful_number)? There are
  infinitely many pairs. Conjectured to not exist by Erdős in 1976 and Mollin
  & Walsh in 1986.
* [Erdős–Moser
  conjecture](https://en.wikipedia.org/wiki/Erd%C5%91s%E2%80%93Moser_equation):
  Does a certain equation have any non-trivial solutions? Equivalently, do any
  of the convergents of a certain transcendental constant fulfill a certain
  equation? The latter sounds like it could be done on a machine.
* Firoozbakht's second conjecture: Is there a fourth natural number *k* such
  that *k* exponentiated to the *k*'th power, plus three, is prime? Given by
  Firoozbakht in 2009. Not to be confused with [Firoozbakt's first
  conjecture](https://en.wikipedia.org/wiki/Firoozbakht%27s_conjecture) about
  the distribution of primes, which seems harder to encode on a computer.
* [Friendly number conjecture](https://en.wikipedia.org/wiki/Friendly_number):
  Is ten a solitary number? There are other small open cases, like fourteen or
  fifteen, which could also be studied.
* Generalized taxicab conjecture: Is the [generalized taxicab
  function](https://en.wikipedia.org/wiki/Generalized_taxicab_number)
  well-defined at Taxicab(5,2,2); are there four natural numbers *a*, *b*,
  *c*, and *d* such that *a*⁵ + *b*⁵ = *c*⁵ + *d*⁵? Guy noted it as an open
  problem in 2004, but it is unlikely that Ramanujan was unaware of it.
* Greathouse conjecture: Is there a fourth natural number expressible as four
  sums of distinct powers; of powers of two, three, four, and five
  respectively? Conjectured by Greathouse in 2016 while editing OEIS; this is
  [OEIS A146025](https://oeis.org/A146025).
* [Quasiperfect numbers](https://en.wikipedia.org/wiki/Quasiperfect_number):
  Do they exist? It's not clear who introduced the concept, but there's a rich
  literature going back over a century of folks studying the properties such
  numbers must have.
* [Van Landingham conjecture](https://en.wikipedia.org/wiki/Lychrel_number):
  In base 10, does the map which reverses the digits of a number and adds it
  to the original ("reverse-and-add") always have palindromes among its
  iterates? In particular, does 196 ever lead to a palindrome? This one is not
  amenable or useful to number theory, but is still useful as a gauge due to
  its ease of implementation.
* [Wall-Sun-Sun
  conjecture](https://en.wikipedia.org/wiki/Wall%E2%80%93Sun%E2%80%93Sun_prime):
  Is there at least one Wall-Sun-Sun prime? Wall asked in 1960 as part of an
  examination into Fibonacci sequences (mod *n*), and Sun & Sun asked in 1992
  as part of the quest to prove Fermat's Last Theorem.

## Languages

Suggested by ais523:

* [Tag systems](https://esolangs.org/wiki/Tag_system): programs are triples of
  a positive natural number ("skip"), a set ("alphabet") with a chosen
  element ("halting symbol"), and a map ("production") mapping the alphabet to
  strings of the alphabet ("words"); indices are the skip, the cardinality of
  the alphabet, and the maximum length of any word in the production
* [The Waterfall Model](https://esolangs.org/wiki/The_Waterfall_Model):
  programs are square matrices of natural numbers; indices are matrix size,
  maximum starting waterclock (maximum over first column), maximum trigger
  value (maximum over rest of matrix)

For tag systems, they note that skip is usually 2 ("2-tag"), and that
Turing-completeness begins to manifest around 5 symbols or maximum word length
3, with an explicit UTM in 2-tag, 19 symbols, maximum word length 4. Lore is
that word length 2 is bounded in space, word length 3 is universal due to an
algorithm which compiles down longer words, and that even though 3 is where
universality starts, word length 4 is much easier for humans to work with.
