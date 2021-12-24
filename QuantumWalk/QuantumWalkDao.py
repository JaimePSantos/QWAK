import numpy as np

from QuantumWalk.State import State
from QuantumWalk.Operator import Operator
from QuantumWalk.QuantumWalk import QuantumWalk
from QuantumWalk.ProbabilityDistribution import ProbabilityDistribution


class QuantumWalkDao:
    def __init__(self,graph):
        self._graph = graph
        self._operator = Operator(self._graph)
        self._n = len(self._graph)
        self._time = 0
        self._gamma = 1
        self._initStateList = [0]

    def runWalk(self,time=0,gamma=1,initStateList=[0]):
        self._time = time
        self._gamma = gamma
        self._initStateList = initStateList
        self._initState = State(self._n, initStateList)
        self._initState.buildState()
        self._operator.buildDiagonalOperator(self._time,self._gamma)
        self._quantumWalk = QuantumWalk(self._initState, self._operator)
        self._quantumWalk.buildWalk()
        self._probDist = ProbabilityDistribution(self._quantumWalk.getWalk())
        self._probDist.buildProbDist()
    
    def buildWalk(self):
        self._initState = State(self._n, self._initStateList)
        self._initState.buildState()
        self._operator.buildDiagonalOperator(self._time,self._gamma)
        self._quantumWalk = QuantumWalk(self._initState, self._operator)
        self._quantumWalk.buildWalk()
        self._probDist = ProbabilityDistribution(self._quantumWalk.getWalk())
        self._probDist.buildProbDist()
        
    def setInitState(self, newInitState):
        self._initState.setState(newInitState)

    def getInitState(self):
        return self._initState
    
    def setTime(self, newTime):
        self._time = newTime

    def getTime(self):
        return self._time

    def setGamma(self, newGamma):
        self._gamma = newGamma

    def getGamma(self):
        return self._gamma

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
