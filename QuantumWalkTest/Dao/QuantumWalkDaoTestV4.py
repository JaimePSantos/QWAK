import numpy as np

from QuantumWalkTest.StateTest import StateTest
from QuantumWalkTest.OperatorTest import OperatorTest
from QuantumWalkTest.QuantumWalkTest import QuantumWalkTest
from QuantumWalkTest.ProbabilityDistributionTest import ProbabilityDistributionTest

from QuantumWalkTest.Operator.OperatorTestV4 import OperatorTestV4
import timeit


class QuantumWalkDaoTestV4:
    def __init__(self, graph, time=0, gamma=1, initStateList=[0],version=None):
        self._graph = graph
        self._n = len(self._graph)
        
        self._operator = OperatorTestV4(self._graph)
        self.resetTimes()
        self.eighExecutionTime = self._operator.eighExecutionTime
    
    def resetTimes(self):
        self.initStateExecutionTime = 0
        self.eighExecutionTime = 0
        self.diagExecutionTime = 0
        self.matMulExecutionTime = 0
        self.fullExecutionTime = 0
        self.walkExecutionTime = 0
        self.probDistExecutionTime = 0 
    
    def initTimes(self):
        self.initStateExecutionTime = self._initState.stateExecutionTime
        
        self.diagExecutionTime = self._operator.diagExecutionTime
        self.matMulExecutionTime = self._operator.matMulExecutionTime
        self.fullExecutionTime = self._operator.fullExecutionTime
        self.walkExecutionTime = self._quantumWalk.walkExecutionTime
        self.probDistExecutionTime = self._probDist.probDistExecutionTime

    def optRunWalk(self,time,gamma,initStateList):
        print("######### Running Optimized: np.Eig * [D] @ np.EigH ##########\n")
        self._operator.timedBuildDiagonalOperator(time,gamma)
        print("######### Completed Optimized: ln.Eig * [D] @ ln.EigH ########\n")

        self._initState = StateTest(self._n, initStateList)
        self._initState.timedBuildState()
        
        self._quantumWalk = QuantumWalkTest(self._initState, self._operator)
        self._quantumWalk.timedBuildWalk()

        self._probDist = ProbabilityDistributionTest(self._quantumWalk.getWalk())
        self._probDist.timedBuildProbDist()

        self.initTimes()
        self.daoExecutionTime =  self.initStateExecutionTime + self.eighExecutionTime + self.diagExecutionTime + self.matMulExecutionTime + self.walkExecutionTime + self.probDistExecutionTime
        self.eighExecutionTime = 0 # So eigh execution time is only added once.

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
