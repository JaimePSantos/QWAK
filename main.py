import networkx as nx
import numpy as np
from matplotlib import pyplot as plt
import timeit

from QuantumWalk.State import State
from QuantumWalk.Operator import Operator
from QuantumWalk.QuantumWalk import QuantumWalk
from QuantumWalk.ProbabilityDistribution import ProbabilityDistribution
from QuantumWalk.QuantumWalkController import QuantumWalkController

if __name__ == '__main__':
    n = 10
    t=3
    gamma=1/(2*np.sqrt(2))
    marked = [int(n/2)]

    qwController = QuantumWalkController(n,nx.cycle_graph(n),t,gamma,marked)
    qwAmplitudes = qwController.getWalk()
    # print(qwAmplitudes)
    # initState = State(n,marked)
    # initState.buildState()
    # # print(initState.getState())
    # print("N=%s\tTime=%s\tGamma=%s\t"%(n,t,round(gamma,2)))
    #
    # startTimeGraph = timeit.default_timer()
    # graph2 = nx.cycle_graph(n)
    # endTimeGraph = timeit.default_timer()
    # executionTimeGraph = (endTimeGraph - startTimeGraph)
    # print("\tGraph took %s seconds." % executionTimeGraph)
    #
    # op = Operator(graph2,t,gamma)
    # # print(op.getAdjacencyMatrix())
    # startTimeExpm = timeit.default_timer()
    # op.buildOperator()
    # endTimeExpm = timeit.default_timer()
    # executionTimeExpm = (endTimeExpm - startTimeExpm)
    # print("\tNormal operator took %s seconds. (linalg.expm)" % executionTimeExpm)
    # # print(op.getOperator())
    #
    # walk = QuantumWalk(initState,op)
    # startTimeWalk = timeit.default_timer()
    # walk.buildWalk()
    # endTimeWalk = timeit.default_timer()
    # executionTimeWalk = (endTimeWalk - startTimeWalk)
    # print("\tWalk took %s seconds." % executionTimeWalk)
    # # print("Walk 1 \n%s\n"%(walk.getWalk().getStateVec()))
    # # print("Walk 1 Prob \n%s\n"%walk.toProbability())
    # # print("Walk 1 \n%s\n"%(walk.getWalk()))
    #
    # probDist = ProbabilityDistribution(walk.getWalk())
    # startTimeProbDist = timeit.default_timer()
    # probDist.buildProbDist()
    # endTimeProbDist = timeit.default_timer()
    # executionTimeProbDist = (endTimeProbDist - startTimeWalk)
    # print("\tProbDist took %s seconds." % executionTimeProbDist)
    # # print("Prob Dist 1 \n%s\n"%probDist.getProbDist())
    # std = np.std(probDist.getProbDist())
    # # print("Prob 1 time: \n\t%s\nProb Dist 1 std \n\t%s\n Sqrt of time\n\t%s\n"%(t,std,0.54*t))
    #
    # startTimeDiag = timeit.default_timer()
    # op.buildDiagonalOperator()
    # endTimeDiag = timeit.default_timer()
    # executionTimeDiag = (endTimeDiag - startTimeDiag)
    # print("\tDiagonal operator took %s seconds." % executionTimeDiag)
    # print("\tNormal / Diagonal = %s times faster" % (round(executionTimeExpm / executionTimeDiag, 2)))
    # walk.buildWalk()
    # probDist.buildProbDist()
    # plt.plot(probDist.getProbDist())
    # plt.show()