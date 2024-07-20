; NB: Initial tape is "111_11111". ~ C.

; We check if current numer is prime
0 1 1 l 1
0 _ _ r 0
1 _ _ l 2
2 _ 1 l 3
3 _ 1 r 4
4 x x l 4
4 1 x r 5
4 _ _ r 8
5 x x r 5
5 _ _ r 6
6 x x r 6
6 1 x l 7
6 _ _ l 11
7 x x l 7
7 _ _ l 4
8 * 1 r 8
8 _ _ r 9
9 x x r 9
9 1 1 l 10
9 _ _ l 14
10 x x l 10
10 _ _ l 4
11 x 1 l 11
11 _ _ l 12
12 * * l 12
12 _ 1 r 8
13 * * r 13
13 1 1 l 14
14 * 1 l 15
14 _ _ r 24
15 * * l 15
15 _ _ l 16
16 * * l 16
16 _ _ r 17
17 * _ r 18
17 _ _ r 19
18 * * r 18
18 _ _ r 13
; No matter what is result, we replace n with 2n-1
; This makes sure we check only numbers of form 2^m+1
19 * _ l 20
19 _ _ l 22
20 * 1 l 20
20 _ 1 r 21
21 * 1 r 21
21 _ 1 r 19
22 1 1 l 22
22 _ _ r 23
23 1 _ r 0
; If number was prime, we decrement counter
24 1 1 r 24
24 _ _ r 25
25 _ _ l halt-Accept ; If counter was 0, we found new Fermat prime (yay!)
25 1 1 r 26
26 1 1 r 26
26 _ _ l 27
27 1 _ l 28
28 1 1 l 28
28 _ _ l 29
29 1 1 l 29
29 _ _ r 19
