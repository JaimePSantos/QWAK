from QuantumWalk.QWAK import QWAK
from QuantumWalk.ProbabilityDistribution import ProbabilityDistribution
from QuantumWalk.QuantumWalk import QuantumWalk
from QuantumWalk.Operator import Operator
from QuantumWalk.State import State

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
    global n, t, gamma, initState, staticQuantumWalk
    n = 100
    t = 30
    gamma = 1/(2*np.sqrt(2))
    # initState = [int(n/2),int(n/2)+1]
    initState = [50,51]
    graph = nx.cycle_graph(n)
    staticQuantumWalk = QWAK(graph)
    staticQuantumWalk.runWalk(t, gamma, initState)

    global timeList,gammaList,initStateList,dynamicQuantumWalk
    timeList = [0,100]
    gammaList = [1/(2*np.sqrt(2))]
    initStateList = [[int(n/2),int(n/2)+1]]
    dynamicQuantumWalk = QWAK(graph)
    dynamicQuantumWalk.runWalk(timeList[0], gammaList[0], initStateList[0])

    @eel.expose
    def setTimeList(newTimeList):
        global timeList
        timeList = list(map(float,newTimeList.split(',')))

    @eel.expose
    def setGammaList(newGammaList):
        global gammaList
        gammaList = list(map(float,newGammaList.split(',')))

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
    def setGamma(newGamma):
        global gamma
        gamma = newGamma
        staticQuantumWalk.setGamma(newGamma)
    
    @eel.expose
    def getGamma():
        return staticQuantumWalk.getGamma()

    @eel.expose
    def runWalk():
        global staticQuantumWalk,n,t,gamma,initState
        # staticQuantumWalk.resetWalk()
        staticQuantumWalk.runWalk(t,gamma,initState)
        qwProbabilities = staticQuantumWalk.getProbDist()
        qwProbVec = qwProbabilities.getProbVec()
        probLists = qwProbVec.tolist()
        print(gamma)
        print(t)
        return probLists
    
    @eel.expose
    def runMultipleWalks():
        qwProbList = []
        global timeList,gammaList,initStateList,dynamicQuantumWalk
        dynamicQuantumWalk.resetWalk()
        timeRange = np.linspace(timeList[0],timeList[1],int(timeList[1]))
        for t in timeRange:
            dynamicQuantumWalk.runWalk(t, gammaList[0], initStateList[0])
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
        print(len(staticQuantumWalk.getAdjacencyMatrix()))
        staticQuantumWalk.runWalk(t, gamma, initState)


    eel.start('index.html', port=8080, cmdline_args=['--start-maximized'])

        
    pass
