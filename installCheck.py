from qwak.State import State
from qwak.Operator import Operator, StochasticOperator
from qwak.QuantumWalk import QuantumWalk, StochasticQuantumWalk
from qwak.ProbabilityDistribution import (
    ProbabilityDistribution,
    StochasticProbabilityDistribution,
)
from qwak.qwak import QWAK, StochasticQWAK

import networkx as nx
import numpy as np
from matplotlib import pyplot as plt
import sympy as sp
from sympy.abc import pi
from math import sqrt, ceil, pow

n = 50
t = 20
graph = nx.cycle_graph(n)
#marked = [n // 2, n // 2 + 1]
marked = [n//2]
customMarked = [(n // 2, 1 / np.sqrt(2)), (n // 2 + 1, 1 / np.sqrt(2))]

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

sOperator = StochasticOperator(graph, noiseParam=0.0, sinkNode=None, sinkRate=1.0)
sOperator.buildStochasticOperator()
sQuantumWalk = StochasticQuantumWalk(initState, sOperator)
sQuantumWalk.buildWalk(t)
new_state = sQuantumWalk.getFinalState().final_state
sProbDist = StochasticProbabilityDistribution(sQuantumWalk)
sProbDist.buildProbDist()

sqwController = StochasticQWAK(graph)
sqwController.runWalk(t, marked, noiseParam=0.15,sinkNode=10, sinkRate=1.0)
vectest =[0.009038414469042867, 0.006972139844657781, 0.0070178799359853685, 0.006556649809073759, 0.008381895060784274, 0.006937028559886048, 0.005796162371444784, 0.006703778528682772, 0.005283728995651229, 0.004782745636500229, 0.0040100315539318395, 0.013317095878876575, 0.016548005514141022, 0.018413563412798564, 0.018664573508772358, 0.019012580481991802, 0.018731455778716672, 0.019319140823255213, 0.020283184340184713, 0.020689054330082918, 0.02211999245680057, 0.021893737073841568, 0.021280366013298396, 0.02134670420822615, 0.021566405295736755, 0.021695171453424075, 0.023458484101877397, 0.0219839290786894, 0.020937873743097725, 0.02076864454134528, 0.0213396295532552, 0.020885397431106352, 0.019971622140206542, 0.02007083117343069, 0.01919617731009013, 0.019673482854858117, 0.018483666832697872, 0.018027512083827555, 0.01908203108546183, 0.0175396177411556, 0.017018090996275513, 0.021014875832779226, 0.020091595301299222, 0.018486489717884882, 0.025165508381331837, 0.021821904286810963, 0.019279650058003812, 0.02057133779850671, 0.022235437490905754, 0.025597761950840077, 0.1409369631784746]
print(sqwController.getProbVec() == vectest) 


#plt.plot(new_state.diag(), label="Manual Stochastic Quantum Walk")
plt.plot(sqwController.getProbVec(), label="StochasticQWAK Quantum Walk")
#plt.plot(qwProbDist.getProbVec(), label="Manual Quantum Walk")
#plt.plot(qwController.getProbDistVec(), label="QWAK Quantum Walk")
#plt.plot(qwController2.getProbDistVec(), label="QWAK Custom State Quantum Walk")

plt.legend()
plt.show()
