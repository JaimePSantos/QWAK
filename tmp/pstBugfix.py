from qwak.qwak import QWAK
import networkx as nx
import numpy as np
import matplotlib as mpl
from matplotlib import pyplot as plt

n1 = 4
n2 = 3
n3 = 4

graph1 = nx.cycle_graph(n1)
graph2 = nx.path_graph(n2)
graph3 = nx.hypercube_graph(n3)

qw1 = QWAK(graph=graph1)
qw2 = QWAK(graph=graph2)
qw3 = QWAK(graph=graph3)

# print(f'\n ########################################## PATH PST - SYMPY ########################################## \n' )
# print(f'{qw2.checkPST_sympy(0,2)}')
# print(f'\n ###########################k############### PATH PST - NUMPY ########################################## \n' )
# print(f'{qw2.checkPST(0,2)}')

print(f'Cycle PST: {qw1.checkPST(0,2)}')
print(f'Path PST: {qw2.checkPST(0,2)}')
print(f'Cube PST: {qw3.checkPST(0,15)}')
