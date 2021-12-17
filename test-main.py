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
    totalTime = 0
    for t in timeList:
        totalTime += t
    return totalTime/len(timeList)


if __name__ == '__main__':
    # Weird behavior on windows: scipy.linalg is 10x slower up until exactly 960.
    n = 1000
    print(n)
    t = int(n/2)
    gamma = 1/(2*np.sqrt(2))
    marked = [int(n/2)]
    # graph = nx.cycle_graph(n)
    graph = nx.complete_graph(n)

    samples = 100
    eighTimeList = []
    eighTimeList2 = []
    eighTimeList3 = []

    matMulTimeList = []
    matMulTimeList2 = []
    matMulTimeList3 = []

    for i in range(samples):
        print("\n--------- Trial #%s -------------------\n" % i)
        qwCont = QuantumWalkDaoTest(n, graph , t, gamma, marked)
        eighTimeList.append(qwCont.eighExecutionTime)
        eighTimeList2.append(qwCont.eighExecutionTime2)
        eighTimeList3.append(qwCont.eighExecutionTime3)
        matMulTimeList.append(qwCont.matMulExecutionTime)
        matMulTimeList2.append(qwCont.matMulExecutionTime2)
        matMulTimeList3.append(qwCont.matMulExecutionTime3)

    avgTimeEigh = getAvgTime(eighTimeList)
    avgTimeEigh2 = getAvgTime(eighTimeList2)
    avgTimeEigh3 = getAvgTime(eighTimeList3)

    print("Avg eigh: %ss\nAvg eigh2: %ss\nAvg eigh3: %s\n\t for N = %s and %s samples." % (
        avgTimeEigh, avgTimeEigh2, avgTimeEigh3, n, samples))
    print(avgTimeEigh2)
    print(avgTimeEigh3)
    print("\n> Eigh3 is %s times faster than Eigh2&1" %
          (avgTimeEigh/avgTimeEigh3))

    avgTimeMatMult = getAvgTime(matMulTimeList)
    avgTimeMatMult2 = getAvgTime(matMulTimeList2)
    avgTimeMatMult3 = getAvgTime(matMulTimeList3)

    print("\nAvg MatMult: %ss\nAvg MatMult2: %ss\nAvg MatMult3: %s\n\t for N = %s and %s samples." % (
        avgTimeMatMult, avgTimeMatMult2, avgTimeMatMult3, n, samples))

    print("\n> MatMult2 is %s times faster than MatMult" %
          (avgTimeMatMult/avgTimeMatMult2))

    # qwController = QuantumWalkDaoTest(n, nx.cycle_graph(n), t, gamma, marked)
    # print("Version: np.Eig @ D @ np.EigH\n")
    # print("\tFull run time: %ss" % round(qwController.fullExecutionTime, 5))
    # print("\t\t--> Eigh time:   %ss" %
    #       round(qwController.eighExecutionTime, 5))
    # print("\t\t--> Diag time:   %ss" %
    #       round(qwController.diagExecutionTime, 5))
    # print("\t\t--> MatMul time: %ss\n" %
    #       round(qwController.matMulExecutionTime, 2))
    # print("Version: (np.Eig * D.toList) @ np.EigH\n")
    # print("\tFull run time: %ss" % round(qwController.fullExecutionTime2, 5))
    # print("\t\t--> Eigh time: %ss" % round(qwController.eighExecutionTime2, 5))
    # print("\t\t--> Diag time: %ss" % round(qwController.diagExecutionTime2, 5))
    # print("\t\t--> MatMul time: %ss\n" %
    #       round(qwController.matMulExecutionTime2, 5))
    # print("Version: (ln.Eig * D.toList) @ ln.EigH\n")
    # print("\tFull run time: %ss" % round(qwController.fullExecutionTime3, 5))
    # print("\t\t--> Eigh time: %ss" % round(qwController.eighExecutionTime3, 5))
    # print("\t\t--> Diag time: %ss" % round(qwController.diagExecutionTime3, 5))
    # print("\t\t--> MatMul time: %ss\n" %
    #       round(qwController.matMulExecutionTime3, 5))

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
