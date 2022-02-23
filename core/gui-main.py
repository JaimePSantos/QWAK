from qwak.qwak import QWAK
from qwak.ProbabilityDistribution import ProbabilityDistribution
from qwak.QuantumWalk import QuantumWalk
from qwak.Operator import Operator
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
    t = 30
    # initState = [int(n/2),int(n/2)+1]
    initState = [50,51]
    graph = nx.cycle_graph(n)
    staticQuantumWalk = QWAK(graph)
    staticQuantumWalk.runWalk(t, initState)

    global timeList,initStateList,dynamicQuantumWalk
    timeList = [0,100]
    initStateList = [[int(n/2),int(n/2)+1]]
    dynamicQuantumWalk = QWAK(graph)
    dynamicQuantumWalk.runWalk(timeList[0], initStateList[0])

    @eel.expose
    def getStaticMean():
        return round(staticQuantumWalk.getMean(),3)

    @eel.expose
    def getStaticSndMoment():
        return round(staticQuantumWalk.getSndMoment(),3)

    @eel.expose
    def getStaticStDev():
        return round(staticQuantumWalk.getStDev(),3)

    @eel.expose
    def getStaticSurvivalProb(k0,k1):
        return round(staticQuantumWalk.getSurvivalProb(k0,k1),3)

    @eel.expose
    def getInversePartRatio():
        return round(staticQuantumWalk.getInversePartRatio(),3)

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
        qwProbList = []
        global timeList,initStateList,dynamicQuantumWalk
        dynamicQuantumWalk.resetWalk()
        timeRange = np.linspace(timeList[0],timeList[1],int(timeList[1]))
        for t in timeRange:
            dynamicQuantumWalk.runWalk(t, initStateList[0])
            qwProbabilities = dynamicQuantumWalk.getProbDist()
            qwProbVec = qwProbabilities.getProbVec()
            probLists = qwProbVec.tolist()
            qwProbList.append(probLists)
        return qwProbList

    @eel.expose
    def graphToJson():
        graph = staticQuantumWalk.getGraph()
        myCytGraph = nx.cytoscape_data(graph)
        return myCytGraph

    @eel.expose
    def printAdjacencyMatrix():
        global staticQuantumWalk, dynamicQuantumWalk
        adjM = np.matrix(eel.sendAdjacencyMatrix()()['data'])
        staticQuantumWalk.setAdjacencyMatrix(adjM)
        staticQuantumWalk.runWalk(t, initState)


    eel.start('index.html', port=8080, cmdline_args=['--start-maximized'])

        
    pass
