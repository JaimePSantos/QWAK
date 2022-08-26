import os

import eel
import networkx as nx
import numpy as np

from qwak.GraphicalQWAK import GraphicalQWAK
from qwak.Errors import StateOutOfBounds, NonUnitaryState, UndefinedTimeList, EmptyProbDistList,MissingNodeInput

dirname = os.path.dirname(__file__)
guiPath = os.path.join(dirname, "../GraphicalInterface")
eel.init(guiPath)

# TODO: Aba ou menu para Plot. Media e desvio padrao. Aba para caminhada estatica e dinamica.
# TODO: Formularios para introduzir parametros.

if __name__ == "__main__":
    staticN = 100
    dynamicN = 100
    t = 10
    initState = [staticN // 2]
    staticGraph = nx.cycle_graph(staticN)
    dynamicGraph = nx.cycle_graph(dynamicN)
    timeList = [0, 100]
    initStateList = [[dynamicN // 2, (dynamicN // 2) + 1]]

    gQwak = GraphicalQWAK(
        staticN,
        dynamicN,
        staticGraph,
        dynamicGraph,
        initState,
        initStateList,
        t,
        timeList)

    resultRounding = 4

    @eel.expose
    def runWalk():
        return gQwak.runWalk()

    @eel.expose
    def runMultipleWalks():
        return gQwak.runMultipleWalks()

    @eel.expose
    def setStaticDim(newDim, graphStr):
        gQwak.setStaticDim(newDim, graphStr)

    @eel.expose
    def setDynamicDim(newDim, graphStr):
        gQwak.setDynamicDim(newDim, graphStr)

    @eel.expose
    def getDim():
        return gQwak.getDim()

    @eel.expose
    def getStaticDim():
        return gQwak.getStaticDim()

    @eel.expose
    def getDynamicDim():
        return gQwak.getDynamicDim()

    @eel.expose
    def setStaticGraph(newGraph):
        gQwak.setStaticGraph(newGraph)

    @eel.expose
    def setDynamicGraph(newGraph):
        gQwak.setDynamicGraph(newGraph)

    @eel.expose
    def getStaticGraph():
        return gQwak.getStaticGraph()

    @eel.expose
    def getDynamicGraph():
        return gQwak.getDynamicGraph()

    @eel.expose
    def getStaticGraphToJson():
        return gQwak.getStaticGraphToJson()

    @eel.expose
    def getDynamicGraphToJson():
        return gQwak.getDynamicGraphToJson()

    @eel.expose
    def setTime(newTime):
        # TODO: Change name of function here and in JS
        gQwak.setStaticTime(newTime)

    @eel.expose
    def getTime():
        # TODO: Change name of function here and in JS
        return gQwak.getStaticTime()

    @eel.expose
    def setDynamicTime(newTime):
        gQwak.setDynamicTime(newTime)
        pass

    @eel.expose
    def getDynamicTime():
        return gQwak.getDynamicTime()

    @eel.expose
    def setInitState(initStateStr):
        gQwak.setStaticInitState(initStateStr)

    @eel.expose
    def setInitStateList(newInitStateList):
        gQwak.setDynamicInitStateList(newInitStateList)

    @eel.expose
    def getInitState():
        return gQwak.getStaticInitState()

    @eel.expose
    def getStaticMean():
        return round(gQwak.getStaticMean(), resultRounding)

    @eel.expose
    def getDynMean():
        return gQwak.getDynamicMean()

    @eel.expose
    def getStaticSndMoment():
        return round(gQwak.getStaticSndMoment(), resultRounding)

    @eel.expose
    def getStaticStDev():
        return round(gQwak.getStaticStDev(), resultRounding)

    @eel.expose
    def getDynStDev():
        return gQwak.getDynamicStDev()

    @eel.expose
    def getStaticSurvivalProb(k0, k1):
        survProb = gQwak.getStaticSurvivalProb(k0, k1)
        if not survProb[0]:
            survProb[1] = round(survProb[1], resultRounding)
        return survProb
    @eel.expose
    def getDynSurvivalProb(k0, k1):
        survProbList = gQwak.getDynamicSurvivalProb(k0, k1)
        if not survProbList[0]:
            survProbList[1] = list(map(lambda survProb: round(survProb,resultRounding),survProbList[1]))
        return survProbList

    @eel.expose
    def getInversePartRatio():
        return round(gQwak.getStaticInversePartRatio(), resultRounding)

    @eel.expose
    def getDynInvPartRatio():
        return gQwak.getDynamicInvPartRatio()

    @eel.expose
    def checkPST(nodeA, nodeB):
        pst = gQwak.checkPST(nodeA, nodeB)
        return pst

    @eel.expose
    def customGraphWalk():
        adjM = np.matrix(eel.sendAdjacencyMatrix()()["data"])
        gQwak.customGraphWalk(adjM)

    eel.start(
        "index.html",
        port=8080,
        cmdline_args=["--start-maximized"])

    pass
