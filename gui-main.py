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
eel.init('GraphicalInterface')


if __name__ == '__main__':
    n = 100
    t = 30
    gamma = 1/(2*np.sqrt(2))
    initState = [int(n/2),int(n/2)+1]
    graph = nx.cycle_graph(n)
    qwController = QuantumWalkDao(graph)
    qwController.runWalk(t,gamma,initState)


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
        newGraph = eval(newGraph + "(%s)"%qwController.getDim())
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
    def runMultipleWalks(time=[0],):
        qwController = QuantumWalkDao(graph)
        qwProbList = []
        for t in time:
            qwController.runWalk(t,gamma,initState)
            qwAmplitudes = qwController.getWalk()
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
