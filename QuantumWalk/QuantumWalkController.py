import numpy as np

from QuantumWalk.State import State
from QuantumWalk.Operator import Operator
from QuantumWalk.QuantumWalk import QuantumWalk
from QuantumWalk.ProbabilityDistribution import ProbabilityDistribution

class QuantumWalkController:
    def __init__(self,n,graph,time=0,gamma=1,initStateList=0):
        self._initState = State(n,initStateList)
        self._initState.timedBuildState()
        self._graph = graph
        self._operator = Operator(self._graph,time,gamma)
        self._operator.timedBuildDiagonalOperator()
        self._quantumWalk = QuantumWalk(self._initState,self._operator)
        self._quantumWalk.timedBuildWalk()
        self._probDist = ProbabilityDistribution(self._quantumWalk.getWalk())
        self._probDist.timedBuildProbDist()

    def timedRunWalk(self):
        self._initState.timedBuildState()
        self._operator.timedBuildDiagonalOperator()
        self._quantumWalk.timedBuildWalk()
        self._probDist.timedBuildProbDist()

    def setInitState(self,newInitState):
        self._initState.setState(newInitState)

    def getInitState(self):
        return self._initState

    def setOperator(self,newOperator):
        self._operator.setOperator(newOperator)

    def getOperator(self):
        return self._operator

    def setWalk(self,newWalk):
        self._quantumWalk.setWalk(newWalk)

    def getWalk(self):
        return self._quantumWalk.getWalk()

    def setProbDist(self,probDist):
        self._probDist = probDist

    def getProbDist(self):
        return self._probDist.getProbDist()

