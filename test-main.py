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
    n = 5000
    print(n)
    t= 600
    gamma=1/(2*np.sqrt(2))
    marked = [int(n/2)]

    qwController = QuantumWalkDaoTest(n,nx.cycle_graph(n),t,gamma,marked)
    qwAmplitudes = qwController.getWalk()
    qwProbabilities = qwController.getProbDist()
    plt.plot(qwProbabilities)
    plt.show()
    searchedState = 2