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
    print("\t np.Eig @ D @ np.EigH")
    print("\t\tFull run time: %s"%round(qwController.fullExecutionTime,3))
    print("\t\t--> Eigh time: %s"%round(qwController.eighExecutionTime,3))
    print("\t\t--> Diag time: %s"%round(qwController.diagExecutionTime,3))
    print("\t\t--> MatMul time: %s"%round(qwController.matMulExecutionTime,2))
    print("\t (np.Eig * D.toList) @ np.EigH")
    print("\t\tFull run time: %s"%round(qwController.fullExecutionTime2,3))
    print("\t\t--> Eigh time: %s"%round(qwController.eighExecutionTime2,3))
    print("\t\t--> Diag time: %s"%round(qwController.diagExecutionTime2,3))
    print("\t\t--> MatMul time: %s"%round(qwController.matMulExecutionTime2,3))
    print("\t(ln.Eig * D.toList) @ ln.EigH")
    print("\t\tFull run time: %s"%round(qwController.fullExecutionTime3,3))
    print("\t\t--> Eigh time: %s"%round(qwController.eighExecutionTime2,3))
    print("\t\t--> Diag time: %s"%round(qwController.diagExecutionTime2,3))
    print("\t\t--> MatMul time: %s"%round(qwController.matMulExecutionTime2,3))
    # qwAmplitudes = qwController.getWalk()
    # qwProbabilities = qwController.getProbDist()
    # plt.plot(qwProbabilities)
    # plt.show()
    # searchedState = 2
