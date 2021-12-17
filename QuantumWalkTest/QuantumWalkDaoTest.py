import numpy as np

from QuantumWalkTest.StateTest import StateTest
from QuantumWalkTest.OperatorTest import OperatorTest
from QuantumWalkTest.QuantumWalkTest import QuantumWalkTest
from QuantumWalkTest.ProbabilityDistributionTest import ProbabilityDistributionTest


class QuantumWalkDaoTest:
    def __init__(self, n, graph, time=0, gamma=1, initStateList=0):
        self._initState = StateTest(n, initStateList)
        self._initState.timedBuildState()
        self._graph = graph
        self._operator = OperatorTest(self._graph, time, gamma)
        print("######### Diag Operator: USING ONLY MATMUL ##########\n")
        self._operator.timedBuildDiagonalOperator()
        print("#####################################################")
        print("######## Diag Operator: MULTIPLYING DIAGONAL ########\n")
        self._operator.timedBuildDiagonalOperator2()
        print("#####################################################\n")
        print("######## Diag Operator: Better EIGH #################\n")
        self._operator.timedBuildDiagonalOperator3()
        print("#####################################################\n")

        self._quantumWalk = QuantumWalkTest(self._initState, self._operator)
        self._quantumWalk.timedBuildWalk()
        self._probDist = ProbabilityDistributionTest(self._quantumWalk.getWalk())
        self._probDist.timedBuildProbDist()

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
