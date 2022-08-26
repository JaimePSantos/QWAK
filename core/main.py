import networkx as nx
from matplotlib import pyplot as plt
import numpy as np

from qwak.GraphicalQWAK import GraphicalQWAK

if __name__ == "__main__":

    staticN = 100
    dynamicN = staticN
    t = 12
    initState = [staticN // 2, (staticN // 2) + 1]
    graph = nx.cycle_graph(staticN)
    timeList = [0, t]
    initStateList = [[staticN // 2, (staticN // 2) + 1]]

    gQwak = GraphicalQWAK(
        staticN,
        dynamicN,
        graph,
        graph,
        initState,
        initStateList,
        t,
        timeList)

    # print(gQwak.runMultipleWalks()[1])
    # gQwak.runWalk()
    gQwak.runMultipleWalks()
    print(gQwak.getDynamicStDev())
