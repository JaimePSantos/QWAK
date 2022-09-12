from qwak.State import State
from qwak.Operator import Operator
from qwak.StochasticOperator import StochasticOperator
from qwak.QuantumWalk import QuantumWalk
from qwak.StochasticQuantumWalk import StochasticQuantumWalk
from qwak.ProbabilityDistribution import ProbabilityDistribution
from qwak.StochasticProbabilityDistribution import StochasticProbabilityDistribution

from qwak.qwak import QWAK
from qwak.StochasticQwak import StochasticQWAK

from qutip import ket2dm, basis, Options, Qobj

import time

import inspect


import networkx as nx
import numpy as np
from matplotlib import pyplot as plt
import sympy as sp
from sympy.abc import pi
from math import sqrt, ceil, pow

n = 1000
t = 50
graph = nx.cycle_graph(n)
marked = [n // 2, n // 2 + 1]
customMarked = [(n // 2, 1 / np.sqrt(2)), (n // 2 + 1, 1 / np.sqrt(2))]
customMarked2 = [(n // 2, 1j * (1 / np.sqrt(2))),
                 (n // 2 + 1, (1 / np.sqrt(2)))]

qwInitState = State(n, marked)
qwInitState.buildState(marked)
qwOperator = Operator(graph=graph)
qwOperator.buildDiagonalOperator(t)
qwFinalState = QuantumWalk(qwInitState, qwOperator)
qwFinalState.buildWalk()
qwProbDist = ProbabilityDistribution(qwFinalState.getFinalState())
qwProbDist.buildProbDist()
print(
    f"Init State: \n {qwInitState}\n\n"
    f"Operator: \n {qwOperator}\n\n"
    f"Final State: \n {qwFinalState}\n\n"
    f"Prob Dist: \n {qwProbDist}\n\n"
)

qwController = QWAK(graph, laplacian=False)
qwController.runWalk(t + 50, marked)

print(
    f"Mean: {qwController.getProbDist().mean()}\t "
    f"Moment 1: {qwController.getProbDist().moment(1)}\n"
    f"Moment 2: {qwController.getProbDist().moment(2)}\n"
    f"Stdev: {qwController.getProbDist().stDev()}\n"
    f"Survival Probability: {qwController.getProbDist().survivalProb(marked[0],marked[0]+1)}\n"
    f"Inverse Part. Ratio: {qwController.getWalk().invPartRatio()}\n")


qwController2 = QWAK(graph, laplacian=False)
qwController2.runWalk(t + 100, customStateList=customMarked2)
print(
    f"Mean: {qwController2.getProbDist().mean()}\t "
    f"Moment 1: {qwController2.getProbDist().moment(1)}\n"
    f"Moment 2: {qwController2.getProbDist().moment(2)}\n"
    f"Stdev: {qwController2.getProbDist().stDev()}\n"
    f"Survival Probability: {qwController2.getProbDist().survivalProb(marked[0],marked[0]+1)}\n"
    f"Inverse Part. Ratio: {qwController2.getWalk().invPartRatio()}\n")

plt.plot(qwProbDist.getProbVec(), label="Manual Quantum Walk")
plt.plot(qwController.getProbVec(), label="QWAK Quantum Walk")
plt.plot(qwController2.getProbVec(), label="QWAK Custom State Quantum Walk")
plt.legend()

noiseParam = 0.0
sinkNode = None
sinkRate = 1.0

n = 50
t = 5
graph = nx.cycle_graph(n)
marked = [n // 2]

initState = State(n)
initState.buildState(marked)

sOperator = StochasticOperator(
    graph, noiseParam=noiseParam, sinkNode=sinkNode, sinkRate=sinkRate
)
sOperator.buildStochasticOperator()
sQuantumWalk = StochasticQuantumWalk(initState, sOperator)
sQuantumWalk.buildWalk(t)
sProbDist = StochasticProbabilityDistribution(sQuantumWalk)
sProbDist.buildProbDist()

sqwController = StochasticQWAK(graph)
sqwController.runWalk(
    t + 3, marked, noiseParam=noiseParam, sinkNode=sinkNode, sinkRate=sinkRate
)

## NOISY QUANTUM WALK ###

noiseParam = 0.15
sinkNode = 10
sinkRate = 1.0

n = 50
t = 20
graph = nx.cycle_graph(n)
marked = [n // 2]

initState = State(n)
initState.buildState(marked)

sOperator = StochasticOperator(
    graph, noiseParam=noiseParam, sinkNode=sinkNode, sinkRate=sinkRate
)
sOperator.buildStochasticOperator()
sQuantumWalk = StochasticQuantumWalk(initState, sOperator)
sQuantumWalk.buildWalk(
    t,
    opts=Options(
        store_states=False,
        store_final_state=True))
sProbDist2 = StochasticProbabilityDistribution(sQuantumWalk)
sProbDist2.buildProbDist()

sqwController2 = StochasticQWAK(graph)
sqwController2.runWalk(
    t - 3, marked, noiseParam=noiseParam, sinkNode=sinkNode, sinkRate=sinkRate
)

plt.figure()
plt.plot(sProbDist.getProbVec(), label="Manual Stochastic Quantum Walk")
plt.plot(sqwController.getProbVec(), label="StochasticQWAK Quantum Walk")
plt.plot(sProbDist2.getProbVec(), label="Manual Noisy Stochastic Quantum Walk")
plt.plot(sqwController2.getProbVec(),
         label="Noisy StochasticQWAK Quantum Walk")

plt.legend()
plt.show()