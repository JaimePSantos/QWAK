import networkx as nx
import numpy as np
from qutip import Options, Qobj

from qwak.Errors import StateOutOfBounds, NonUnitaryState
from qwak.State import State
from qwak.StochasticOperator import StochasticOperator
from qwak.StochasticProbabilityDistribution import StochasticProbabilityDistribution
from qwak.StochasticQuantumWalk import StochasticQuantumWalk


class StochasticQWAK:

    def __init__(
        self,
        graph: nx.Graph,
        initStateList: list = None,
        customStateList: list = None,
        noiseParam: float = None,
        sinkNode: int = None,
        sinkRate: float = None,
    ) -> None:
        """  This class integrates the components of a stochastic quantum walk including
        the graph, initial state, stochastic operator, quantum walk dynamics, and
        probability distribution.
        Initializes a StochasticQWAK instance with a graph and optional parameters.

        Parameters
        ----------
        graph : nx.Graph
            The graph over which the quantum walk is performed.
        initStateList : list, optional
            List of nodes to initialize the quantum state.
        customStateList : list, optional
            Custom states for the quantum walk.
        noiseParam : float, optional
            Parameter controlling noise in the stochastic operator.
        sinkNode : int, optional
            Node acting as a sink in the quantum walk.
        sinkRate : float, optional
            Rate of transfer to the sink node.
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
        customStateList: list = None,
        noiseParam: float = None,
        sinkNode: int = None,
        sinkRate: float = None,
        observables: list = [],
        opts: Options = Options(
            store_states=True,
            store_final_state=True),
    ) -> None:
        """Executes the stochastic quantum walk.

        Parameters
        ----------
        time : float, optional
            Duration of the quantum walk.
        initStateList : list, optional
            Initial state list for the quantum walk.
        customStateList : list, optional
            Custom state list for the quantum walk.
        noiseParam : float, optional
            Noise parameter for the operator.
        sinkNode : int, optional
            Sink node index in the graph.
        sinkRate : float, optional
            Rate of transfer to the sink node.
        observables : list, optional
            List of observables to monitor during the walk.
        opts : Options, optional
            QuTiP options for the simulation.
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

    def setProbDist(
            self,
            newProbDist: StochasticProbabilityDistribution) -> None:
        """Sets a new probability distribution for the quantum walk.

        Parameters
        ----------
        newProbDist : StochasticProbabilityDistribution
            The new probability distribution to set.
        """
        self._probDist = newProbDist

    def getProbDist(self) -> StochasticProbabilityDistribution:
        """Returns the current probability distribution of the quantum walk.

        Returns
        -------
        StochasticProbabilityDistribution
            The current probability distribution.
        """
        return self._probDist

    def getProbVec(self) -> np.ndarray:
        """Returns the probability vector of the current quantum state.

        Returns
        -------
        np.ndarray
            The probability vector.
        """
        return self._probDist.getProbVec()

    def getQuantumHamiltonian(self) -> Qobj:
        """Retrieves the quantum Hamiltonian of the stochastic operator.

        Returns
        -------
        Qobj
            The quantum Hamiltonian governing the evolution of the quantum walk.
        """
        return self._operator.getQuantumHamiltonian()

    def getClassicalHamiltonian(self) -> list[Qobj]:
        """Retrieves the classical Hamiltonian (Lindblad operators) of the stochastic operator.

        Returns
        -------
        list[Qobj]
            A list of Lindblad operators representing the classical component of the quantum walk.
        """
        return self._operator.getClassicalHamiltonian()

    def getLaplacian(self) -> np.ndarray:
        """Retrieves the Laplacian matrix of the graph associated with the stochastic operator.

        Returns
        -------
        np.ndarray
            The Laplacian matrix of the graph.
        """
        return self._operator.getLaplacian()
