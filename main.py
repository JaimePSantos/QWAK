import networkx as nx
from matplotlib import pyplot as plt
import numpy as np

from qwak.GraphicalQWAK import GraphicalQWAK
from qwak.qwak import QWAK
from qwak.State import State
from qwak.Operator import Operator
from qwak.QuantumWalk import QuantumWalk

if __name__ == "__main__":

    state = State(4, [0, 1, 2, 3])
    state.buildState()
    st_json_str = state.to_json()
    # print(json_str)

    deserialized_state = State.from_json(st_json_str)
    # print(state2.getStateVec())
    deserialized_state.buildState(customStateList=[(0,-1)])
    # print(state2.getStateVec())

    graph = nx.cycle_graph(4)
    operator = Operator(graph,0.1)
    operator.buildDiagonalOperator()
    # print(operator.getOperator())

    # Serialize the operator to JSON
    op_json_str = operator.to_json()
    # print(op_json_str)

    # Deserialize the JSON string back into an instance of the Operator class
    deserialized_operator = Operator.from_json(op_json_str)
    # print(deserialized_operator.getOperator())
    deserialized_operator.buildDiagonalOperator(1)
    # print(deserialized_operator.getOperator())

    quantumWalk = QuantumWalk(state=deserialized_state,operator=deserialized_operator)
    # print(quantumWalk.getOperator())
    qw_json_str = quantumWalk.to_json()
    # print(qw_json_str)

    deserialized_walk = QuantumWalk.from_json(qw_json_str)
    # print(deserialized_walk.getFinalState())

    deserialized_walk.buildWalk()
    # print(deserialized_walk.getOperator())
    print(deserialized_walk.getFinalState())
    # print(quantumWalk.getInitState())