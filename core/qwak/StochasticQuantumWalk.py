from __future__ import annotations

import numpy as np
from qutip import Qobj, Options, mesolve
from qwak.StochasticOperator import StochasticOperator
from qwak.State import State


class StochasticQuantumWalk(object):
    """_summary_"""

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
        self._finalState = Qobj(State(self._n))
        self._time = 0

    def buildWalk(
        self,
        time,
        observables=[],
        opts=Options(store_states=True, store_final_state=True),
    ) -> None:
        """_summary_

        Parameters
        ----------
        time : _type_
            _description_
        observables : list, optional
            _description_, by default []
        opts : _type_, optional
            _description_, by default Options(store_states=True, store_final_state=True)
        """
        # TODO: Can we move the time dependency to the StochasticOperator class?
        # TODO: Can we make the time evolution low cost?
        # TODO: Is there a way to obtain amplitudes?
        # TODO: The final state is a of the Qobj class. Find a way to
        # make it State class.
        self._time = np.arange(0, time + 1)
        if self._operator.getSinkNode() is not None:
            self._initQutipState = Qobj(
                np.vstack([self._initState.getStateVec(), [0.0]])
            )
        self._finalState = mesolve(
            self._operator.getQuantumHamiltonian(),
            self._initQutipState,
            self._time,
            self._operator.getClassicalHamiltonian(),
            observables,
            options=opts,
        ).final_state.full()
        # if you want the full list of states, keep option store_states=True and instead
        # of final_state.full() use states.full()

    def getFinalState(self) -> Qobj:
        """_summary_

        Returns
        -------
        Qobj
            _description_
        """
        return self._finalState

    def setFinalState(self, newFinalState) -> None:
        """_summary_

        Parameters
        ----------
        newFinalState : _type_
            _description_
        """
        self._finalState = newFinalState

    def getDim(self) -> int:
        """_summary_

        Returns
        -------
        int
            _description_
        """
        return self._n
