import networkx as nx
from matplotlib import pyplot as plt
import numpy as np

from qwak.GraphicalQWAK import GraphicalQWAK
from qwak.qwak import QWAK
from qwak.State import State

if __name__ == "__main__":

    state = State(4, [0, 1, 2, 3])
    state.buildState()
    json_str = state.to_json()
    print(json_str)

    state2 = State.from_json(json_str)
    print(state2.getStateVec())
    state2.buildState(customStateList=[(0,-1)])
    print(state2.getStateVec())
