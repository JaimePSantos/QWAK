import networkx as nx
import numpy as np
from matplotlib import pyplot as plt

from QuantumWalk.State import State
from QuantumWalk.Operator import Operator
from QuantumWalk.QuantumWalk import QuantumWalk
from QuantumWalk.ProbabilityDistribution import ProbabilityDistribution

if __name__ == '__main__':
    n = 200
    t=120
    gamma=1/(2*np.sqrt(2))
    marked = [int(n/2)]
    initState = State(n,marked)
    initState.buildState()
    # print(initState.getState())

    graph2 = nx.cycle_graph(n)

    op = Operator(graph2,n,t,gamma)
    print(op.getAdjacencyMatrix())
    op.buildOperator()
    print(op.getOperator())

    walk = QuantumWalk(initState,op)
    walk.buildWalk()
    # print("Walk 1 \n%s\n"%(walk.getWalk().getStateVec()))
    # print("Walk 1 Prob \n%s\n"%walk.toProbability())
    print("Walk 1 \n%s\n"%(walk.getWalk()))

    probDist = ProbabilityDistribution(walk.getWalk())
    probDist.buildProbDist()
    # print("Prob Dist 1 \n%s\n"%probDist.getProbDist())
    std = np.std(probDist.getProbDist())
    print("Prob 1 time: \n\t%s\nProb Dist 1 std \n\t%s\n Sqrt of time\n\t%s\n"%(t,std,0.54*t))

    plt.plot(probDist.getProbDist())
    # plt.show()