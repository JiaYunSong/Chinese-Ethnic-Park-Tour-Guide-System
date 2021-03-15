# -*- coding: UTF-8 -*-
# editor: Li YiMing

import numpy as np


def optimize(ticketPrice,flowVolume,guidancePrice,maxGuidanceNum,tolerance,serviceTime,touristsNum = 5):
    """
    选择当前景点最优的导游数目

    :param ticketPrice: <int> 当前景点的票价
    :param flowVolume: <int> 一小时的客流量
    :param guidancePrice: <int> 单次雇佣一名导游一小时的费用
    :param maxGuidanceNum: <int> 当前景点可雇佣导游的最大数目
    :param tolerance: <int> 排队的最大游客数目
    :param serviceTime: <int> 一组游客预计的参观时间
    :param touristsNum: <int> 一个导游单次可以带多少名游客
    :return <tuple> 第一个元素为最优安排对应的最大利润,第二个元素为最优安排对应的导游数目
    """

    # 列表,记录每一种导游选择方案的利润
    profit = []
    serviceVolume = 60 / serviceTime

    # 枚举可以选择的导游数目
    for i in range(1,maxGuidanceNum + 1):

        # 排队的最大游客组数(人数/每组人数)
        group = tolerance // touristsNum

        # 一小时一位导游可以服务的游客数
        mu = touristsNum*serviceVolume


        # A为递推矩阵,b为方程组右端系数
        A = np.zeros((group,group))
        b = np.zeros(group)
        b[-1] = 1

        # 根据递推公式给每个矩阵元素赋值
        A[0,0],A[0,1] = flowVolume,-mu

        for j in range(1,group-1):
            if j <= (i-1):
                A[j,j - 1],A[j,j],A[j,j + 1] = flowVolume,-(flowVolume + mu*j), mu*(j + 1)
            else:
                A[j,j - 1],A[j,j],A[j,j + 1] = flowVolume,-(flowVolume + mu*i), mu*i

        # 所有概率相加等于1
        for j in range(0,group):
            A[-1,j] = 1
        
        # print(A)
        p = np.linalg.solve(A,b)

        # p[-1]为当前队伍满园的概率,相应地,(1-p[-1])为不损失游客的概率
        realFlowVolume = flowVolume * (1 - p[-1])

        # 计算当前利润
        profit.append(realFlowVolume*ticketPrice - i*guidancePrice)

    # print(profit)

    # 最大利润及其对应的导游数量
    return max(profit),profit.index(max(profit))+1


if __name__ == "__main__":

    # 三个示例
    '''
    小型景点 
    门票价格10元,一小时客流量100人,一小时给导游的工资50元,最多可雇佣10个导游,
    队伍最大排队容量60人,一个导游一小时可以带5组讲解,一个导游一次讲解可以带5名游客。
    '''
    print(optimize(10,100,50,10,60,12))

    '''
    中型景点 
    门票价格15元,一小时客流量150人,一小时给导游的工资50元,最多可雇佣15个导游,
    队伍最大排队容量100人,一个导游一小时可以带4组讲解,一个导游一次讲解可以带5名游客。
    '''
    print(optimize(15,150,50,15,100,15))

    '''
    大型景点 
    门票价格20元,一小时客流量250人,一小时给导游的工资50元,最多可雇佣25个导游,
    队伍最大排队容量180人,一个导游一小时可以带3组讲解,一个导游一次讲解可以带5名游客。
    '''
    print(optimize(20,250,50,25,180,20))
