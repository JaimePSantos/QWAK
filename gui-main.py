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
    t = 1
    gamma = 1/(2*np.sqrt(2))
    initState = [int(n/2)]
    graph = nx.cycle_graph(n)
    qwController = QuantumWalkDao(graph)
    qwController.runWalk(t,gamma,initState)

    def defaultWalk(defaultN,defaultT,defaultGamma,defaultInitState,defaultGraph):
        n = defaultN
        t = defaultT
        gamma = defaultGamma
        initState = defaultInitState
        graph = eval(defaultGraph + "(%s)"%n)
        qwController = QuantumWalkDao(graph)
        qwController.runWalk(t,gamma,initState)

    @eel.expose
    def setTime(newTime):
        qwController.setTime(newTime)
    
    @eel.expose
    def getTime():
        return qwController.getTime()

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
            qwController.runWalk(t,gamma,marked)
            qwAmplitudes = qwController.getWalk()
            qwProbabilities = qwController.getProbDist()
            probLists = qwProbabilities.tolist()
            qwProbList.append(probLists)
        return qwProbList


    @eel.expose
    def graphToJson():
        graph = nx.complete_graph(5)
        myCytGraph = convert2cytoscapeJSON(graph)
        myCytGraph2 = nx.cytoscape_data(graph)
        return myCytGraph2


    @eel.expose
    def startWalk():
        defaultN = eel.getDim()
        defaultT = eel.getT()
        defaultGamma = eel.getGamma()
        defaultInitState = eel.getInitState()
        print(defaultInitState)
        graphStr = 'nx.cycle_graph'
        print(graphStr)
        graph = eval(graphStr + "(%s)"%defaultN)
        defaultWalk(defaultN,defaultT,defaultGamma,defaultInitState,graph)

    eel.start('index.html', port=8080, cmdline_args=['--start-maximized'])

        
    pass
