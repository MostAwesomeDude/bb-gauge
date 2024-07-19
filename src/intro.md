# Introduction

This living book compares the sizes of programs in several Turing-complete
categories in order to gauge the relative expressive power and difficulty of
longstanding open problems in mathematics. Our approach will follow the
following pattern:

* Many functions describing properties of computer programs are uncomputable
  ([WP](https://en.wikipedia.org/wiki/Computable_function),
  [nLab](https://ncatlab.org/nlab/show/computability)) because they give
  oracles for [Halting](https://en.wikipedia.org/wiki/Halting_problem)
* Choose a computer, a property of its programs, and a formal system;
  enumerate the system's theorems with a program for the computer, halting if
  and only if a contradiction is found
* If this system has a theorem determining every value of the property for
  every program, then this theorem determines whether the enumerating program
  will halt and the enumerating program will eventually find it, allowing the
  system to decide its own consistency in violation of [Gödel's second
  incompleteness](https://en.wikipedia.org/wiki/G%C3%B6del%27s_incompleteness_theorems);
  so, any formal system can only prove at most finitely many instances of any
  property of programs

If we're careful about the details implied by each of these steps, then we can
gauge the complexity of any open problem in mathematics:

* Choose a computer and a formal system for expressing the problem
* Encode a search for counterexamples/proofs to the problem as a proof search
  over the formal system
* Choose an uncomputable property of programs
* Without loss of generality, we may index the uncomputable portion of the
  property by some computable property known during enumeration; it is still
  uncomputable
* Assign comparison operators to the index

For a fully-worked example of the entire recipe, consider:

* The function BB giving the maximum number of steps taken by halting Turing
  machines is uncomputable, as it could be used to decide Halting by providing
  a cutoff
* Without loss of generality, we may index BB by states and symbols
* BB is valued in natural numbers, and by a counting argument, BB is monotone
  with regard to both states and symbols
* In natural number theory, we may search for k such that k > 8 and 2
  exponentiated to the k'th power has at least one '2' in its trinary
  representation (alternatively, such that k > 8 and 2 exponentiated to the
  k'th power cannot be written as a sum of distinct powers of 3)
* We do not yet know whether this statement is true, so we do not yet know
  whether this search will halt
* We may encode the search directly as a 15-state 2-symbol Turing machine or a
  5-state 4-symbol Turing machine, done by [Stérin & Woods
  2021](https://arxiv.org/abs/2107.12475)

Therefore, we may say that this particular number-theoretic question, known as
one of Erdős' conjectures, is gauged to be at most as hard as BB(15,2) or
BB(5,4). While this is far beyond our ability to compute with brute force, we
may nonetheless compare it to other conjectures, such as Goldbach's
conjecture, which has been gauged to be at most as hard as BB(43,2).

More generally, if our properties are not neatly indexed by natural numbers or
do not obey nice shrinking behaviors, we may still consider programs under
some reduction and then require properties to be invariant or monotone as
reduction proceeds, as well as converging to some limit after a finite number
of reductions. The classic example is gauging the size of expressions in
lambda calculus; we could work with [OEIS A114851, the number of terms of
given size](https://oeis.org/A114851), but we may find it easier to work with
the reduced gauge [OEIS A195691, the number of closed terms in normal
form](https://oeis.org/A195691).
