; Initial input: 11

; We check if current number is prime
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
14 _ _ r 19
15 * * l 15
15 _ _ l 16
16 * * l 16
16 _ _ r 17
17 * _ r 18
17 _ _ r halt-True
18 * * r 18
18 _ _ r 13
; If it is, we check 2^n-1
19 1 _ l 24
19 _ _ l 25
20 1 1 l 20
20 _ 1 r 21
21 1 1 r 21
21 _ 1 r 22
22 1 _ l 20
22 _ 1 r 23
23 1 _ l 24
23 _ _ l 25
24 1 1 l 24
24 _ _ r 22
25 1 1 l 25
25 _ _ r 0
