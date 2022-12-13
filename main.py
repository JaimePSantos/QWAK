import networkx as nx
from matplotlib import pyplot as plt
import numpy as np

from qwak.GraphicalQWAK import GraphicalQWAK
from qwak.qwak import QWAK
from qwak.State import State
from qwak.Operator import Operator
from qwak.QuantumWalk import QuantumWalk
from qwak.ProbabilityDistribution import ProbabilityDistribution


if __name__ == "__main__":

    state = State(4, [0, 1, 2, 3])
    state.buildState()
    st_json_str = state.to_json()
    print(st_json_str)

    deserialized_state = State.from_json(st_json_str)
    # print(state2.getStateVec())
    deserialized_state.buildState()
    print(deserialized_state)
    # print(state2.getStateVec())
    #
    # graph = nx.cycle_graph(4)
    # operator = Operator(graph,0.1)
    # operator.buildDiagonalOperator()
    # # print(operator.getOperator())
    #
    # # Serialize the operator to JSON
    # op_json_str = operator.to_json()
    # # print(op_json_str)
    #
    # # Deserialize the JSON string back into an instance of the Operator class
    # deserialized_operator = Operator.from_json(op_json_str)
    # # print(deserialized_operator.getOperator())
    # deserialized_operator.buildDiagonalOperator(1)
    # # print(deserialized_operator.getOperator())
    #
    # quantumWalk = QuantumWalk(state=deserialized_state,operator=deserialized_operator)
    # # print(quantumWalk.getOperator())
    # qw_json_str = quantumWalk.to_json()
    # # print(qw_json_str)
    #
    # deserialized_walk = QuantumWalk.from_json(qw_json_str)
    # # print(deserialized_walk.getFinalState())
    #
    # deserialized_walk.buildWalk()
    # # print(deserialized_walk.getOperator())
    # # print(deserialized_walk.getFinalState())
    # # print(quantumWalk.getInitState())
    #
    # probDist = ProbabilityDistribution(deserialized_walk.getFinalState())
    # # print(probDist.getProbVec())
    # probDist_json_str = probDist.to_json()
    #
    # deserialized_probDist = ProbabilityDistribution.from_json(probDist_json_str)
    # deserialized_probDist.buildProbDist()
    # # print(deserialized_probDist)

    # graph = nx.cycle_graph(100)
    # qwak = QWAK(graph)
    # qwak_json_str = qwak.to_json()
    #
    # deserialized_qwak = QWAK.from_json(qwak_json_str)
    # deserialized_qwak.runWalk(time=10,initStateList=[50])
    # plt.plot(deserialized_qwak.getProbVec())
    # plt.show()
    # staticN = 100
    # dynamicN = 100
    # t = 0
    # initState = [2]
    # staticGraph = nx.cycle_graph(staticN)
    # dynamicGraph = nx.cycle_graph(dynamicN)
    # timeList = [0, 10]
    # initStateList = [[dynamicN//2,dynamicN//2 + 1]]
    #
    # gQwak = GraphicalQWAK(
    #     staticN=staticN,
    #     dynamicN=dynamicN,
    #     staticGraph=staticGraph,
    #     dynamicGraph=dynamicGraph,
    #     staticStateList=initState,
    #     dynamicStateList=initStateList,
    #     staticTime=t,
    #     dynamicTimeList=timeList)
    #
    # gQwak_json_string = gQwak.to_json()
    #
    # deserialized_gQwak = GraphicalQWAK.from_json(gQwak_json_string)
    # # deserialized_gQwak.runWalk()
    # deserialized_gQwak.runMultipleWalks()
    #
    # for walks in deserialized_gQwak.getDynamicProbVecList():
    #     print('bla')
    #     plt.plot(walks)
    # plt.show()

