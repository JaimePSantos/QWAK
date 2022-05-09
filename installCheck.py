from qwak.State import State
from qwak.Operator import Operator, StochasticOperator
from qwak.QuantumWalk import QuantumWalk, StochasticQuantumWalk
from qwak.ProbabilityDistribution import (
    ProbabilityDistribution,
    StochasticProbabilityDistribution,
)
from qwak.qwak import QWAK, StochasticQWAK

from sqwalk import SQWalker

from qutip import ket2dm, basis, Options, Qobj

import time

import networkx as nx
import numpy as np
from matplotlib import pyplot as plt
import sympy as sp
from sympy.abc import pi
from math import sqrt, ceil, pow

n = 100 
t = 12 
graph = nx.cycle_graph(n)
marked = [n // 2, n // 2 + 1]
#marked = [n//2]
customMarked = [(n // 2, 1 / np.sqrt(2)), (n // 2 + 1, 1 / np.sqrt(2))]
#customMarked = [(n // 2, 1)]

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
qwController.runWalk(t, marked)
print(
    f"Mean: {qwController.getProbDist().mean()}\t "
    f"Moment 1: {qwController.getProbDist().moment(1)}\n"
    f"Moment 2: {qwController.getProbDist().moment(2)}\n"
    f"Stdev: {qwController.getProbDist().stDev()}\n"
    f"Survival Probability: {qwController.getProbDist().survivalProb(marked[0],marked[0]+1)}\n"
    f"Inverse Part. Ratio: {qwController.getWalk().invPartRatio()}\n"
)

qwController2 = QWAK(graph, laplacian=False)
qwController2.runWalk(t, customStateList=customMarked)
print(
    f"Mean: {qwController2.getProbDist().mean()}\t "
    f"Moment 1: {qwController2.getProbDist().moment(1)}\n"
    f"Moment 2: {qwController2.getProbDist().moment(2)}\n"
    f"Stdev: {qwController2.getProbDist().stDev()}\n"
    f"Survival Probability: {qwController2.getProbDist().survivalProb(marked[0],marked[0]+1)}\n"
    f"Inverse Part. Ratio: {qwController2.getWalk().invPartRatio()}\n"
)

initState = State(n)
initState.buildState(marked)

noiseParam = 0. 
sinkNode = None 
sinkRate = 1.0

sOperator = StochasticOperator(graph, noiseParam=noiseParam, sinkNode=sinkNode, sinkRate=sinkRate)
sOperator.buildStochasticOperator()
sQuantumWalk = StochasticQuantumWalk(initState, sOperator)
sQuantumWalk.buildWalk(t)
new_state = sQuantumWalk.getFinalState().final_state
sProbDist = StochasticProbabilityDistribution(sQuantumWalk)
sProbDist.buildProbDist()

sqwController = StochasticQWAK(graph)
sqwController.runWalk(t, marked, noiseParam=noiseParam,sinkNode=sinkNode, sinkRate=sinkRate)

adj = nx.adj_matrix(graph).todense()
walker = SQWalker(np.array(adj), noise_param=noiseParam, sink_node=sinkNode,sink_rate = sinkRate)

plt.plot(new_state.diag(), label="Manual Stochastic Quantum Walk")
plt.plot(sqwController.getProbVec(), label="StochasticQWAK Quantum Walk")
plt.plot(qwProbDist.getProbVec(), label="Manual Quantum Walk")
plt.plot(qwController.getProbDistVec(), label="QWAK Quantum Walk")
plt.plot(qwController2.getProbDistVec(), label="QWAK Custom State Quantum Walk")
plt.legend()
plt.show()

### NOISY QUANTUM WALK ###

noiseParam = 0.15 
sinkNode = 10
sinkRate = 1.0

n = 100 
t = 12 
graph = nx.cycle_graph(n)
marked = [n//2]

initState = State(n)
initState.buildState(marked)

sOperator = StochasticOperator(graph, noiseParam=noiseParam, sinkNode=sinkNode, sinkRate=sinkRate)
sOperator.buildStochasticOperator()
sQuantumWalk = StochasticQuantumWalk(initState, sOperator)
sQuantumWalk.buildWalk(t)
new_state = sQuantumWalk.getFinalState().final_state
sProbDist = StochasticProbabilityDistribution(sQuantumWalk)
sProbDist.buildProbDist()

sqwController = StochasticQWAK(graph)
sqwController.runWalk(t, marked, noiseParam=noiseParam,sinkNode=sinkNode, sinkRate=sinkRate)

adj = nx.adj_matrix(graph).todense()
walker = SQWalker(np.array(adj), noise_param=noiseParam, sink_node=sinkNode,sink_rate = sinkRate)
opts = Options(store_states=False, store_final_state=True)
result = walker.run_walker(marked[0], time_samples=t,dt = 1 ,opts=opts)
new_state2 = result.final_state

plt.plot(new_state.diag(), label="Manual Stochastic Quantum Walk")
plt.plot(sqwController.getProbVec(), label="StochasticQWAK Quantum Walk")
plt.plot(new_state2.diag(), label="SQWALK Quantum Walk")
plt.legend()
plt.show()
