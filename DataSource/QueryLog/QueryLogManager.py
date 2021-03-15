# -*- coding: UTF-8 -*-
# editor: JiaYunSong

from typing import List
import yaml


class QueryLogManager:
    """
    Features
    -----------------------------------------
    日志管理类，用于记录添加和推荐查询，可自动重构、存储日志，利用list、dict可变数据类型特性进行构建操作

    Members
    ----------------------------------------
    __queryLogPath : <str> 日志文件目录
    __LogNum : <dict> 日志记录数量字典，用于控制日志更新周期，结构：{出发地编号: 总查询请求次数, ...}
    __QueryLog : <dict> 日志记录字典，结构：{出发地编号: [[目的地编号, 查询请求次数], ...], ...}
    __OldLog : <dict> 上一更新周期的日志记录字典，结构：{出发地编号: [[目的地编号, 查询请求次数], ...], ...}
    __MaxHeap : <dict> 大根堆，用于查询热点景点，结构：{出发地编号: [QueryLog[出发地编号]的大根堆], ...}

    Functions
    ----------------------------------------
    __init__(filepath: str, placeNum: int = 23) : 新建类并加载历史记录
    addQueryLog(nowPlace: int, vertexSet: list) : 添加查询记录
    clearAll() : 删除所有查询记录
    SearchRecommendAttraction(self, curvertex: int) -> List[List[int]] : 利用历史数据更新查询当前顶点的推荐景点

    """

    def __init__(self, filepath: str, placeNum: int = 23):
        """
        新建类并加载历史记录

        :param filepath: <str> 日志路径
        :param placeNum: <int> 地点数量，预设23个景点
        """
        self.__placeNum = placeNum
        self.__queryLogPath = filepath
        self.__LogNum = dict()
        self.__QueryLog = dict()
        self.__OldLog = dict()
        self.__MaxHeap = dict()

        try:
            self.__readQueryLog()
        except Exception as e:
            print(f"QueryLog {e}, {self.__queryLogPath} rebuild is doing...")
            self.clearAll()

        # TODO: 需要保存日志时取消注释
        # # 提前加载日志文件，防止 open 函数在 __del__() 操作异常
        # self.__file = open(self.__queryLogPath, 'w')

    def __readQueryLog(self):
        """加载历史日志文件"""
        with open(self.__queryLogPath, 'r') as f:
            self.__LogNum, self.__QueryLog, self.__OldLog, self.__MaxHeap = yaml.load(f.read(), Loader=yaml.FullLoader)
        assert len(self.__LogNum) == self.__placeNum

    def addQueryLog(self, nowPlace: int, vertexSet: List[int]) -> None:
        """
        添加查询记录，更新大根堆，并进行日志大小控制

        :param nowPlace: <int> 现在所处位置编号
        :param vertexSet: <list> 查询列表
        """
        self.__LogNum[nowPlace] += 1

        # 利用节点查询次数控制日志大小
        if self.__LogNum[nowPlace] > 10000:
            # 更新节点查询频率
            for i in vertexSet:     # 不能直接迭代加一，python默认重新建立list，破坏指针结构
                z = self.__QueryLog[nowPlace][i][1] + 1
                self.__QueryLog[nowPlace][i][1] = z

            # 减去上一周期查询频率
            self.__QueryLog[nowPlace] = [[i[0], i[1] - j[1]] for i, j in zip(self.__QueryLog[nowPlace], self.__OldLog[nowPlace])]

            # 完整重建该节点大根堆结构
            self.__MaxHeap[nowPlace] = [*self.__QueryLog[nowPlace]]
            self.__RebuildHeapOverall(nowPlace)

            # 更新查询次数
            self.__LogNum[nowPlace] = 5000
        else:
            # 更新节点查询频率并部分调整大根堆结构
            for i in vertexSet:  # 不能直接迭代加一，python默认重新建立list，破坏指针结构
                z = self.__QueryLog[nowPlace][i][1] + 1
                self.__QueryLog[nowPlace][i][1] = z
                self.__RebuildHeapPart(nowPlace, i)

        if self.__LogNum[nowPlace] == 5000:
            self.__OldLog[nowPlace] = [[*i] for i in self.__QueryLog[nowPlace]]

    def __RebuildHeapPart(self, nowPlace: int, fixPlace: int):
        """
        大根堆部分更新，即将某一节点按大根堆更新规则移动

        :param nowPlace: <int> 需要调整的地点编号
        :param fixPlace: <int> 需要调整的大根堆节点
        """
        # 寻找已经调整的节点位置
        num = 0
        for inum, imes in enumerate(self.__MaxHeap[nowPlace]):
            if imes[0] == fixPlace:
                num = inum
                break

        # 不断与父节点比较，若大，则交换，否则结束调整
        while num > 0:
            if self.__MaxHeap[nowPlace][num][1] >= self.__MaxHeap[nowPlace][num//2][1]:
                self.__MaxHeap[nowPlace][num], self.__MaxHeap[nowPlace][num//2] = \
                    self.__MaxHeap[nowPlace][num//2], self.__MaxHeap[nowPlace][num]
                num = num // 2
            else:
                break

    def __RebuildHeapOverall(self, nowPlace: int):
        """
        整体重建大根堆

        :param nowPlace: <int> 需要调整的地点编号
        """
        r = self.__MaxHeap[nowPlace]
        n = self.__placeNum

        # 初始建堆，最后一个分支的下标是(n-1)/2
        for k in range((n-1)//2, -1, -1):
            # i 为需要调整的结点，j 为 i 的左孩子
            i, j = k, 2 * k + 1

            # 一直筛选到叶子
            while j < n:
                if j < n-1 and r[j][1] < r[j+1][1]:
                    j += 1  # 取孩子中较大者
                if r[i][1] > r[j][1]:
                    break   # 根节点值已经大于孩子
                else:       # 结点与较大孩子互换
                    r[i], r[j] = r[j], r[i]
                    i, j = j, 2 * j + 1

    def SearchRecommendAttraction(self, curvertex: int) -> List[List[int]]:
        """
        利用历史数据更新查询当前顶点的推荐景点

        :param curvertex: <int> 当前所在地景点编号
        :return: <list> 三元组，游客位于当前景点受大数据推荐的三个景点编号及其近期热度
        """
        # 大根堆结构中取排序前三的节点
        # 若两子节点值相同，则排序前三的节点为前三个节点，并输出
        if self.__MaxHeap[curvertex][1][1] == self.__MaxHeap[curvertex][2][1]:
            return [[*self.__MaxHeap[curvertex][i]] for i in range(3)]
        # 若不相等，则排序前三的节点为前7个节点中最大的三个，并排序输出
        return sorted([[*self.__MaxHeap[curvertex][i]] for i in range(7)], key=lambda x: x[1], reverse=True)[: 3]

    def clearAll(self):
        """重置所有查询记录"""
        self.__LogNum = {i: 0 for i in range(self.__placeNum)}
        self.__QueryLog = {i: [[j, 0] for j in range(self.__placeNum)] for i in range(self.__placeNum)}
        self.__OldLog = {i: [[j, 0] for j in range(self.__placeNum)] for i in range(self.__placeNum)}
        self.__MaxHeap = {i: [*self.__QueryLog[i]] for i in range(self.__placeNum)}

    def __del__(self):
        """退出时保存日志文件"""

        # TODO: 需要保存日志时取消注释
        # yaml.dump([self.__LogNum, self.__QueryLog, self.__OldLog, self.__MaxHeap], self.__file)
        # self.__file.close()


if __name__ == '__main__':
    # 通过日志路径加载历史日志
    qLogM = QueryLogManager('queryLog.history')

    # 添加查询日志
    for i in range(2):
        qLogM.addQueryLog(0, [1, 6, 7])
        qLogM.addQueryLog(1, [3, 5, 9])
        qLogM.addQueryLog(2, [6, 14, 21])

    # 查询 0 地点前三 pick 量的节点
    print(qLogM.SearchRecommendAttraction(0))

    # 清除所有日志记录
    qLogM.clearAll()
