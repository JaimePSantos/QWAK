from qwak.qwak import QWAK
from qwak.ProbabilityDistribution import ProbabilityDistribution
from qwak.QuantumWalk import QuantumWalk
from qwak.operator import Operator
from qwak.State import State

import json
import timeit
from matplotlib import pyplot as plt
import numpy as np
import networkx as nx
import eel
import os
dirname = os.path.dirname(__file__)
guiPath = os.path.join(dirname, '../GraphicalInterface')
eel.init(guiPath)

#TODO: Aba ou menu para Plot. Media e desvio padrao. Aba para caminhada estatica e dinamica.
#TODO: Grafico de animacao do JavaScript mexe com o tamanho dos picos.
#TODO: Formularios para introduzir parametros.

if __name__ == '__main__':
    global n, t, initState, staticQuantumWalk
    n = 100
    t = 10
    # initState = [int(n/2),int(n/2)+1]
    initState = [50,51]
    graph = nx.cycle_graph(n)
    staticQuantumWalk = QWAK(graph)
    staticQuantumWalk.runWalk(t, initState)

    global timeList,initStateList,dynamicQuantumWalk,dynProbDistList, dynAmpsList
    timeList = [0,100]
    initStateList = [[int(n/2),int(n/2)+1]]
    dynamicQuantumWalk = QWAK(graph)
    dynamicQuantumWalk.runWalk(timeList[0], initStateList[0])
    dynProbDistList = []
    dynAmpsList = []

    resultRounding = 3

    @eel.expose
    def getStaticMean():
        return round(staticQuantumWalk.getMean(),resultRounding)

    @eel.expose
    def getStaticSndMoment():
        return round(staticQuantumWalk.getSndMoment(),resultRounding)

    @eel.expose
    def getStaticStDev():
        return round(staticQuantumWalk.getStDev(),resultRounding)

    @eel.expose
    def getStaticSurvivalProb(k0,k1):
        return round(staticQuantumWalk.getSurvivalProb(k0,k1),resultRounding)

    @eel.expose
    def getInversePartRatio():
        return round(staticQuantumWalk.getInversePartRatio(),resultRounding)

    @eel.expose
    def checkPST(nodeA,nodeB):
        pst = staticQuantumWalk.checkPST(nodeA,nodeB)
        return str(pst)

    @eel.expose
    def setTimeList(newTimeList):
        global timeList
        timeList = list(map(float,newTimeList.split(',')))

    @eel.expose
    def setInitStateList(newInitStateList):
        global initStateList
        initStateList = []
        parsedInitState = newInitStateList.split(';')
        for initState in parsedInitState:
            initStateList.append(list(map(int,initState.split(','))))

    @eel.expose
    def setInitState(initStateStr):
        global initState
        initState = list(map(int,initStateStr.split(',')))
        newState = State(staticQuantumWalk.getDim())
        newState.buildState(initState)
        staticQuantumWalk.setInitState(newState)

    @eel.expose
    def getInitState():
        return staticQuantumWalk.getInitState()
        
    @eel.expose
    def setDim(newDim,graphStr):
        global staticQuantumWalk, dynamicQuantumWalk
        staticQuantumWalk.setDim(newDim, graphStr)
        dynamicQuantumWalk.setDim(newDim, graphStr)

    @eel.expose
    def getDim():
        return staticQuantumWalk.getDim()
        
    @eel.expose
    def setGraph(newGraph):
        global staticQuantumWalk, dynamicQuantumWalk
        newStaticGraph = eval(newGraph + f"({staticQuantumWalk.getDim()})")
        newDynamicGraph = eval(newGraph + f"({dynamicQuantumWalk.getDim()})")
        staticQuantumWalk.setGraph(newStaticGraph)
        dynamicQuantumWalk.setGraph(newDynamicGraph)

    @eel.expose
    def getGraph():
        return staticQuantumWalk.getGraph()

    @eel.expose
    def setTime(newTime):
        global staticQuantumWalk,t
        t=newTime
        staticQuantumWalk.setTime(newTime)
    
    @eel.expose
    def getTime():
        return staticQuantumWalk.getTime()

    @eel.expose
    def runWalk():
        global staticQuantumWalk,n,t,initState
        # staticQuantumWalk.resetWalk()
        staticQuantumWalk.runWalk(t,initState)
        qwProbabilities = staticQuantumWalk.getProbDist()
        qwProbVec = qwProbabilities.getProbVec()
        probLists = qwProbVec.tolist()
        return probLists
    
    @eel.expose
    def runMultipleWalks():
        qwProbVecList = []
        global timeList,initStateList,dynamicQuantumWalk,dynProbDistList,dynAmpsList
        dynamicQuantumWalk.resetWalk()
        dynProbDistList = []
        dynAmpsList = []
        timeRange = np.linspace(timeList[0],timeList[1],int(timeList[1]))
        for t in timeRange:
            dynamicQuantumWalk.runWalk(t, initStateList[0])
            qwProbabilities = dynamicQuantumWalk.getProbDist()
            qwAmps = dynamicQuantumWalk.getWalk()
            dynAmpsList.append(qwAmps)
            dynProbDistList.append(qwProbabilities)
            qwProbVec = qwProbabilities.getProbVec()
            probLists = qwProbVec.tolist()
            qwProbVecList.append(probLists)
        return qwProbVecList

    @eel.expose
    def getDynMean():
        meanList = []
        global dynProbDistList
        for probDist in dynProbDistList:
            meanList.append(probDist.mean())
        return meanList

    @eel.expose
    def getDynStDev():
        stDevList = []
        global dynProbDistList
        for probDist in dynProbDistList:
            stDevList.append(probDist.stDev())
        return stDevList

    @eel.expose
    def getDynInvPartRatio():
        invPartRatioList = []
        global dynAmpsList
        for amps in dynAmpsList:
            invPartRatioList.append(amps.invPartRatio())
        return invPartRatioList

    @eel.expose
    def getDynSurvivalProb(k0,k1):
        survProbList = []
        global dynAmpsList
        for probDist in dynProbDistList:
            survProbList.append(probDist.survivalProb(k0,k1))
        return survProbList

    @eel.expose
    def graphToJson():
        graph = staticQuantumWalk.getGraph()
        myCytGraph = nx.cytoscape_data(graph)
        return myCytGraph

    @eel.expose
    def customGraphWalk():
        global staticQuantumWalk, dynamicQuantumWalk
        adjM = np.matrix(eel.sendAdjacencyMatrix()()['data'])
        staticQuantumWalk.setAdjacencyMatrix(adjM)
        staticQuantumWalk.runWalk(t, initState)
        dynamicQuantumWalk.setAdjacencyMatrix(adjM)
        dynamicQuantumWalk.runWalk(t,initState)

    eel.start('index.html', port=8080, cmdline_args=['--start-maximized'])

        
    pass
