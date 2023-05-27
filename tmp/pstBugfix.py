from qwak.qwak import QWAK
import networkx as nx
import numpy as np
import matplotlib as mpl
from matplotlib import pyplot as plt

n=3
graph = nx.hypercube_graph(n)
t = 0
initCond = [0]

qw = QWAK(graph=graph)
print(f'PST: {qw.checkPST(0,7)}')
qw.runWalk(time=t,initStateList=initCond)