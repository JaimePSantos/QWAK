from qwak.State import State
from qwak.Operator import Operator
from qwak.QuantumWalk import QuantumWalk
from qwak.ProbabilityDistribution import ProbabilityDistribution
from core.qwak.qwak import QWAK


import networkx as nx
import numpy as np
from matplotlib import pyplot as plt
import timeit
import sympy as sp
from sympy.abc import pi
from math import sqrt, ceil, pow


if __name__ == '__main__':

    import cProfile, pstats
    n = 1000
    t = 10
    graph = nx.cycle_graph(n)
    marked = [50]

    qwController = QWAK(graph, laplacian=False,benchmark=True)

    #
    # profiler = cProfile.Profile()
    # profiler.enable()
    qwController.runWalk(t, marked)
    # profiler.disable()

    # stats = pstats.Stats(profiler).sort_stats('tottime')
    # stats.print_stats()