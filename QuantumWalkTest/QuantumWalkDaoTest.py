import numpy as np

from QuantumWalkTest.StateTest import StateTest
from QuantumWalkTest.OperatorTest import OperatorTest
from QuantumWalkTest.QuantumWalkTest import QuantumWalkTest
from QuantumWalkTest.ProbabilityDistributionTest import ProbabilityDistributionTest

import timeit


class QuantumWalkDaoTest:
    def __init__(self, n, graph, time=0, gamma=1, initStateList=0,version=None):
        startTimeDao = timeit.default_timer()

        self._initState = StateTest(n, initStateList)
        self._initState.timedBuildState()
        
        self._graph = graph

        if version is None:
            self._operator = OperatorTest(self._graph, time, gamma)
            print("######### Running: np.Eig @ D @ np.EigH ###################\n")
            self._operator.timedBuildDiagonalOperator()
            print("######### Completed: np.Eig @ D @ np.EigH ###################\n")
            print("######### Running: (np.Eig * D.toList) @ np.EigH ############\n")
            self._operator.timedBuildDiagonalOperator2()
            print("######### Completed: (np.Eig * D.toList) @ np.EigH ##########\n")
            print("######### Running: (ln.Eig * D.toList) @ ln.EigH ############\n")
            self._operator.timedBuildDiagonalOperator3()
            print("######### Completed: (ln.Eig * D.toList) @ ln.EigH ##########\n")
        elif version == '1':
            self._operator = OperatorTest(self._graph, time, gamma)
            print("######### Running: np.Eig @ D @ np.EigH #####################\n")
            self._operator.timedBuildDiagonalOperator()
            print("######### Completed: np.Eig @ D @ np.EigH ###################\n")
        elif version == '2':
            self._operator = OperatorTest(self._graph, time, gamma)
            print("######### Running: (np.Eig * D.toList) @ np.EigH ############\n")
            self._operator.timedBuildDiagonalOperator2()
            print("######### Completed: (np.Eig * D.toList) @ np.EigH ##########\n")
        elif version == '3':
            self._operator = OperatorTest(self._graph, time, gamma)
            print("######### Running: (ln.Eig * D.toList) @ ln.EigH #############\n")
            self._operator.timedBuildDiagonalOperator3()
            print("######### Completed: (ln.Eig * D.toList) @ ln.EigH ###########\n")
        elif version == 'opt':
            self._operator = OperatorTest(self._graph, mode='opt')

        else:
            print("Invalid version.")
            return

        self._quantumWalk = QuantumWalkTest(self._initState, self._operator)
        self._quantumWalk.timedBuildWalk()

        self._probDist = ProbabilityDistributionTest(self._quantumWalk.getWalk())
        self._probDist.timedBuildProbDist()
        endTimeDao = timeit.default_timer()

        self.initStateExecutionTime = self._initState.stateExecutionTime

        self.eighExecutionTime = self._operator.eighExecutionTime
        self.eighExecutionTime2 = self._operator.eighExecutionTime2
        self.eighExecutionTime3 = self._operator.eighExecutionTime3

        self.diagExecutionTime = self._operator.diagExecutionTime
        self.diagExecutionTime2 = self._operator.diagExecutionTime2
        self.diagExecutionTime3 = self._operator.diagExecutionTime3

        self.matMulExecutionTime = self._operator.matMulExecutionTime
        self.matMulExecutionTime2 = self._operator.matMulExecutionTime2
        self.matMulExecutionTime3 = self._operator.matMulExecutionTime3

        self.fullExecutionTime = self._operator.fullExecutionTime
        self.fullExecutionTime2 = self._operator.fullExecutionTime2
        self.fullExecutionTime3 = self._operator.fullExecutionTime3

        self.walkExecutionTime = self._quantumWalk.walkExecutionTime

        self.probDistExecutionTime = self._probDist.probDistExecutionTime

        self.daoExecutionTime = endTimeDao - startTimeDao
    
    def optRunWalk(self,time,gamma):
        print("######### Running Optimized: (np.Eig * D.toList) @ np.EigH ##########\n")
        self._operator.timedBuildDiagonalOperator4(time,gamma)
        print("######### Completed Optimized: (ln.Eig * D.toList) @ ln.EigH ########\n")

    def timedRunWalk(self):
        self._initState.timedBuildState()
        self._operator.timedBuildDiagonalOperator()
        self._quantumWalk.timedBuildWalk()
        self._probDist.timedBuildProbDist()

    def setInitState(self, newInitState):
        self._initState.setState(newInitState)

    def getInitState(self):
        return self._initState

    def setOperator(self, newOperator):
        self._operator.setOperator(newOperator)

    def getOperator(self):
        return self._operator

    def setWalk(self, newWalk):
        self._quantumWalk.setWalk(newWalk)

    def getWalk(self):
        return self._quantumWalk.getWalk()

    def setProbDist(self, probDist):
        self._probDist = probDist

    def getProbDist(self):
        return self._probDist.getProbDist()

    def getStateAmplitude(self, state):
        return self._quantumWalk.getStateAmplitude(state)

    def getStateProbability(self, state):
        return self._probDist.getStateProbability(state)
