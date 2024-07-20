; Tape consists of three parts - prime, work value and function value
; Pólya conjecture states that so called summatory Liouville function is everywhere positive
; This is equivalent to 'function value is always non-zero' in my machine
; Number of 1's in function space is equal to -L(n)+1

; These are setup states. They are here to make tape ready to work
0 _ 1 l 1
1 _ _ l 2
2 _ 1 l 3
3 _ 1 l 4
4 _ 1 l 5
5 _ _ l 6
6 _ 1 l 7
7 _ 1 r x0
; This is 'get to work' state. It simply moves from leftmost symbol to work space
x0 1 1 r x0
x0 x _ r x0
x0 _ _ l w1
; These are working states. They check if work value is divisible by prime
; w states mark p symbols in work value (where p is value of prime)
w1 1 x r w2
w1 x x l w1
w3 1 x l w0
w2 _ _ r w3
w3 _ _ l s0 ; If p doesn't divide work value, it skips to s
w0 _ _ l w1
w0 * * l w0
w2 * * r w2
w3 * * r w3
w1 _ _ r c0
; If we finished marking p, we check if it's end of work value 
c0 _ _ r c1
c0 * * r c0
c0 x 1 r c0
c1 _ p l d0 ; if it does, skip to d
c1 p _ l d0
c1 1 1 l c2
c2 x y l w0 ; If it isn't, return to w
c1 * * r c1
; Division - we divide work value by p and we leave 'p' on tape, marking prime factor
d0 x y l d1
d0 y y l d1
d1 x y r d2
d1 y y l d1
d2 p p l d3
d2 _ _ l d3
d2 * * r d2
d3 y _ l d0
d1 _ _ r d4
d4 y 1 r d4
d4 _ _ l d5
d5 1 1 l d6
d6 1 1 l w0
d6 _ _ r a0
; This simply increments prime
s0 x 1 l s0
s0 y 1 l s0
s0 _ _ l s1
s1 x 1 l s1
s1 1 1 l s1
s1 _ 1 r x0
; Crucial part - depending on number of prime factors we increment or decrement function value
; It also sets work value to next number
a0 * * r a1
a1 _ 1 r a1
a1 p 1 r a2
a2 _ 1 r a2
a2 p 1 r a1
a1 1 _ r a3
a3 _ _ r halt-False ; If function value reaches 0, Pólya conjecture is false, and machine halts
a3 1 1 l r0
a2 1 _ r a4
a4 1 1 r a4
a4 _ 1 r a5
a5 _ 1 l r0
; Return - after changing function value it starts dividing new number
r0 1 1 l r0
r0 _ _ l r1
r1 1 1 l r1
r1 _ _ l r2
r2 1 1 l r3
r3 1 1 l r4
r4 1 x l r4
r4 _ _ r x0
