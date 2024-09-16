# Introduction

## Idea

How hard are questions about mathematics? Some have remained open for
millennia, some are considered too hard for all known techniques, and some
have only been answered with the help of computers. Nonetheless, some
questions are harder than others; in particular, sometimes progress on one
question can contribute answers to other questions.

How do computers help with mathematical questions? Mathematics can be
**formalized**: reduced to manipulation of abstract symbols, like letters on a
page or beads on an abacus. Answers to questions can be formalized as proofs,
which are sequences of manipulations that follow some predetermined rules. A
computer can be programmed to perform a search for a proof. (Indeed, in a
certain sense, [all programs are searches for
proofs](https://ncatlab.org/nlab/show/proofs+as+programs).) However, if there
is no proof, then the program will run forever, and [whether a program will
halt](https://en.wikipedia.org/wiki/Halting_problem) is itself uncomputable
([WP](https://en.wikipedia.org/wiki/Computable_function),
[nLab](https://ncatlab.org/nlab/show/computability)).

What use is a program that might run forever? On its own, not much. However,
this living book presents a collection of several different programs, collated
by formalism and mathematical question, which all search for proofs in one way
or another. We may then roughly *gauge* the difficulty of questions by
comparing the sizes of different programs which each search for proofs
answering the same question.

As a quick aside: the search for bounds on halting programs is known as the
[busy beaver game](https://en.wikipedia.org/wiki/Busy_beaver), and so this
book is naturally known as the **Busy Beaver Gauge**.

## Nuts & Bolts

To make this whole concept useful, we choose machines and languages which are
Turing-complete and seem relatively simple to describe (in the sense of
[Kolmogorov complexity](https://en.wikipedia.org/wiki/Kolmogorov_complexity))
but are otherwise not particularly good for expressing any facet of
mathematics, in order to be unbiased. We also must find reasonable ways of
measuring the size of programs such that smaller programs are simpler than
larger programs.

We also need a good list of unsolved problems in mathematics. These problems
need to be questions; specifically, we need to be able to search for a
definite answer to the question using only one infinite loop or infinite
recursion.

Finally, we wish to thank the many folks who authored the programs that we
study here. Credits are given per-program in the following pages, in tables of
values at the bottom of each page. Where possible, we also link to English
Wikipedia (WP), the esoteric languages wiki (esolangs), and the *n*Lab.
