# Experimenting with ideas from http://cheddarmonk.org/papers/laver.pdf

N = 8
stack = []

def check(i=[1, 1]):
    i[0] += 1
    if len(stack) >= i[1]:
        i[1] = len(stack)
        print("depth", len(stack), "at step", i[0])

while True:
    N <<= 1
    print("N", N)
    stack.append(16)
    stack.append(1)
    while True:
        check()
        x = stack.pop()
        stack.append((x + 1) % N)
        if len(stack) == 1: break
        x = stack.pop()
        y = stack.pop()
        for _ in range(y): stack.append(x)
    x = stack.pop()
    assert x == 1
