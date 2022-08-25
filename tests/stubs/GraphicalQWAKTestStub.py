import networkx as nx

from qwak.GraphicalQWAK import GraphicalQWAK


class GraphicalQWAKTestStub:
    def __init__(self, testGQwak=None):
        staticN = 100
        dynamicN = staticN
        staticTime = 12
        initState = [staticN // 2, (staticN // 2) + 1]
        staticGraph = nx.cycle_graph(staticN)
        dynamicGraph = nx.cycle_graph(dynamicN)
        dynamicTimeList = [0, 12]
        initStateList = [[staticN // 2, (staticN // 2) + 1]]
        if testGQwak is None:
            self.gQwak = GraphicalQWAK(
                staticN=staticN,
                dynamicN=dynamicN,
                staticGraph=staticGraph,
                dynamicGraph=dynamicGraph,
                staticStateList=initState,
                dynamicStateList=initStateList,
                staticTime=staticTime,
                dynamicTimeList=dynamicTimeList,
            )
        else:
            self.gQwak = testGQwak

    def runWalk(self):
        return self.gQwak.runWalk()

    def runMultipleWalks(self):
        return self.gQwak.runMultipleWalks()

    def getStaticProbVec(self):
        return self.gQwak.getStaticProbVec()

    def getDynamicProbVecList(self):
        return self.gQwak.getDynamicProbVecList()

    def setStaticDim(self,newDim,graphStr):
        self.gQwak.setStaticDim(newDim,graphStr)

    def setDynamicDim(self, newDim, graphStr):
        self.gQwak.setDynamicDim(newDim,graphStr)

    def getStaticDim(self):
        return self.gQwak.getStaticDim()

    def getDynamicDim(self):
        return self.gQwak.getDynamicDim()

    def getStaticAdjacencyMatrix(self):
        return self.gQwak.getStaticAdjacencyMatrix()

    def getDynamicAdjacencyMatrix(self):
        return self.gQwak.getDynamicAdjacencyMatrix()

    def setStaticInitState(self,initStateStr):
        self.gQwak.setStaticInitState(initStateStr)

    def setDynamicInitStateList(self, newInitStateList):
        self.gQwak.setDynamicInitStateList(newInitStateList)

    def getStaticInitState(self):
        return self.gQwak.getStaticInitState()

    def getDynamicInitStateList(self):
        return self.gQwak.getDynamicInitStateList()

    def setStaticGraph(self, newGraphStr):
        self.gQwak.setStaticGraph(newGraphStr)

    def setDynamicGraph(self, newGraphStr):
        self.gQwak.setDynamicGraph(newGraphStr)

    def getStaticGraph(self):
        return self.gQwak.getStaticGraph()

    def getDynamicGraph(self):
        return self.gQwak.getDynamicGraph()