import networkx as nx
from matplotlib import pyplot as plt
import numpy as np

from qwak.GraphicalQWAK import GraphicalQWAK
from qwak.qwak import QWAK
from qwak.State import State
from qwak.Operator import Operator

if __name__ == "__main__":

    state = State(4, [0, 1, 2, 3])
    state.buildState()
    json_str = state.to_json()
    # print(json_str)

    state2 = State.from_json(json_str)
    # print(state2.getStateVec())
    state2.buildState(customStateList=[(0,-1)])
    # print(state2.getStateVec())

    graph = nx.cycle_graph(4)
    operator = Operator(graph,0.1)
    operator.buildDiagonalOperator()
    print(operator.getOperator())

    # Serialize the operator to JSON
    json_str = operator.to_json()
    print(json_str)

    # Deserialize the JSON string back into an instance of the Operator class
    deserialized_operator = Operator.from_json(json_str)
    print(deserialized_operator.getOperator())
    deserialized_operator.buildDiagonalOperator(1)
    print(deserialized_operator.getOperator())