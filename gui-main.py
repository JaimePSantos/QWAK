import eel
eel.init('GraphicalInterface')

import networkx as nx
import numpy as np
from matplotlib import pyplot as plt
import timeit
import json

from QuantumWalk.State import State
from QuantumWalk.Operator import Operator
from QuantumWalk.QuantumWalk import QuantumWalk
from QuantumWalk.ProbabilityDistribution import ProbabilityDistribution
from QuantumWalk.QuantumWalkDao import QuantumWalkDao

if __name__ == '__main__':
    n = 1000
    t= n/2
    gamma=1/(2*np.sqrt(2))
    marked = [int(n/2)]

    @eel.expose
    def runWalk():
        qwController = QuantumWalkDao(n,nx.cycle_graph(n),t,gamma,marked)
        qwAmplitudes = qwController.getWalk()
        qwProbabilities = qwController.getProbDist()
        probLists = qwProbabilities.tolist()
        return probLists

    def print_num(n):
        print('Got this from Javascript:', n)

    eel.start('index.html',port=8080,cmdline_args=['--start-maximized'])
    pass