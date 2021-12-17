import networkx as nx
import numpy as np
from matplotlib import pyplot as plt
import timeit

from QuantumWalkTest.StateTest import StateTest
from QuantumWalkTest.OperatorTest import OperatorTest
from QuantumWalkTest.QuantumWalkTest import QuantumWalkTest
from QuantumWalkTest.ProbabilityDistributionTest import ProbabilityDistributionTest
from QuantumWalkTest.QuantumWalkDaoTest import QuantumWalkDaoTest

if __name__ == '__main__':
    n = 1000
    print(n)
    t= 600
    gamma=1/(2*np.sqrt(2))
    marked = [int(n/2)]

    qwController = QuantumWalkDaoTest(n,nx.cycle_graph(n),t,gamma,marked)
    print("Version: np.Eig @ D @ np.EigH\n")
    print("\tFull run time: %ss"%round(qwController.fullExecutionTime,5))
    print("\t\t--> Eigh time:   %ss"%round(qwController.eighExecutionTime,5))
    print("\t\t--> Diag time:   %ss"%round(qwController.diagExecutionTime,5))
    print("\t\t--> MatMul time: %ss\n"%round(qwController.matMulExecutionTime,2))
    print("Version: (np.Eig * D.toList) @ np.EigH\n")
    print("\tFull run time: %ss"%round(qwController.fullExecutionTime2,5))
    print("\t\t--> Eigh time: %ss"%round(qwController.eighExecutionTime2,5))
    print("\t\t--> Diag time: %ss"%round(qwController.diagExecutionTime2,5))
    print("\t\t--> MatMul time: %ss\n"%round(qwController.matMulExecutionTime2,5))
    print("Version: (ln.Eig * D.toList) @ ln.EigH\n")
    print("\tFull run time: %ss"%round(qwController.fullExecutionTime3,5))
    print("\t\t--> Eigh time: %ss"%round(qwController.eighExecutionTime3,5))
    print("\t\t--> Diag time: %ss"%round(qwController.diagExecutionTime3,5))
    print("\t\t--> MatMul time: %ss\n"%round(qwController.matMulExecutionTime3,5))

    samples = 20
    eighTimeList = []
    eighTimeList2 = []
    eighTimeList3 = []

    matMulTimeList = []
    matMulTimeList2 = []
    matMulTimeList3 = []

    for i in range(samples):
        print("\n--------- Trial #%s -------------------\n"%i)
        qwCont = QuantumWalkDaoTest(n,nx.cycle_graph(n),t,gamma,marked)
        eighTimeList.append(qwCont.eighExecutionTime)
        eighTimeList2.append(qwCont.eighExecutionTime2)
        eighTimeList3.append(qwCont.eighExecutionTime3)
        matMulTimeList.append(qwCont.matMulExecutionTime)
        matMulTimeList2.append(qwCont.matMulExecutionTime2)
        matMulTimeList3.append(qwCont.matMulExecutionTime3)

    k=1
    for eigh in [eighTimeList,eighTimeList2,eighTimeList3]:
        plt.plot(eigh,label='%s'%k)
        k+=1
        plt.legend()

    # k=1
    # for eigh in [matMulTimeList,matMulTimeList2,matMulTimeList3]:
    #     plt.plot(eigh,label='%s'%k)
    #     k+=1
    #     plt.legend()


    ax = plt.gca()
    ax.set_ylim([-0.1, 0.4])
    plt.show()

