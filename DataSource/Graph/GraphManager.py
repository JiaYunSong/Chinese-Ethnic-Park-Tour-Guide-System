# -*- coding: UTF-8 -*-
# editor: Li YiMing,Su HanYu,JiaYunSong,Li ZhongHao

import pandas as pd
import numpy as np
import random
from heapq import *
from typing import List, Tuple, Dict


class GraphEdges(object):
    """
    Features
    -----------------------------------------
    稀疏图类

    Members
    ----------------------------------------
    __size: <int> 图的顶点个数
    __cnt: <int> 图的边的个数
    __edges: <list> 存储边的信息，每一个元素是一个四元组(起点，终点，边长，下一条边的索引)
    __head: <list> 每个顶点的初始边(类似于邻接表的头节点)
    __ver2idx: <dict> 两端点到其所对应边的映射

    Functions
    ----------------------------------------
    __init__(size, path, logFunc) : 新建类并加载历史记录
    __updateRealDis() : 利用floyd算法建立实际距离图
    queryEdgeByTwoVertexes(i, j) : 根据路径两端点的景点编号 i,j 查询路径信息
    queryWeightByTwoVertexes(i, j) : 根据路径两端点的景点编号 i,j 查询路径初始权重
    queryDisByTwoVertexes(i, j) : 根据路径两端点的景点编号 i,j 查询两点间实际距离
    queryEdgesByVertex(idx) : 根据景点编号 idx 查询与该景点邻接的边的信息
    addOrDelVertex(idx: int, isAdd: bool = True) : 根据景点编号删除相关景点
    updatePathInfo(vertexPair, newWeight) : 路径信息的更新，默认做删除操作
    searchHamilton(startVertex, vertexSet,endVertex, isCircut) : 根据顶点集的大小不同，选择不同算法求解最短哈密顿回路
    searchPathByDijkstra(startVertex, endVertex) : 根据起点startVertex与终点endVertex搜索最短路径
    getAllPaths(startVertex, endVertex, path) : 求两点之间适宜距离内的所有路径
    searchKShortestPath(startVertex, endVertex, k) : 求两点之间的k短路
    SearchWithinDistance(self, curvertex: int, distance: int) : 求在当前景点一定距离内的景点(广度优先搜索算法，及时剪枝)
    """

    def __init__(self, path: str, logFunc):
        """
        使用链式前向星存储稀疏图，利用csv文件生成无向图，用链式前向星存储图

        :param path: <str> 图数据文件路径
        :param logFunc: <def> addQueryLog(nowPlace: int, vertexSet: List[int]) 添加查询记录函数
        """
        self.logFunc = logFunc
        
        df = pd.read_csv(path)
        df.drop(df.columns[0], axis=1, inplace=True)

        self.__size = len(df.keys())
        # 边的个数初始时为0
        self.__cnt = 0
        # 存储边的信息，每一个元素是一个四元组(起点，终点，边长，下一条边的索引)
        self.edges = [-1]
        # 每个顶点的初始边(类似于邻接表的头节点)
        self.__head = [0 for i in range(2 * self.__size)]
        # 哈希表，键是边的两端点，值是边的长度
        self.__ver2idx = {}
        # 完整距离图
        self.__realDis = np.zeros((self.__size, self.__size))

        weight = df.values

        for i in range(self.__size):
            for j in range(i + 1):
                w = eval(weight[i][j]) if weight[i][j] != '无穷' else np.inf

                self.edges.append([i, j, w, self.__head[i]])
                self.__cnt += 1
                self.__head[i] = self.__cnt

                self.edges.append([j, i, w, self.__head[j]])
                self.__cnt += 1
                self.__head[j] = self.__cnt

                self.__ver2idx[(i, j)], self.__ver2idx[(j, i)] = self.__cnt - 1, self.__cnt

        self.__updateRealDis()

    def __updateRealDis(self):
        """建立完整距离图"""
        for i in range(self.__size):
            for j in range(self.__size):
                w = self.queryEdgeByTwoVertexes(i, j)[2]
                self.__realDis[i, j], self.__realDis[j, i] = w, w

        # 利用Floyd算法求最短路径并更新距离图
        for k in range(self.__size):
            for i in range(self.__size):
                for j in range(self.__size):
                    if self.__realDis[i, j] > self.__realDis[i, k] + self.__realDis[k, j]:
                        self.__realDis[i, j] = self.__realDis[i, k] + self.__realDis[k, j]

    def queryEdgeByTwoVertexes(self, i, j):
        """
        根据路径两端点的景点编号 i,j 查询路径信息

        :param i: <int> 景点编号之一
        :param j: <int> 景点编号之二
        :return: <tuple> 待查询的路径信息
        """
        return self.edges[self.__ver2idx[(i, j)]]

    def queryWeightByTwoVertexes(self, i, j):
        """
        根据路径两端点的景点编号 i,j 查询路径初始权重

        :param i: <int> 景点编号之一
        :param j: <int> 景点编号之二
        :return: <int> 待查询的路径长度
        """
        return self.edges[self.__ver2idx[(i, j)]][-2]

    def queryDisByTwoVertexes(self, i: int, j: int):
        """
        根据路径两端点的景点编号 i,j 查询两点间实际距离

        :param i: <int> 景点编号之一
        :param j: <int> 景点编号之二
        :return: <int> 待查询两点间的实际距离
        """
        return int(self.__realDis[i, j])

    def queryEdgesByVertex(self, idx):
        """
        根据景点编号 tmp 查询与该景点邻接的边的信息

        :param idx: <int> 景点编号
        :return ans: <list> 储存邻接边信息的列表，每一个元素是一个三元组(起点，终点，边长)
        """
        i = self.__head[idx]
        ans = []
        while i != 0:
            ans.append(self.edges[i][:-1])
            i = self.edges[i][-1]
        return ans

    def addOrDelVertex(self, idx: int, isAdd: bool = True):
        """
        根据景点编号删除相关景点

        :param idx: <int> 待修改景点编号
        :param isAdd: <bool> 为True时代表增加一个景点，否则，代表删除一个景点
        """
        if isAdd:
            # 链式前向星加边，边权默认为inf
            for vertex in range(self.__size):
                self.edges.append([vertex, idx, np.inf, self.__head[vertex]])
                self.__cnt += 1
                self.__head[vertex] = self.__cnt

                self.edges.append([idx, vertex, np.inf, self.__head[idx]])
                self.__cnt += 1
                self.__head[idx] = self.__cnt

                self.__ver2idx[(vertex, idx)], self.__ver2idx[(idx, vertex)] = self.__cnt - 1, self.__cnt

        else:
            # 清空以idx为顶点的所有边，只需让其顶点的头指针指向一个不存在的位置(0)即可
            self.__head[idx] = 0
            # 遍历所有要修改的边，修改其权重为inf，并从前向星中删除该星节点
            for vertex in range(self.__size):
                deletingEdgeOne = self.queryEdgeByTwoVertexes(vertex, idx)
                deletingEdgeTwo = self.queryEdgeByTwoVertexes(idx, vertex)
                for num in range(1, self.__cnt + 1):
                    if self.edges[self.edges[num][-1]] == deletingEdgeOne:
                        self.edges[self.edges[num][-1]][-2] = np.inf
                        # 类似于链表删除，修改下一条边的索引
                        self.edges[num][-1] = deletingEdgeOne[-1]

                    # 防止被删除的边仍然留在哈希表中
                    elif self.edges[self.edges[num][-1]] == deletingEdgeTwo:
                        self.edges[self.edges[num][-1]][-2] = np.inf

    def updatePathInfo(self, vertexPair: list, newWeight: int = np.inf):
        """
        路径信息的更新，默认做删除操作

        :param vertexPair: <list> 景点编号对，即要修改路径的两端点
        :param newWeight: <int> 更新后的路径长度，默认为inf，代表删除该路径
        """
        e = self.__ver2idx[(vertexPair[0], vertexPair[1])]
        # 错误提示
        if vertexPair[0] >= self.__size or vertexPair[1] >= self.__size:
            return "edge not exists!"
        self.edges[e][-2] = newWeight
        return "成功！"

    def searchHamilton(self, startVertex: int, vertexSet: list,endVertex: int = None,isCircuit: bool = True) -> (int, list):
        """
        根据顶点集的大小不同，选择状态压缩动态规划或优化邻域选择的禁忌搜索算法求解最短哈密顿回路

        :param startVertex: <int> 出发景点编号
        :param vertexSet: <list> 要途经的景点编号集
        :param endVertex: <int> 终点景点编号
        :param isCircut: <bool> 是否求解哈密顿回路
        :return: <tuple> 元组第一个元素代表最短路径长度，第二个元素代表具体的最短路径 
        """
        def searchSmallScaleHamiltonCircut(self, startVertex: int, vertexSet: list,endVertex: int = None,isCircuit: bool = True) -> (int, list):
            """
            求从一个顶点出发，经过点集中顶点一次，回到该顶点的哈密顿回路长度及路径,要求顶点集的规模较小
                  
            :param startvertex: <int> 起点景点编号
            :param vertexSet: <list> 要经过的顶点编号集合:
            :Return:<tuple> 元组第一个元素代表最短路径长度，第二个元素代表具体的最短路径        
            """
            # 将起始顶点作为经过顶点集的第0个点
            vertexSet.insert(0, startVertex)

            # 存储路径信息，path内存放景点编号
            path = [vertexSet[0]]
            # 共经过几个景点
            n = len(vertexSet)
            # 除起始景点外所有景点集合的子集数
            m = 2 ** (n - 1)
            # 动态规划计算表格，用于记录从当前顶点经过对应子集中所有顶点一次且仅一次，并回到起始点的最短路径长度
            dp = [[np.inf] * m for i in range(n)]
            # 与 dp 表一一对应，记录遍历当前表项对应子集的那段路径中的首个结点，用于还原路径
            # 例如 当前表项对应子集 {1,3}，得到其记录的最小距离的路径为 {0,3,1,0},则 prev 表该位置为 3
            prev = [[-1] * m for i in range(n)]

            if isCircuit:
                endVertex = startVertex

            # 初始化过程表
            for i in range(1, n):
                dp[i][0] = self.queryWeightByTwoVertexes(vertexSet[i], endVertex)

            # 依次处理每一个子集数组
            for j in range(1, m):
                for i in range(1, n):
                    # 使用状态压缩的方法判断子集中是否包含景点i
                    if not (j & (1 << (i - 1))):
                        # 依次处理子集中的每个元素k
                        for k in range(1, n):
                            if j & (1 << (k - 1)):
                                tmp = self.queryWeightByTwoVertexes(vertexSet[i], vertexSet[k]) + dp[k][j - (1 << (k - 1))]
                                if tmp < dp[i][j]:
                                    dp[i][j] = tmp
                                    prev[i][j] = k

            # 完成第0行最后一列，即路径长度的计算
            for i in range(1, n):
                tmp = self.queryWeightByTwoVertexes(vertexSet[i], vertexSet[0]) + dp[i][m - 1 - (1 << (i - 1))]
                if tmp < dp[0][m - 1]:
                    dp[0][m - 1] = tmp
                    prev[0][m - 1] = i

            # 回溯得到路径
            row = 0
            col = m - 1
            if prev[row][col] == -1:
                return np.inf, []
            while col != 0:
                point = prev[row][col]
                path.append(vertexSet[point])
                col -= (1 << (point - 1))
                row = point

            path.append(endVertex)
            return dp[0][m - 1], path

        def searchLargeScaleHamilton(self, startVertex: int,vertexSet: list,endVertex: int = None,isCircuit: bool = True) -> (int,list):
            """
            使用优化邻域选择的禁忌搜索求解最优哈密顿回路或通路，要求顶点集规模较大

            :param startVertex: <int> 出发景点编号
            :param vertexSet: <list> 要途经的景点编号集
            :param endVertex: <int> 终点景点编号
            :param isCircut: <bool> 是否求解哈密顿回路
            :return: <tuple> 元组第一个元素代表最短路径长度，第二个元素代表具体的最短路径        
            """
            def getLen(path: list) -> (int):
                """
                求解特定回(通)路长度

                :param path: <list> 待求回路(通路)序列
                :return distance: <int> 所求回路长度
                """
                distance = self.queryWeightByTwoVertexes(startVertex,path[0])
                for i in range(len(path) - 1):
                    distance += self.queryWeightByTwoVertexes(path[i],path[i + 1])

                #如果是回路要最后加上终点到起点的位置
                distance += ((self.queryWeightByTwoVertexes(path[-1],startVertex)) if isCircuit else self.queryWeightByTwoVertexes(path[-1],endVertex))
                return distance

            def getAllLens(pathSets: list) -> (list):
                """
                求解列表中所有回(通)路长度

                :param pathSets: <list> 为多条路径构成列表，它的每一个元素都是一条回路或通路
                :return distanceList: <list> 每一个元素对应着PathSets中相应索引处路径的长度        
                """
                distanceList = [getLen(path) for path in pathSets]
                return distanceList

            def findNeighbors(bestpath:list) -> (list):
                """
                求解局部最优路径的邻域

                :param bestpath: <list> 当前局部最优路径，根据禁忌搜索算法，需要在其邻域附近进行搜索
                :return neighbors: <list> 每一个元素都是当前局部最优路径的邻域        
                """
                neighbors = []

                # 根据“三角形两边之和大于第三边”搜索邻域
                for i in range(len(vertexSet) - 1):
                    for j in range(i + 1,len(vertexSet)):
                        path = bestpath.copy()
                        path[i + 1:j + 1] = path[j:i:-1]
                        neighbors.append(path)

                # 根据“平滑多边形路径的凸度”搜索邻域     
                for i in range(len(vertexSet) - 1):
                    for j in range(i + 1,len(vertexSet) + 1):
                        path = bestpath.copy()
                        path.insert(j + 1,path[i])
                        del path[i]
                        neighbors.append(path)

                # 传统的邻域搜索方式，随机交换路径上的两个顶点
                for i in range(len(vertexSet) - 1):
                    for j in range(i + 1,len(vertexSet)):
                        path = bestpath.copy()
                        path[i],path[j] = path[j],path[i]
                        neighbors.append(path)

                return neighbors

            # tabooList为禁忌表
            tabooList = []
            # tabooList为禁忌表最大长度，为超参数
            tabooMaxLen = len(vertexSet) // 2
            # 禁忌搜索最大迭代次数
            maxiter = 1000
            # 早停法的阈值
            earlyStoppingThrehold = 150

            # 选择一条较优的路径序列作为搜索起点
            initialPathList = [vertexSet]
            cnt = 0
            for i in range(maxiter):
                tmpSet = vertexSet.copy()
                random.shuffle(tmpSet)
                initialPathList.append(tmpSet)

            initialDisList = getAllLens(initialPathList)
            # initialBestpath与ininitialBestdis分别为初始的路径序列及其长度
            initialBestdis = min(initialDisList)
            initialBestpath = initialPathList[initialDisList.index(initialBestdis)]

            # 将初始序列加入禁忌表，并初始化局部最优解和全局最优解
            localBestpath,localBestdis = initialBestpath,getLen(initialBestpath)
            globalBestpath,globalBestdis = localBestpath,localBestdis
            tabooList.append(vertexSet)

            # 迭代禁忌搜索
            for i in range(maxiter):
                newPathList = findNeighbors(localBestpath)
                newDisList = getAllLens(newPathList)

                localBestdis = min(newDisList)
                localBestpath = newPathList[newDisList.index(localBestdis)]

                # 当前局部最优优于全局最优
                if localBestdis < globalBestdis:
                    # 更改全局最优并将其加入禁忌表
                    globalBestpath = localBestpath
                    globalBestdis = localBestdis

                    if globalBestpath not in tabooList:
                        tabooList.append(globalBestpath)
            
                # 当前局部最优劣于全局最优
                else:
                    cnt += 1

                    # 若当前局部最优在禁忌表中，选择局部次优解进一步搜索，否则将其加入禁忌表
                    if localBestpath in tabooList:
                        newPathList.remove(localBestpath)
                        newDisList.remove(localBestdis)
                        localBestdis = min(newDisList)
                        localBestpath = newPathList[newDisList.index(localBestdis)]
                        tabooList.append(localBestpath)

                    else:
                        tabooList.append(localBestpath)

                # 超过禁忌表最大长度则删除最早加入禁忌表的路径
                if len(tabooList) >= tabooMaxLen:
                    del tabooList[0] 

                # 早停
                if cnt > earlyStoppingThrehold:
                    break

            # 返回结果
            if isCircuit:
                return globalBestdis,[startVertex] + globalBestpath + [startVertex]
            else:
                return globalBestdis,[startVertex] + globalBestpath + [endVertex]

        # 将查询记录写入日志
        self.logFunc(startVertex, vertexSet)
        # 根据问题规模选择相应的算法
        if len(vertexSet) <= 5:
            return searchSmallScaleHamiltonCircut(self, startVertex, vertexSet, endVertex, isCircuit)
        else:
            return searchLargeScaleHamilton(self, startVertex, vertexSet, endVertex, isCircuit)

    def searchPathByDijkstra(self, startVertex: int, endVertex: int) -> list:
        """
        根据起点startVertex终点endVertex搜索最短路径

        :param startVertex: <int> 起点编号
        :param endVertex: <int> 终点编号
        :return result:<list> 记录路径的列表
        """

        # 将查询记录写入日志
        self.logFunc(startVertex, [endVertex])
        #构建完整路径图
        e = np.zeros((self.__size, self.__size))

        #权重初始化
        for i in range(self.__size):
            for j in range(i + 1):
                w = self.queryWeightByTwoVertexes(i, j)
                e[i,j],e[j,i] = (w,w) if i != j else (0,0)

        res = np.zeros(self.__size)
        vis = np.zeros(self.__size)
        #path记录该起点到其他点的全部路径
        path= np.zeros(self.__size)
        #查找出起点到终点的路径
        pathCh = np.zeros(self.__size)
        #重新整理路径
        result = np.zeros(self.__size)

        vis[startVertex] = 1
        for i in range (self.__size):
            res[i],path[i],pathCh[i] = e[startVertex][i],-1,-1

        # Dijkstra算法求单源最短路径
        for t in range (self.__size):
            minn,temp = float("inf"),0
            # 求距离startVertex最近的点
            for i in range (self.__size):
                if (vis[i] == 0 and res[i] < minn):
                    minn,temp = res[i],i
            vis[temp] = 1

            # 用该点松弛各边
            for i in range (self.__size):
                if(e[temp][i] + res[temp] < res[i] and vis[i] == 0):
                    res[i] = e[temp][i] + res[temp]
                    path[i] = temp

        #路径回溯
        p,res = endVertex,[endVertex]
        while path[p] != -1:
            res.append(int(path[p]))
            p = int(path[p])
        res = res + [startVertex]

        return (res[::-1])

    def getAllPaths(self, startVertex: int, endVertex: int, path: list = []):
        """
        求两点之间适宜距离内的所有路径

        :param startVertex: <int> 起点编号
        :param endVertex: <int> 终点编号
        :param path: <list> 单次路径记录
        :return paths: <list> 记录两点之间的所有路径
        """

        # 使用深度优先搜索(DFS)搜索两点之间的所有路径
        path = path + [startVertex]
        if startVertex == endVertex:
            return [path]
        paths = []
        for edges in self.queryEdgesByVertex(startVertex):
            # 剪枝
            if (edges[1] not in path) and (edges[-1] != np.inf) and (self.queryDisByTwoVertexes(edges[1],endVertex) != np.inf) and len(path) <= 4:
                nextpaths = self.getAllPaths(edges[1],endVertex,path)
                for nextpath in nextpaths:
                    paths.append(nextpath)
        return paths

    def searchKShortestPath(self,startVertex: int,endVertex: int,k: int = 4) -> (list):
        """
        求两点之间的k短路

        :param startVertex: <int> 起点编号
        :param endVertex: <int> 终点编号
        :param k: <int> 待求前k短路
        :return: <list> 每个元素是一个元组,第i个元组的第一个值代表路径第i短路径的长度，第i个元组的第二个值代表第i短路径
        """

        class vertexEval(object):
            """
            Features
            -----------------------------------------
            为了方便A*搜索,建立了一个类储存节点及其估值函数的值
            Members
            ----------------------------------------
            :param vertex: <int> 当前搜索位置所处的节点编号
            :param h: <int> 从当前节点到终点估计要走的路径长度
            :param f: <int> 总花费的估计
            :param path: <list> 记录路径

            Functions
            ----------------------------------------
            __init__(self,vertex,h,f,path): 新建类
            __lt__(self,other): 重载小于运算符
            """

            def __init__(self,vertex: int,h: int,f: int,path: list = []):
                """
                初始化方法
                :params: 详见上方注释
                """
                self.vertex = vertex
                self.h = h
                self.f = f
                self.path = path
            def __lt__(self,other):
                """
                重载小于运算符
                :params:other 该类的其它对象
                """
                return self.f < other.f

        # 初始化堆及计数器
        priorityQueue = []
        disAndPaths = []
        vis = [0 for i in range(self.__size)]
        cnt = 0
        heappush(priorityQueue,vertexEval(startVertex,0,0,[startVertex]))

        while(True):
            # 结果返回
            if(cnt == k):
                return disAndPaths
            # 取出估值代价最少的节点
            cur = heappop(priorityQueue)
            vis[cur.vertex] += 1
            # 到达终点，先到达的一定路径长度更短
            if(cur.vertex == endVertex):
                disAndPaths.append((cur.h,cur.path))
                cnt += 1
                continue
            # 剪枝，证明详见报告
            if(vis[cur.vertex] > k):
                continue
            # 遍历该节点所有的邻接节点，将其加入堆中，并更新估值函数的值
            for edge in self.queryEdgesByVertex(cur.vertex):
                if(edge[-1] != np.inf):
                    heappush(priorityQueue,vertexEval(edge[1],cur.h + edge[-1],
                        cur.h + edge[-1] + self.queryDisByTwoVertexes(edge[1],endVertex),cur.path+[edge[1]]))

    @staticmethod
    def getPathList(queryEdgesByVertex, nextPathList: List[List[int]], gonePointDict: Dict[int, int],
                    distance: int) -> None:
        """
        依据当前节点及其到达出发点的距离更新节点计算列表和节点最短距离字典

        :param queryEdgesByVertex: <def> 邻接节点及距离的获取函数
        :param nextPathList: <list> 节点计算列表，构成：[[节点, 到达节点的距离], ...]
        :param gonePointDict: <dict> 节点最短距离字典
        :param distance: <int> 限制的距离查找范围
        """
        # 取出当前需要计算的第一个节点
        curvertex, nowdistance = nextPathList[0]
        del nextPathList[0]

        # 取出该节点的邻接节点及路径长度
        pathList = queryEdgesByVertex(curvertex)

        i = 0
        while i < len(pathList):
            if pathList[i][2] == np.inf:
                # 删除不存在的路径
                del pathList[i]
            else:
                del pathList[i][0]
                # 计算节点到达出发点的距离
                pathList[i][1] += nowdistance
                i += 1

        for num, pathLen in pathList:
            if pathLen > distance:
                continue  # 距离大于查找范围，剪枝
            if num in gonePointDict.keys():
                if gonePointDict[num] < pathLen:
                    continue  # 距离大于先前获得的值，剪枝
            # 添加至节点计算列表，更新节点最短距离字典
            gonePointDict[num] = pathLen
            nextPathList.append([num, pathLen])

    def SearchWithinDistance(self, curvertex: int, distance: int) -> List[Tuple[int, int]]:
        """
        求在当前景点一定距离内的景点(广度优先搜索算法，及时剪枝)

        :param queryEdgesByVertex: <def> 邻接节点及距离的获取函数
        :param curvertex: <int> 当前所在地景点编号
        :param distance: <int> 距离阈值
        :return: <list> 距离当前顶点距离在阈值内的景点编号及长度
        """
        # 初始化节点计算列表和节点最短距离字典
        nextPathList = [[curvertex, 0]]
        gonePointDict = {curvertex: 0}

        # 迭代至节点计算列表为空，即已遍历distance内所有节点
        while len(nextPathList) > 0:
            self.getPathList(self.queryEdgesByVertex, nextPathList, gonePointDict, distance)

        del gonePointDict[curvertex]
        # 排序后输出
        return sorted(gonePointDict.items(), key=lambda x: x[1])


if __name__ == '__main__':
    # 测试稀疏图类

    # 所建图共有23个顶点
    log = QueryLogManager.QueryLogManager('../QueryLog/queryLog.history')
    g = GraphEdges('Graph.csv',log.addQueryLog)


    print("--------------Test Func: queryEdgeByTwoVertexes-----------------")
    # 查询景点11与景点12间的路径信息
    print(g.queryEdgeByTwoVertexes(11, 12))
    print(g.queryEdgeByTwoVertexes(12, 11))

    # 查询景点13与景点17间的路径信息
    print(g.queryEdgeByTwoVertexes(13, 17))
    print(g.queryEdgeByTwoVertexes(17, 13))

    # 查询景点0与景点22间的路径信息
    print(g.queryEdgeByTwoVertexes(0, 22))
    print(g.queryEdgeByTwoVertexes(22, 0))

    print("--------------------Test One Over ------------------------")

    print("--------------Test Func: queryWeightByTwoVertexes-----------------")
    # 查询景点11与景点12间的路径长度
    print(g.queryWeightByTwoVertexes(11, 12))
    print(g.queryWeightByTwoVertexes(12, 11))

    # 查询景点13与景点17间的路径长度
    print(g.queryWeightByTwoVertexes(13, 17))
    print(g.queryWeightByTwoVertexes(17, 13))

    # 查询景点0与景点22间的路径长度
    print(g.queryWeightByTwoVertexes(0, 22))
    print(g.queryWeightByTwoVertexes(22, 0))

    print("--------------------Test Two Over ------------------------")

    print("--------------Test Func: queryDisByTwoVertexes-----------------")
    # 查询景点11与景点12间的实际距离
    print(g.queryDisByTwoVertexes(11, 12))
    print(g.queryDisByTwoVertexes(12, 11))

    # 查询景点13与景点17间的实际距离
    print(g.queryDisByTwoVertexes(13, 17))
    print(g.queryDisByTwoVertexes(17, 13))

    # 查询景点0与景点22间的实际距离
    print(g.queryDisByTwoVertexes(0, 22))
    print(g.queryDisByTwoVertexes(22, 0))

    print("--------------------Test Three Over ------------------------")

    print("--------------Test Func: queryEdgesByVertex-----------------")
    # 查询与0邻接的路径的信息
    print(g.queryEdgesByVertex(0))

    # 查询与8邻接的路径的信息
    print(g.queryEdgesByVertex(8))

    # 查询与22邻接的路径的信息
    print(g.queryEdgesByVertex(22))

    print("--------------------Test Four Over ------------------------")

    print("--------------Test Func: searchHamilton-----------------")
    # 查询0为起点,经过[1-4]的哈密顿回路
    print(g.searchHamilton(0,list(range(1,4))))

    # 查询0为起点,经过[1-11]的哈密顿回路
    print(g.searchHamilton(0,list(range(1,11))))

    # 查询4为起点,经过[5-8]的哈密顿回路
    print(g.searchHamilton(4,list(range(5,8))))

    # 查询0为起点,经过[1-23]的哈密顿回路
    print(g.searchHamilton(0,list(range(1,23))))

    print("--------------------Test Five Over ------------------------")

    print("--------------Test Func: searchPathByDijkstra-----------------")
    # 查询景点11与景点12间的最短路径
    print(g.searchPathByDijkstra(11, 12))
    print(g.searchPathByDijkstra(12, 11))

    # 查询景点13与景点17间的最短路径
    print(g.searchPathByDijkstra(13, 17))
    print(g.searchPathByDijkstra(17, 13))

    # 查询景点0与景点22间的最短路径
    print(g.searchPathByDijkstra(0, 22))
    print(g.searchPathByDijkstra(22, 0))

    print("--------------------Test Six Over ------------------------")

    print("--------------Test Func: getAllPaths-----------------")
    # 查询景点11与景点12间的所有路径的数目
    print(len(g.getAllPaths(11, 12)))

    # 查询景点13与景点17间的所有路径的数目
    print(len(g.getAllPaths(13, 17)))

    # 查询景点0与景点22间的最短路径
    print(len(g.getAllPaths(0, 22)))

    print("--------------------Test Seven Over ------------------------")

    print("--------------Test Func: searchKShortestPath-----------------")
    # 查询景点11与景点12间的所有路径的数目
    print(g.searchKShortestPath(11, 12))

    # 查询景点13与景点17间的所有路径的数目
    print(g.searchKShortestPath(13, 17))

    # 查询景点0与景点22间的最短路径
    print(g.searchKShortestPath(0, 22))

    print("--------------------Test Eight Over ------------------------")
