from qwak import *
import networkx as nx
import numpy as np
from matplotlib import pyplot as plt
import timeit
import sympy as sp
from sympy.abc import pi
from math import sqrt, ceil, pow

n = 100
t = 10
graph = nx.cycle_graph(n)
marked = [50]

qwInitState = State.State(n,marked)
qwInitState.buildState()
qwOperator = operator.Operator(graph=graph)
qwOperator.buildDiagonalOperator(t)
qwFinalState = QuantumWalk.QuantumWalk(qwInitState,qwOperator)
qwFinalState.buildWalk()
qwProbDist = ProbabilityDistribution.ProbabilityDistribution(qwFinalState.getWalk())
qwProbDist.buildProbDist()
print(f"Init State: \n {qwInitState}\n\n"
      f"Operator: \n {qwOperator}\n\n"
      f"Final State: \n {qwFinalState}\n\n"
      f"Prob Dist: \n {qwProbDist}\n\n")



qwController = qwak.QWAK(graph, laplacian=False)
qwController.runWalk(t, marked)
print(f"Mean: {qwController.getProbDist().mean()}\t "
      f"Moment 1: {qwController.getProbDist().moment(1)}\n"
      f"Moment 2: {qwController.getProbDist().moment(2)}\n"
      f"Stdev: {qwController.getProbDist().stDev()}\n"
      f"Survival Probability: {qwController.getProbDist().survivalProb(marked[0],marked[0]+1)}\n"
      f"Inverse Part. Ratio: {qwController.getWalk().invPartRatio()}\n")
      # f"PST {qwController.checkPST(0,2)}")

plt.plot(qwController.getProbDist().getProbVec())
plt.show()