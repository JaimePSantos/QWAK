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
    initState = [int(n/2)]
    graph = nx.cycle_graph(n)
    qwController = QuantumWalkDao(graph)
    qwController.runWalk(t,gamma,initState)


    @eel.expose
    def setInitState(initStateStr):
        initStateList = list(map(int,initStateStr.split(',')))
        print(initStateList)
        newState = State(qwController.getDim(), initStateList)
        newState.buildState()
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

    def convert2cytoscapeJSON(G):
        # load all nodes into nodes array
        final = {}
        final["elements"] = []
        final["edges"] = []
        for node in G.nodes():
            nx = {}
            nx["data"] = {}
            nx["data"]["id"] = node
            nx["data"]["label"] = node
            final["elements"].append(nx.copy())
        # load all edges to edges array
        for edge in G.edges():
            nx = {}
            nx["data"] = {}
            myEdges = edge[0]+edge[1]
            nx["data"]["id"] = myEdges
            nx["data"]["source"] = str(edge[0])
            nx["data"]["target"] = str(edge[1])
            final["edges"].append(nx)
        return json.dumps(final)

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
