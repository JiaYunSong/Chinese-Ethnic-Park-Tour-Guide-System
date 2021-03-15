global pBF, k
pBF = True
k = 10


def mDistance(x0, y0, x, y):
    return abs(x0-x) + abs(y0-y)

def oDistance(x0, y0, x, y):
    return (x0-x)**k + (y0-y)**k

def bruteForce(DotList, x0, y0):
    length = len(DotList)
    Q = DotList[0]
    LQ = oDistance(x0, y0, Q[0], Q[1])
    Q = 0
    for num, [x, y] in zip(range(length), DotList[1:]):
        LR = oDistance(x0, y0, x, y)
        if LR < LQ:
            Q = num
            LQ = LR
    return Q


def probabilisticBruteForce(DotList, x0, y0):
    length = len(DotList)
    global pBF
    step = pBF * 2 - 1
    dotNow = 0 if pBF else length
    pBF = not pBF

    Q = DotList[0]
    Max = mDistance(x0, y0, Q[0], Q[1])
    Min = Max >> 1
    Q = 0
    while True:
        dotNow += step
        if dotNow == 0 or dotNow == length:
            break
        x, y = DotList[dotNow]
        L1 = mDistance(x0, y0, x, y)
        L2 = L1 >> 1
        if L2 > Max:
            continue
        elif L1 < Min:
            Min = L2
            Max = L1
            DotList[dotNow], DotList[Q] = DotList[Q], DotList[dotNow]
        else:
            LR = oDistance(x0, y0, x, y)
            LQ = oDistance(x0, y0, DotList[Q][0], DotList[Q][1])
            if LR < LQ:
                Min = L2
                Max = L1
                DotList[dotNow], DotList[Q] = DotList[Q], DotList[dotNow]
    return dotNow


if __name__ == '__main__':
    import random
    import time

    NUM = 10000
    dotList = [[random.randint(-100, 100) for _ in range(2)] for _ in range(NUM)]

    T = [[], []]

    for _ in range(100):
        x = 0
        y = 0
        T[0].append(0)
        T[1].append(0)
        for _ in range(10):
            x += random.randint(-2, 2)
            y += random.randint(-2, 2)

            start = time.time()
            w1 = bruteForce(dotList[:-1], x, y)
            T[0][-1] += time.time()-start

            start = time.time()
            w2 = probabilisticBruteForce(dotList, x, y)
            T[1][-1] += time.time()-start

            if w1 != w2:
                exit(1)

    import matplotlib.pyplot as plt

    plt.figure()
    plt.plot(range(100), T[0], label='bruteForce')
    plt.plot(range(100), T[1], label='probabilisticBruteForce')
    plt.legend()
    plt.xlabel('Test Number')
    plt.ylabel('Time(s)')
    plt.show()
