def oDistance(x0, y0, x, y):
    """
    两点间二维欧式距离计算

    :param x0: 第一点横坐标
    :param y0: 第一点纵坐标
    :param x: 第二点横坐标
    :param y: 第二点纵坐标
    :return: 欧式距离
    """
    return (x0-x)**2 + (y0-y)**2

def bruteForce(DotList, x0, y0):
    """
    蛮力法解决单临近问题，返回点集最临近点

    :param DotList: 需要查找的点集
    :param x0: 参考点横坐标
    :param y0: 参考点纵坐标
    :return: 最临近点编号
    """
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

def mDistance(x0, y0, x, y):
    """
    两点间二维曼哈顿距离计算

    :param x0: 第一点横坐标
    :param y0: 第一点纵坐标
    :param x: 第二点横坐标
    :param y: 第二点纵坐标
    :return: 曼哈顿距离
    """
    return abs(x0-x) + abs(y0-y)

global pBF
pBF = True
def probabilisticBruteForce(DotList, x0, y0):
    """
    基于历史查询概率优化后的加速的某点单临近查询算法解决单临近问题，返回点集最临近点

    :param DotList: 需要查找的点集
    :param x0: 参考点横坐标
    :param y0: 参考点纵坐标
    :return: 最临近点编号
    """
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
            # 随机游走
            x += random.randint(-2, 2)
            y += random.randint(-2, 2)

            start = time.time()
            a = bruteForce(dotList[:-1], x, y)
            T[0][-1] += time.time()-start

            start = time.time()
            b = probabilisticBruteForce(dotList, x, y)
            T[1][-1] += time.time()-start

            # 完整性检验
            if a != b:
                exit(0)

    import matplotlib.pyplot as plt

    plt.figure()
    plt.plot(range(100), T[0], label='bruteForce')
    plt.plot(range(100), T[1], label='probabilisticBruteForce')
    plt.legend()
    plt.xlabel('Test Number')
    plt.ylabel('Time(s)')
    plt.show()
