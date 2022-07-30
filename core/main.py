import networkx as nx
import numpy as np
from matplotlib import pyplot as plt

from qwak.qwak import QWAK
from qwak.State import State
from GraphicalQWAK import GraphicalQWAK 

if __name__ == "__main__":
    n = 100
    t = 10
    initState = [51]
    graph = nx.cycle_graph(n)
    timeList = [0, 100]
    initStateList = [[int(n / 2), int(n / 2) + 1]]
    gQwak = GraphicalQWAK(n,graph,initState,initStateList,t,timeList)
    gQwak.setStaticTime(str(t))
    gQwak.runWalk()
    # print(gQwak.runMultipleWalks())
    # print(gQwak.getStaticMean())
    gQwak.runMultipleWalks()
    gQwak.getDynamicStDev()
    gQwak.runMultipleWalks()
    gQwak.getDynamicStDev()

#    t = 40
#    n = 200
#    graph = nx.circular_ladder_graph(n)
#    customInitState = [(n // 2,1/np.sqrt(2)),(n // 2 + 1,1/np.sqrt(2))]
#    qwController = QWAK(graph,customStateList=customInitState)
#    qwController.runWalk(t)
#    font = {'family': 'sans-serif',
#            'size': 12}
#    plt.rc('font', **font)
#    plt.plot(qwController.getProbVec(), linewidth=1.0, color='blue')
#    plt.ylabel("Probability")
#    plt.xlabel("Graph Node")
#    plt.show()

    # st = State(10,customStateList= [(1,5),(2,6)])
    # st = State(9,nodeList=[9])
    # st.buildState(nodeList = [1])
    # print(st.getStateVec())
    # n = 100
    # t = 6
    # marked = list(range(n))
    # print(marked)
    # graph = nx.cycle_graph(n)
    # # graph=nx.complete_graph(n)
    # # graph = nx.complete_bipartite_graph(4,3)
    # # marked = range(int(n/2))
    # marked = [3]
    # print(list(marked))
    # qwController = QWAK(graph)
    # qwController.runWalk(t, marked)
    # print(qwController.getAmpVec())
    # print(qwController.getProbDistVec())
    # plt.plot(qwController.getProbDistVec())
    # plt.show()
    # qwController = QWAK(graph, laplacian=True, markedSearch=[(n // 4, -1)])
    # qwController.runWalk(t, marked)
    # plt.plot(qwController.getProbVec())
    # plt.show()
    # sp.pprint(f"PST {qwController.checkPST(0,2)}")
    # eta = []
    # times = np.linspace(0, 50, 200)
    # print(f"init: {qwController.getInitState()}")

    # for time in times:
    #     print()
    #     print(f"time = {time}")
    #     print()
    #     qwController.runWalk(time, marked)
    #     print(f"init cond: {qwController.getInitState()}\n")
    #     print(f"adjm: {qwController.getAdjacencyMatrix()}")
    #     tef = qwController.getTransportEfficiency()
    #     # print(f"Controller time: {qwController.getOperator().getTime()}")
    #     # print(f"init: {qwController.getInitState()}")
    #     # print(f"finalState: {qwController.getAmpVec()}")
    #     eta.append(tef)
    #     print()
    #     print("###################################################################################################")
    #     print()

    # print(f"calculo: {1/((1-(4/7))*7)}")
    # print(f"eta: {eta[-1]}")
    # plt.plot(eta)
    # plt.show()

    # qwOperator = Operator(graph=graph)
    # qwOperator.buildDiagonalOperator(1)
    # print(qwOperator.getAdjacencyMatrix())
    # print(f"{qwOperator}\n")
    # qwOperator.setAdjacencyMatrix(nx.adjacency_matrix(nx.complete_graph(n)).todense())
    # print(qwOperator.getAdjacencyMatrix())
    # qwOperator.buildDiagonalOperator(1)
    # print(qwOperator)

    # print(f"Mean: {qwController.getProbDist().mean()}\t "
    #       f"Moment 1: {qwController.getProbDist().moment(1)}\n"
    #       f"Moment 2: {qwController.getProbDist().moment(2)}\n"
    #       f"Stdev: {qwController.getProbDist().stDev()}\n"
    #       f"Survival Probability: {qwController.getProbDist().survivalProb(0,0)}\n"
    #       f"Inverse Part. Ratio: {qwController.getWalk().invPartRatio()}\n")
    #       f"PST {qwController.checkPST(0,2)}")

    # G = nx.Graph()
    # for i in range(0,100):
    #     G.add_edge(f"{i}",f"{i+1}",weight=2)
    #     # print(f" {i} ---- {i+1}")
    # G.add_edge("100","101", weight=2)
    # G.add_edge("100","a", weight=2)
    # G.add_edge("100","b", weight=2)
    # G.add_edge("100","c", weight=2)
    # for i in range(101, 199):
    #     G.add_edge(f"{i}", f"{i + 1}", weight=2)
    #     # print(f" {i} ---- {i+1}")
    # G.add_edge("199", "0", weight=2)
    #
    # # print(nx.adjacency_matrix(G))
    #
    # # graph=G
    # qwController = QWAK(graph, laplacian=True)
    # qwController.runWalk(t, gamma, [100])
    #
    # qwProbabilities = qwController.getProbDist()
    # qwProbVec = qwProbabilities.getProbVec()
    #
    # m = 0
    # std = 0
    # pos = np.arange(0,len(qwProbVec))
    # for x in range(len(qwProbVec)):
    #     m += pos[x] * qwProbVec[x]
    #
    # for x in range(len(qwProbVec)):
    #     std += (qwProbVec[x] * (pos[x] - m)**2)/(t**2)
    #
    # # print(G)
    # print(qwProbabilities.mean())
    # print(qwProbabilities.stdev())
    # # print(std)
    # nx.draw(G)
    # plt.show()
    # plt.plot(qwProbVec)
    # plt.show()

    # print(qwProbabilities.mean())
    # print(m)
    # print(qwProbabilities.std())
