from qwak.State import State
from qwak.Operator import Operator, StochasticOperator
from qwak.QuantumWalk import QuantumWalk, StochasticQuantumWalk
from qwak.ProbabilityDistribution import ProbabilityDistribution
from qwak.qwak import QWAK

import networkx as nx
import numpy as np
from matplotlib import pyplot as plt
import timeit
import sympy as sp
from sympy.abc import pi
from math import sqrt, ceil, pow

n = 100
t = 12
graph = nx.cycle_graph(n)
marked = [n//2]
customMarked = [(50,1)]

qwInitState = State(n,marked)
qwInitState.buildState(marked)
qwOperator = Operator(graph=graph)
qwOperator.buildDiagonalOperator(t)
qwFinalState = QuantumWalk(qwInitState,qwOperator)
qwFinalState.buildWalk()
qwProbDist = ProbabilityDistribution(qwFinalState.getFinalState())
qwProbDist.buildProbDist()
print(f"Init State: \n {qwInitState}\n\n"
      f"Operator: \n {qwOperator}\n\n"
      f"Final State: \n {qwFinalState}\n\n"
      f"Prob Dist: \n {qwProbDist}\n\n")

qwController = QWAK(graph, laplacian=False)
qwController.runWalk(t, marked)
print(f"Mean: {qwController.getProbDist().mean()}\t "
      f"Moment 1: {qwController.getProbDist().moment(1)}\n"
      f"Moment 2: {qwController.getProbDist().moment(2)}\n"
      f"Stdev: {qwController.getProbDist().stDev()}\n"
      f"Survival Probability: {qwController.getProbDist().survivalProb(marked[0],marked[0]+1)}\n"
      f"Inverse Part. Ratio: {qwController.getWalk().invPartRatio()}\n")
      # f"PST {qwController.checkPST(0,2)}")

qwController2 = QWAK(graph, laplacian=False)
qwController2.runWalk(t, marked)
print(f"Mean: {qwController2.getProbDist().mean()}\t "
      f"Moment 1: {qwController2.getProbDist().moment(1)}\n"
      f"Moment 2: {qwController2.getProbDist().moment(2)}\n"
      f"Stdev: {qwController2.getProbDist().stDev()}\n"
      f"Survival Probability: {qwController2.getProbDist().survivalProb(marked[0],marked[0]+1)}\n"
      f"Inverse Part. Ratio: {qwController2.getWalk().invPartRatio()}\n"
      f"Init State = {qwController2.getInitState()}")

n = 100
time = 12
initial_node = n // 2

initState = State(n,[n//2])
initState.buildState()

sOperator = StochasticOperator(nx.cycle_graph(n), noiseParam=0.0, sinkNode=None)
sOperator.buildStochasticOperator(0.0, 1)

sQuantumWalk = StochasticQuantumWalk(initState,sOperator)
sQuantumWalk.buildWalk(time)
new_state = sQuantumWalk.getFinalState().final_state

plt.plot(new_state.diag(), label="Stochastic Quantum Walk")

plt.plot(qwController.getProbDistVec(),label="Manual Quantum Walk")

plt.plot(qwController2.getProbDistVec(),label="QWAK Quantum Walk")
plt.legend()
plt.show()

