from QuantumWalk.QuantumWalkDao import QuantumWalkDao
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

if __name__ == '__main__':
    n = 100
    t = 30
    gamma = 1/(2*np.sqrt(2))
    initState = [int(n/2),int(n/2)+1]
    graph = nx.cycle_graph(n)
    staticQuantumWalk = QuantumWalkDao(graph)
    staticQuantumWalk.runWalk(t, gamma, initState)

    global timeList,gammaList,initStateList,dynamicQuantumWalk
    timeList = [0,100]
    gammaList = [1/(2*np.sqrt(2))]
    initStateList = [[int(n/2),int(n/2)+1]]
    dynamicQuantumWalk = QuantumWalkDao(graph)
    dynamicQuantumWalk.runWalk(timeList[0], gammaList[0], initStateList[0])

    @eel.expose
    def setTimeList(newTimeList):
        global timeList
        print(timeList)
        timeList = list(map(float,newTimeList.split(',')))
        print(timeList)

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
        initStateList = list(map(int,initStateStr.split(',')))
        newState = State(staticQuantumWalk.getDim())
        newState.buildState(initStateList)
        staticQuantumWalk.setInitState(newState)

    @eel.expose
    def getInitState():
        return staticQuantumWalk.getInitState()
        
    @eel.expose
    def setDim(newDim,graphStr):
        staticQuantumWalk.setDim(newDim, graphStr)

    @eel.expose
    def getDim():
        return staticQuantumWalk.getDim()
        
    @eel.expose
    def setGraph(newGraph):
        newGraph = eval(newGraph + f"({staticQuantumWalk.getDim()})")
        staticQuantumWalk.setGraph(newGraph)

    @eel.expose
    def getGraph():
        return staticQuantumWalk.getGraph()

    @eel.expose
    def setTime(newTime):
        staticQuantumWalk.setTime(newTime)
    
    @eel.expose
    def getTime():
        return staticQuantumWalk.getTime()

    @eel.expose
    def setGamma(newGamma):
        staticQuantumWalk.setGamma(newGamma)
    
    @eel.expose
    def getGamma():
        return staticQuantumWalk.getGamma()

    @eel.expose
    def runWalk():
        staticQuantumWalk.buildWalk()
        qwProbabilities = staticQuantumWalk.getProbDist()
        qwProbVec = qwProbabilities.getProbVec()
        probLists = qwProbVec.tolist()
        return probLists
    
    @eel.expose
    def runMultipleWalks():
        qwProbList = []
        global timeList,gammaList,initStateList,dynamicQuantumWalk
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

    eel.start('index.html', port=8080, cmdline_args=['--start-maximized'])

        
    pass
