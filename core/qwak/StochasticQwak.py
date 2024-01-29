import networkx as nx
import numpy as np
from qutip import Options

from qwak.Errors import StateOutOfBounds, NonUnitaryState
from qwak.State import State
from qwak.StochasticOperator import StochasticOperator
from qwak.StochasticProbabilityDistribution import StochasticProbabilityDistribution
from qwak.StochasticQuantumWalk import StochasticQuantumWalk


class StochasticQWAK:
    """_summary_"""

    def __init__(
        self,
        graph: nx.Graph,
        initStateList=None,
        customStateList=None,
        noiseParam=None,
        sinkNode=None,
        sinkRate=None,
    ) -> None:
        """_summary_

        Parameters
        ----------
        graph : nx.Graph
            _description_
        initStateList : _type_, optional
            _description_, by default None
        customStateList : _type_, optional
            _description_, by default None
        noiseParam : _type_, optional
            _description_, by default None
        sinkNode : _type_, optional
            _description_, by default None
        sinkRate : _type_, optional
            _description_, by default None
        """
        self._graph = graph
        self._n = len(self._graph)
        self._operator = StochasticOperator(
            self._graph,
            noiseParam=noiseParam,
            sinkNode=sinkNode,
            sinkRate=sinkRate,
        )
        self._initState = State(
            self._n,
            nodeList=initStateList,
            customStateList=customStateList)
        self._quantumWalk = StochasticQuantumWalk(
            self._initState, self._operator)
        self._probDist = StochasticProbabilityDistribution(
            self._quantumWalk)

    def runWalk(
        self,
        time: float = 0,
        initStateList: list = None,
        customStateList=None,
        noiseParam=None,
        sinkNode=None,
        sinkRate=None,
        observables=[],
        opts=Options(store_states=True, store_final_state=True),
    ) -> None:
        """_summary_

        Parameters
        ----------
        time : float, optional
            _description_, by default 0
        initStateList : list, optional
            _description_, by default None
        customStateList : _type_, optional
            _description_, by default None
        noiseParam : _type_, optional
            _description_, by default None
        sinkNode : _type_, optional
            _description_, by default None
        sinkRate : _type_, optional
            _description_, by default None
        observables : list, optional
            _description_, by default []
        opts : _type_, optional
            _description_, by default Options(store_states=True, store_final_state=True)

        Raises
        ------
        stOBErr
            _description_
        nUErr
            _description_
        """
        try:
            self._initState.buildState(
                nodeList=initStateList, customStateList=customStateList
            )
        except StateOutOfBounds as stOBErr:
            raise stOBErr
        except NonUnitaryState as nUErr:
            raise nUErr
        self._operator.buildStochasticOperator(
            noiseParam=noiseParam, sinkNode=sinkNode, sinkRate=sinkRate
        )
        self._quantumWalk = StochasticQuantumWalk(
            self._initState, self._operator)
        self._quantumWalk.buildWalk(time, observables, opts)
        self._probDist = StochasticProbabilityDistribution(
            self._quantumWalk)
        self._probDist.buildProbDist()

    def setProbDist(self, newProbDist: object) -> None:
        """_summary_

        Parameters
        ----------
        newProbDist : object
            _description_
        """
        self._probDist = newProbDist

    def getProbDist(self) -> StochasticProbabilityDistribution:
        """_summary_

        Returns
        -------
        ProbabilityDistribution
            _description_
        """
        return self._probDist

    def getProbVec(self) -> np.ndarray:
        """_summary_

        Returns
        -------
        ProbabilityDistribution
            _description_
        """
        return self._probDist.getProbVec()

    def getQuantumHamiltonian(self):
        """_summary_

        Returns
        -------
        _type_
            _description_
        """
        return self._operator.getQuantumHamiltonian()

    def getClassicalHamiltonian(self):
        """_summary_

        Returns
        -------
        _type_
            _description_
        """
        return self._operator.getClassicalHamiltonian()

    def getLaplacian(self):
        """_summary_

        Returns
        -------
        _type_
            _description_
        """
        return self._operator.getLaplacian()
