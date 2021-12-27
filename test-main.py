import networkx as nx
import numpy as np
from matplotlib import pyplot as plt
import timeit

from QuantumWalkTest.StateTest import StateTest
from QuantumWalkTest.OperatorTest import OperatorTest
from QuantumWalkTest.QuantumWalkTest import QuantumWalkTest
from QuantumWalkTest.ProbabilityDistributionTest import ProbabilityDistributionTest
from QuantumWalkTest.QuantumWalkDaoTest import QuantumWalkDaoTest


def getAvgTime(timeList):
    te = 0
    te2 = 0
    te3 = 0
    tm = 0
    tm2 = 0
    tm3 = 0
    tf = 0
    tf2 = 0
    tf3 = 0
    for i in range(0, len(timeList), 9):
        if(i + 9 > len(timeList)):
            break
        te += timeList[i]
        te2 += timeList[i+1]
        te3 += timeList[i+2]
        tm += timeList[i+3]
        tm2 += timeList[i+4]
        tm3 += timeList[i+5]
        tf += timeList[i+6]
        tf2 += timeList[i+7]
        tf3 += timeList[i+8]

    return [te/(len(timeList)/9), te2/(len(timeList)/9), te3/(len(timeList)/9), 
            tm/(len(timeList)/9), tm2/(len(timeList)/9), tm3/(len(timeList)/9), 
            tf/(len(timeList)/9), tf2/(len(timeList)/9), tf3/(len(timeList)/9)]


def createTimeList(samples, n, graph, t, gamma, marked):
    timeList = []
    for i in range(samples):
        print("\n--------- Trial #%s -------------------\n" % i)
        qwCont = QuantumWalkDaoTest(n, graph, t, gamma, marked)
        timeList.extend([qwCont.eighExecutionTime, qwCont.eighExecutionTime2, qwCont.eighExecutionTime3,
                        qwCont.matMulExecutionTime, qwCont.matMulExecutionTime2, qwCont.matMulExecutionTime3,
                        qwCont.fullExecutionTime, qwCont.fullExecutionTime2, qwCont.fullExecutionTime3])
    return timeList


if __name__ == '__main__':
    n = 1000
    print(n)
    t = int(n/2)
    gamma = 1/(2*np.sqrt(2))
    marked = [int(n/2)]
    graph = nx.cycle_graph(n)

    # qwCont = QuantumWalkDaoTest(n, graph, t, gamma, marked,'2')
    # qwContProb = qwCont.getProbDist()
    # qwContOpt = QuantumWalkDaoTest(n, graph, t, gamma, marked,version='opt')
    # qwContOpt.optRunWalk(t,gamma)
    # qwContOptProb = qwContOpt.getProbDist()
    # print(qwContOptProb == qwContProb)

    time = range(0,100)
    markedList = [marked,[marked[0],marked[0]+1],[marked[0],marked[0]-1,marked[0]+1]]
    
    qwContTime = 0
    print(marked)
    for t in time:
        qwCont = QuantumWalkDaoTest(graph, t, gamma, [0],version='2')
        qwContTime += qwCont.daoExecutionTime

    qwContOptTime = 0
    qwContOpt = QuantumWalkDaoTest(graph, t, gamma, marked,version='opt')
    for t in time:
        qwContOpt.optRunWalk(t,gamma,marked)
        qwContOptTime += qwContOpt.daoExecutionTime
    
    print("Time - Old dao: %s "%qwContTime)
    print("Time - New dao: %s "%qwContOptTime)

    qwContTime = 0
    for marked1 in markedList:
        qwCont = QuantumWalkDaoTest(graph, t, gamma, marked1,version='2')
        qwContTime += qwCont.daoExecutionTime

    qwContOptTime = 0
    qwContOpt = QuantumWalkDaoTest(graph, t, gamma, marked1,version='opt')
    for marked1 in markedList:
        qwContOpt.optRunWalk(t,gamma,marked1)
        qwContOptTime += qwContOpt.daoExecutionTime
    
    print("InitList - Old dao: %s "%qwContTime)
    print("InitList - New dao: %s "%qwContOptTime)

    # graph = nx.complete_graph(n)

    # samples = 1
    # timeList = createTimeList(samples, n, graph, t, gamma, marked)
    # avgTimeList = getAvgTime(timeList)

    # print("Avg eigh: %ss\nAvg eigh2: %ss\nAvg eigh3: %s\n\t for N = %s and %s samples." % (
    #     avgTimeList[0], avgTimeList[1], avgTimeList[2], n, samples))
    # print("\n> Eigh3 is %s times faster than Eigh2&1" %
    #       (avgTimeList[0]/avgTimeList[2]))
    # print("\nAvg MatMult: %ss\nAvg MatMult2: %ss\nAvg MatMult3: %s\n\t for N = %s and %s samples." % (
    #     avgTimeList[3], avgTimeList[4], avgTimeList[5], n, samples))
    # print("\n> MatMult2 is %s times faster than MatMult\n" %
    #       (avgTimeList[3]/avgTimeList[4]))

    # print("Avg full: %ss\nAvg full2: %ss\nAvg full3: %s\n\t for N = %s and %s samples." % (
    #     avgTimeList[6], avgTimeList[7], avgTimeList[8], n, samples))
    # print("\n> Full2 is %s times faster than Full" %
    #       (avgTimeList[6]/avgTimeList[7]))
    # print("\n> Full3 is %s times faster than Full2" %
    #       (avgTimeList[7]/avgTimeList[8]))

    # nList = range(2,1000)
    # multTimeList = []
    # for n in nList:
    #     tList = createTimeList(10, n, nx.cycle_graph(n), t, gamma, [int(n/2)])
    #     avgTList = getAvgTime(tList)
    #     multTimeList.append(avgTList[7])
    
    # f = open("2-1000_10Samples_Test","w")
    # f.write(str(multTimeList))
    # f.close()

    #plt.plot(multTimeList)
    #plt.show()
        # k=1
        # for eigh in [eighTimeList,eighTimeList2,eighTimeList3]:
        #     plt.plot(eigh,label='%s'%k)
        #     k+=1
        #     plt.legend()

        # k=1
        # for eigh in [matMulTimeList,matMulTimeList2,matMulTimeList3]:
        #     plt.plot(eigh,label='%s'%k)
        #     k+=1
        #     plt.legend()

        # ax = plt.gca()
        # ax.set_ylim([-0.1, 0.4])
        # plt.show()
