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


if __name__ == '__main__':
    n = 100
    t = 30
    gamma = 1/(2*np.sqrt(2))
    initState = [int(n/2),int(n/2)+1]
    graph = nx.cycle_graph(n)
    qwController = QuantumWalkDao(graph)
    qwController.runWalk(t,gamma,initState)

    global timeList
    timeList = [0,100]
    gammaList = [gamma]
    initStateList = [initState]

    @eel.expose
    def setTimeList(newTimeList):
        global timeList
        print(timeList)
        timeList = list(map(int,newTimeList.split(',')))
        print(timeList)

    @eel.expose
    def setInitState(initStateStr):
        initStateList = list(map(int,initStateStr.split(',')))
        newState = State(qwController.getDim())
        newState.buildState(initStateList)
        qwController.setInitState(newState)

    @eel.expose
    def getInitState():
        return qwController.getInitState()
        
    @eel.expose
    def setDim(newDim,graphStr):
        qwController.setDim(newDim,graphStr)

    @eel.expose
    def getDim():
        return qwController.getDim()
        
    @eel.expose
    def setGraph(newGraph):
        newGraph = eval(newGraph + f"({qwController.getDim()})")
        qwController.setGraph(newGraph)

    @eel.expose
    def getGraph():
        return qwController.getGraph()

    @eel.expose
    def setTime(newTime):
        qwController.setTime(newTime)
    
    @eel.expose
    def getTime():
        return qwController.getTime()

    @eel.expose
    def setGamma(newGamma):
        qwController.setGamma(newGamma)
    
    @eel.expose
    def getGamma():
        return qwController.getGamma()

    @eel.expose
    def runWalk():
        qwController.buildWalk()
        qwProbabilities = qwController.getProbDist()
        probLists = qwProbabilities.tolist()
        return probLists
    
    @eel.expose
    def runMultipleWalks():
        qwProbList = []
        global timeList
        print(qwController.getDim())
        for t in range(timeList[0],timeList[1]):
            qwController.runWalk(t,gamma,initState)
            qwProbabilities = qwController.getProbDist()
            probLists = qwProbabilities.tolist()
            qwProbList.append(probLists)
        return qwProbList

    @eel.expose
    def graphToJson():
        graph = qwController.getGraph()
        myCytGraph = nx.cytoscape_data(graph)
        return myCytGraph

    eel.start('index.html', port=8080, cmdline_args=['--start-maximized'])

        
    pass
