from qwak.State import State
from qwak.Operator import Operator, StochasticOperator
from qwak.QuantumWalk import QuantumWalk, StochasticQuantumWalk
from qwak.ProbabilityDistribution import ProbabilityDistribution, StochasticProbabilityDistribution
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
marked = [n//2,n//2 + 1]
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

initState = State(n)
initState.buildState(marked)

sOperator = StochasticOperator(graph, noiseParam=0.0, sinkNode=None)
sOperator.buildStochasticOperator(0.0, 1)

sQuantumWalk = StochasticQuantumWalk(initState,sOperator)
sQuantumWalk.buildWalk(t)
new_state = sQuantumWalk.getFinalState().final_state

sProbDist = StochasticProbabilityDistribution(sQuantumWalk) 
sProbDist.buildProbDist()

plt.plot(qwProbDist.getProbVec(),label="Manual Quantum Walk")
plt.plot(new_state.diag(), label="Manual Stochastic Quantum Walk")
plt.plot(qwController.getProbDistVec(),label="QWAK Quantum Walk")

plt.legend()
plt.show()
