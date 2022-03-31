import networkx as nx
import numpy as np
from matplotlib import pyplot as plt
import timeit
import sympy as sp
from sympy.abc import pi
from math import sqrt, ceil, pow
from qwak.qwak import QWAK
from qwak.Operator import Operator
from scipy.linalg import expm, schur
from sympy import Matrix

if __name__ == '__main__':
    n = 7
    t = 5
    graph = nx.cycle_graph(n)
    # graph=nx.complete_graph(n)
    # graph = nx.complete_bipartite_graph(4,3)
    # marked = range(int(n/2))
    marked = [3]
    print(list(marked))
    qwController = QWAK(graph)
    qwController.runWalk(t,marked)
    print(qwController.getAmpVec())
    print(qwController.getProbDistVec())
    plt.plot(qwController.getProbDistVec())
    plt.show()
    # qwController = QWAK(graph, laplacian=True,markedSearch=[(0,-1j)])
    # qwController.runWalk(t,marked)
    # plt.plot(qwController.getProbDist().getProbVec())
    # plt.show()
    # sp.pprint(f"PST {qwController.checkPST(0,2)}")
    eta = []
    times = np.linspace(0,50,200)
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