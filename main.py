import networkx as nx
from matplotlib import pyplot as plt
import numpy as np

from qwak.GraphicalQWAK import GraphicalQWAK
from qwak.qwak import QWAK

if __name__ == "__main__":

    staticN = 200
    dynamicN = staticN
    t = 12
    initState = [staticN // 2, (staticN // 2) + 1]
    graph = nx.cycle_graph(staticN)
    timeList = [0, t]
    initStateList = [[staticN // 2, (staticN // 2) + 1]]
    nx.draw(graph)
    plt.show()
    # qwak = QWAK(graph,initState)
    # qwak.setDim(150,graphStr='nx.cycle_graph',initStateList=initState)
    # qwak.runWalk(t)
    # plt.plot(qwak.getProbVec())
    # plt.show()
    #
    # gQwak = GraphicalQWAK(
    #     staticN,
    #     dynamicN,
    #     graph,
    #     graph,
    #     initState,
    #     initStateList,
    #     t,
    #     timeList)

    # gQwak.runMultipleWalks()
    # gQwak.runWalk()
    # print(gQwak.getStaticInversePartRatio())
    # print(gQwak.getDynamicInvPartRatio())
