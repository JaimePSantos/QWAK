import networkx as nx
import numpy as np
from qutip import Options,Qobj

from qwak.Errors import StateOutOfBounds, NonUnitaryState
from qwak.State import State
from qwak.StochasticOperator import StochasticOperator
from qwak.StochasticProbabilityDistribution import StochasticProbabilityDistribution
from qwak.StochasticQuantumWalk import StochasticQuantumWalk

n = 100
t = 1
noiseParam = 0.1
sinkNode = 99
sinkRate = 1.0
graph = nx.cycle_graph(n)
initStateList = [n // 2]
operator = StochasticOperator(
    graph,
    noiseParam=noiseParam,
    sinkNode=sinkNode,
    sinkRate=sinkRate,
)
initState = State(
    n,
    nodeList=initStateList,
    customStateList=None)
quantumWalk = StochasticQuantumWalk(
    initState, operator)
probDist = StochasticProbabilityDistribution(quantumWalk)

operator.buildStochasticOperator(
            noiseParam = noiseParam,
            sinkNode= sinkNode,
            sinkRate = sinkRate)
print(operator.getClassicalHamiltonian())

quantumWalk.buildWalk(t)
