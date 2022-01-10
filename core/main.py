import networkx as nx
import numpy as np
from matplotlib import pyplot as plt
import timeit

from QuantumWalk.State import State
from QuantumWalk.Operator import Operator
from QuantumWalk.QuantumWalk import QuantumWalk
from QuantumWalk.ProbabilityDistribution import ProbabilityDistribution
from QuantumWalk.QuantumWalkDao import QuantumWalkDao

if __name__ == '__main__':
    n = 102
    t = 50
    gamma = 1 / (2 * np.sqrt(2))
    graph = nx.cycle_graph(n)
    G = nx.Graph()



    for i in range(0,50):
        G.add_edge(f"{i}",f"{i+1}",weight=2)

    G.add_edge("50","51", weight=2)
    G.add_edge("50","a", weight=2)
    G.add_edge("50","b", weight=2)
    G.add_edge("50","c", weight=2)

    for i in range(51, 100):
        G.add_edge(f"{i}", f"{i + 1}", weight=2)

    G.add_edge("100", "0", weight=2)


    marked = [int(n / 2)]
    print(nx.adjacency_matrix(G))
    graph=G

    qwController = QuantumWalkDao(graph,True)
    qwController.runWalk(30, gamma, [50,51])

    qwProbabilities = qwController.getProbDist()

    qwProbVec = qwProbabilities.getProbVec()
    m = 0
    std = 0
    pos = np.arange(0,len(qwProbVec))
    for x in range(len(qwProbVec)):
        m += pos[x] * qwProbVec[x]

    for x in range(len(qwProbVec)):
        std += qwProbVec[x] * (pos[x] - m)**2
    print(std)

    plt.plot(qwProbVec)
    plt.show()



    # print(qwProbabilities.mean())
    # print(m)
    # print(qwProbabilities.std())


    # plt.plot(qwProbabilities)
    # plt.show()
    # print("Amplitudes: \n %s \n Probability:\n %s \n Mean: \n\t%s"%(qwAmplitudes,qwProbabilities,np.mean(qwProbabilities)))
    # searchedState = 2
    # print("Amplitude of state %s \n\t %s"%(searchedState,qwController.getStateAmplitude(searchedState)))
    # print("Probability of state %s \n\t %s"%(searchedState,qwController.getStateProbability(searchedState)))
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
