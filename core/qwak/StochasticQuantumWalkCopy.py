from __future__ import annotations

import numpy as np
from qutip import Qobj, Options, mesolve
from qwak.StochasticOperator import StochasticOperator
from qwak.State import State


class StochasticQuantumWalk(object):

    def __init__(
            self,
            state: State,
            operator: StochasticOperator) -> None:
        """This object is initialized with a user inputted initial state and
        operator.
        The dimension of the quantum walk will then be loaded from the initial
        state.
        The final state will contain the amplitudes of the time evolution of
        the initial state, as a function of the operator. This variable is initialized
        as an instance of QObj class.

        Parameters
        ----------
        state : State
            Initial state which will be the basis of the time dependant evolution.
        operator : StochasticOperator
            Operator which will evolve the initial state.
        """
        self._n = state.getDim()
        self._initState = state
        self._initQutipState = Qobj(state.getStateVec())
        self._operator = operator
        self._finalState = Qobj(State(self._n).getStateVec())
        self._time = 0

    def buildWalk(
        self,
        time: float,
        observables: list = [],
        opts: Options = Options(store_states=True, store_final_state=True)
    ) -> None:
        """Constructs the quantum walk over a specified time frame.

        Parameters
        ----------
        time : float
            The time over which the walk is to be simulated.
        observables : list, optional
            A list of observables to monitor during the walk. Defaults to an empty list.
        opts : Options, optional
            QuTiP options for the simulation. Defaults to storing states and the final state.
        """
        print("\t\t\tBefore calling self._time")
        self._time = np.arange(0, time + 1)
        print("\t\t\tAfter calling self._time")
        if self._operator.getSinkNode() is not None:
            print("\t\t\tBefore calling Qobj")
            self._initQutipState = Qobj(
                np.vstack([self._initState.getStateVec(), [0.0]])
            )
            print("\t\t\tAfter calling Qobj")
        print("\t\t\tBefore calling mesolve")
        print("\t\t\t\tType of self._operator.getQuantumHamiltonian():", type(self._operator.getQuantumHamiltonian()))
        print("\t\t\t\tType of self._initQutipState:", type(self._initQutipState))
        print("\t\t\t\tType of self._time:", type(self._time))
        print("\t\t\t\tType of self._operator.getClassicalHamiltonian():", type(self._operator.getClassicalHamiltonian()))
        print("\t\t\t\tType of observables:", type(observables))
        print("\t\t\t\tType of opts:", type(opts))
        print(f"\t\t\t\tself._operator.getQuantumHamiltonian() hermitian:{self._operator.getQuantumHamiltonian().isherm}")
        # print("Classical Hamiltonian contents:", self._operator.getClassicalHamiltonian())
        print("\t\t\tBefore calling mesolve")
        collapse_ops = self._operator.getClassicalHamiltonian()
        # If all classical Hamiltonians are zero, set collapse_ops to None
        if collapse_ops and all((op.full() == 0).all() for op in collapse_ops):
            print("\t\t\tAll collapse operators are zero. Setting collapse_ops to None.")
            collapse_ops = None

        # Debugging print to confirm final collapse operators before calling mesolve
        # print("\t\t\tFinal collapse operators:", collapse_ops)
        # print(f"self._time size: {self._time.shape}, values: {self._time[:10]} ... {self._time[-10:]}")
        # print("Quantum Hamiltonian matrix:\n", self._operator.getQuantumHamiltonian().full())
        # print("Initial Qutip State (self._initQutipState):\n", self._initQutipState.full())
        # collapse_ops = self._operator.getClassicalHamiltonian()
        # print("Collapse operators count:", len(collapse_ops))
        # for i, c_op in enumerate(collapse_ops):
        #     print(f"Collapse Operator {i}:\n", c_op.full())  # Print full matrix for each collapse operator
        

        self._finalState = mesolve(
            self._operator.getQuantumHamiltonian(),
            self._initQutipState,
            self._time,
            collapse_ops,
            observables,
            options=opts,
        ).final_state.full()
        print("\t\t\tAfter calling mesolve")

    def getFinalState(self) -> Qobj:
        """Returns the final quantum state after the completion of the walk.

        Returns
        -------
        Qobj
            The final state of the quantum walk.
        """
        return self._finalState

    def setFinalState(self, newFinalState: Qobj) -> None:
        """Sets a new final state for the quantum walk.

        Parameters
        ----------
        newFinalState : Qobj
            The new final state to be set for the quantum walk.
        """
        self._finalState = newFinalState

    def getDim(self) -> int:
        """Returns the dimension of the quantum walk's state space.

        Returns
        -------
        int
            The dimension of the quantum walk.
        """
        return self._n
