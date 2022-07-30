import os

import eel
import networkx as nx
import numpy as np
import copy

from qwak.Errors import StateOutOfBounds
from qwak.State import State
from qwak.qwak import QWAK
from GraphicalQWAK import GraphicalQWAK

dirname = os.path.dirname(__file__)
guiPath = os.path.join(dirname, "../GraphicalInterface")
eel.init(guiPath)

# TODO: Aba ou menu para Plot. Media e desvio padrao. Aba para caminhada estatica e dinamica.
# TODO: Formularios para introduzir parametros.

if __name__ == "__main__":
    global n, t, initState, staticQuantumWalk
    n = 100
    t = 10
    initState = [n//2]
    graph = nx.cycle_graph(n)
    timeList = [0, 100]
    initStateList = [[int(n / 2), int(n / 2) + 1]]

    gQwak = GraphicalQWAK(n, graph, initState, initStateList, t, timeList)

    resultRounding = 4

    @eel.expose
    def runWalk():
        return gQwak.runWalk()

    @eel.expose
    def runMultipleWalks():
        return gQwak.runMultipleWalks()

    @eel.expose
    def setDim(newDim, graphStr):
        global staticQuantumWalk, dynamicQuantumWalk
        gQwak.setDim(newDim,graphStr)

    @eel.expose
    def getDim():
        return gQwak.getDim()

    @eel.expose
    def setGraph(newGraph):
        gQwak.setGraph(newGraph)

    @eel.expose
    def getGraph():
        return gQwak.getGraph()

    @eel.expose
    def graphToJson():
        return gQwak.getGraphToJson()

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

        pass

    @eel.expose
    def getDynamicTime():
        pass

    @eel.expose
    def setTimeList(newTimeList):
        gQwak.setDynamicTime(newTimeList)

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
        return round(gQwak.getStaticSurvivalProb(k0, k1), resultRounding)

    @eel.expose
    def getDynSurvivalProb(k0, k1):
        return gQwak.getDynamicSurvivalProb(k0,k1)

    @eel.expose
    def getInversePartRatio():
        return round(gQwak.getStaticInversePartRatio(), resultRounding)

    @eel.expose
    def getDynInvPartRatio():
        return gQwak.getDynamicInvPartRatio()

    @eel.expose
    def checkPST(nodeA, nodeB):
        pst = staticQuantumWalk.checkPST(nodeA, nodeB)
        return str(pst)

    @eel.expose
    def customGraphWalk():
        adjM = np.matrix(eel.sendAdjacencyMatrix()()["data"])
        gQwak.customGraphWalk(adjM)

    eel.start("index.html", port=8080, cmdline_args=["--start-maximized"])

    pass
