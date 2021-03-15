# -*- coding: UTF-8 -*-
# editor: Su HanYu,JiaYunSong

import os
import sys
import pandas as pd
from typing import List
from DataSource.Graph import GraphManager


class AttractionInfo(object):
    """
    Features
    -----------------------------------------
    景点信息类

    Member
    -----------------------------------------
    num : <int> 编号
    name : <str> 景点名称
    x : <int> x
    y : <int> y
    miniIntro: <str> 简介
    intro : <str> 介绍
    active : <list> 活动

    """

    def __init__(self, num: int, name, x, y, miniIntro, intro, active):
        """
        建立类

        :param num: 编号
        :param name: 景点名称
        :param x: x
        :param y: y
        :param miniIntro: 简介
        :param intro: 介绍
        :param active: 活动
        """
        self.num = int(num)
        self.name = str(name)
        self.x = int(x)
        self.y = int(y)
        self.miniIntro = str(miniIntro)
        self.intro = str(intro)
        self.active = str(active)


class AttractionSet(object):
    def __init__(self, path: str, graph):
        self.attractions = {}
        self.__addAttractionsFromFile(path)
        self.__graph = graph

        # TODO: 需要输出保存的话请将注释去除
    #     self.__outputFile = open(path.replace('Sightseeing.csv', 'test.csv'), 'w', newline='', encoding='gbk')
    #
    # def __storeAttractionsToFile(self):
    #     """将景点信息重写进文件"""
    #     csvWrite = csv.writer(self.__outputFile, dialect='excel')
    #     for key, attr in self.__attractions.items():
    #         # if type(key) is int:
    #         csvWrite.writerow([attr.num, attr.name, attr.x, attr.y, attr.miniIntro, attr.intro, attr.active])

    @staticmethod
    def SearchAttractionsImage(num) -> str:
        """获取景区图片路径"""
        currentPath = os.path.abspath(__file__)
        father_path = os.path.abspath(os.path.dirname(currentPath) + os.path.sep + ".")
        return father_path.replace('\\', '/') + f'/images/{num}.jpg'

    @staticmethod
    def SearchAttractionsImgFile(name) -> str:
        """获取景区图片路径"""
        currentPath = os.path.abspath(__file__)
        father_path = os.path.abspath(os.path.dirname(currentPath) + os.path.sep + ".")
        return father_path.replace('\\', '/') + f'/images/{name}'

    def __addAttractionsFromFile(self, path: str):
        """加载文件数据"""
        df = pd.read_csv(path, encoding='gbk')
        infos = df.values
        for i in range(infos.shape[0]):
            id = infos[i][0]
            # name = infos[i][1]
            attraction = AttractionInfo(infos[i][0], infos[i][1], infos[i][2], infos[i][3], infos[i][4], infos[i][5],
                                        infos[i][6])
            self.attractions[id] = attraction
            # self.__attractions[name] = attraction

    @staticmethod
    def minDistance(str1: str, str2: str) -> int:
        """
        计算两个字符串之间最小距离

        :param str1: <str> 待比较字符串1
        :param str2: <str> 待比较字符串2
        :return: <int> 最小编辑距离
        """
        # 存放字符串1的长度
        m = len(str1)
        # 存放字符串2的长度
        n = len(str2)
        # 动态规划计算表格，记录当前位置最小差别数
        dp = [[-1] * (n + 1) for i in range(m + 1)]

        # 初始化第0行和第0列
        for i in range(m + 1):
            dp[i][0] = i
        for j in range(n + 1):
            dp[0][j] = j

        # 逐行填写动态规划过程表格
        for i in range(1, m + 1):
            for j in range(1, n + 1):
                # 根据状态转移方程列出两种情况的计算式
                if str1[i - 1] == str2[j - 1]:
                    dp[i][j] = min(dp[i - 1][j - 1], dp[i][j - 1] + 1, dp[i - 1][j] + 1)
                else:
                    dp[i][j] = min(dp[i - 1][j - 1] + 1, dp[i][j - 1] + 1, dp[i - 1][j] + 1)

        return dp[m][n]

    @staticmethod
    def get_F(s):
        F = [-1]
        for i, v in enumerate(s):
            k = F[i]
            while k != -1 and s[k] != s[i]:
                k = F[k]
            F.append(k + 1)
        return F

    @staticmethod
    def kmp(s1, s2):
        F = AttractionSet.get_F(s2)
        i, j = 0, 0
        while i < len(s1):
            if s1[i] == s2[j]:
                i += 1
                j += 1
            else:
                j = F[j]
            if j == len(s2):
                return True
            if j == -1:
                i += 1
                j += 1
        return False

    def searchAttractionsInfoByName(self, name: str) -> List[AttractionInfo]:
        """
        根据景点名称查询景点信息(可使用编辑距离等算法以支持模糊查询)

        :param name: <str> 景点名称
        :return: <List[AttractionsInfo]> 相应的景点信息
        """
        r = []
        for i in self.attractions.values():
            # 计算编辑距离
            dis = self.minDistance(name, i.name)
            # 设置编辑距离与字符串长度的比值小于0.4为可容忍的错误范围，同时利用正则表达式实现部分匹配
            if dis / len(name) < 0.4 or self.kmp(i.name, name):
                r.append(i)

        return r

    def searchAttractionsInfo(self, id: int) -> AttractionInfo:
        """
        根据景点编号查询景点信息

        :param id: <int> 景点编号
        :return: <AttractionsInfo> 相应的景点信息
        """
        return self.attractions[id]

    def updateAttractionsInfoFromList(self, id: int, mesList: list, operateType: int = 0) -> str:
        return self.updateAttractionsInfo(id, AttractionInfo(*mesList), operateType)

    def updateAttractionsInfo(self, id: int, attrInfo: AttractionInfo = None, operateType: int = 0) -> str:
        """
        景点信息的更新、添加、删除，默认做删除操作

        :param id: <int> 景点编号
        :param attrInfo: <AttractionsInfo> 待更新的景点信息，默认为空
        :param operateType: <int> 0 - 删除操作; 1 - 添加操作; 2 - 修改操作，默认做删除操作
        :return: <str> 提示信息
        """
        Message = "成功！"

        # 操作类型为删除
        if operateType == 0:
            if id not in self.attractions.keys():
                # print("id not exists!", file=sys.stderr)  # 要改成前端提示
                Message = "id not exists!"
            self.attractions.pop(id)
            self.__graph.addOrDelVertex(id, False)

        # 操作类型为添加
        elif operateType == 1:
            if id in self.attractions.keys():
                print("id exists!", file=sys.stderr)  # 要改成前端提示
                Message = "id exists!"
            self.attractions[id] = attrInfo
            self.__graph.addOrDelVertex(id)

        # 操作类型为修改
        elif operateType == 2:
            if id not in self.attractions.keys():
                # print("id not exists!", file=sys.stderr)  # 要改成前端提示
                Message = "id not exists!"
            self.attractions[id] = attrInfo

        return Message

    def __del__(self):
        pass
        # TODO: 需要输出保存的话请将注释去除
    #     # self.__storeAttractionsToFile()
    #     # self.__outputFile.close()


if __name__ == '__main__':
    import DataSource.Graph.GraphManager

    graph = GraphManager.GraphEdges('../Graph/Graph.csv', None)

    attractionSet = AttractionSet('Sightseeing.csv', graph)
    # 测试通过id查找景点信息
    r: AttractionInfo = attractionSet.searchAttractionsInfo(2)
    print(r.num, r.name)

    # 测试通过景点名称查找景点信息
    rl: list = attractionSet.searchAttractionsInfoByName('白')
    for i in rl:
        print(i.name, i.num)

    # 更改景点信息
    attractionSet.updateAttractionsInfo(25, AttractionInfo(25, '白族', 100, 100, 'x', 'x', 'x'), 1)

    attractionSet.updateAttractionsInfoFromList(25, [25, '白族', 100, 100, 'x', 'x', 'x'], 2)

    # 所有景点信息
    # print(list(attractionSet.attractions.values()))

    # line = "222222222"
    # pattern = "1"
    # m = re.search(pattern, line)
    # print(m)




