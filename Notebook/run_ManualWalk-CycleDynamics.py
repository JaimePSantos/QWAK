from qwak.State import State
from qwak.Operator import Operator
from qwak.QuantumWalk import QuantumWalk
from qwak.ProbabilityDistribution import ProbabilityDistribution
from qwak.qwak import QWAK
from utils.plotTools import plot_qwak
import networkx as nx
import numpy as np
from matplotlib import pyplot as plt
import timeit
import sympy as sp
from sympy.abc import pi
from math import sqrt, ceil, pow
import os
import shutil

SCRIPT_DIR = os.getcwd()

tList = [40, 80, 120]
gamma = 1 / (2 * np.sqrt(2))
n = 200
graph = nx.cycle_graph(n)
initNodes = [n // 2, n // 2 + 1]
quantum_walk = QWAK(graph, gamma=gamma)

probVecList = []

for t in tList:
    quantum_walk.runWalk(t, initNodes)
    probVecList.append(quantum_walk.getProbVec())

n = len(graph)
nodeList = list(range(0, n))

params = {
    'font_size': 24,
    'figsize': (16, 10),
    'plot_title': f'Cycle Graph N={n}',
    'x_label': 'Nodes',
    'y_label': "Probability",
    'legend_labels': tList,
    'legend_loc': "best",
    'legend_title': r'Time Interval',
    'legend_ncol': 1,
    'color_list': ['#0000FF', '#008000', '#525252'],
    'line_style_list': ['-', '-', '-.'],
    'save_path': os.path.join(SCRIPT_DIR, 'Notebook', 'Output', 'UndirectedDynamics', f'cycleDynamics_N{n}_GAM{round(gamma, 3)}_TMAX{str(tList).replace(", ", "-").replace("[", "").replace("]", "")}.png'),
    'use_loglog': False,
    'use_cbar': False,
    'cbar_label': None,
    'cbar_ticks': None,
    'cbar_tick_labels': None,
    'x_lim': None,
    # 'x_num_ticks': 7,
    'y_num_ticks': 7,
    'x_round_val': 1,
    'y_round_val': 3,
    'title_font_size': 44,
    'xlabel_font_size': 38,
    'ylabel_font_size': 38,
    'legend_font_size': 34,
    'legend_title_font_size': 36,
    'tick_font_size': 34,
}

plot_qwak(
    x_value_matrix=[nodeList] * 3,
    y_value_matrix=probVecList,
    **params)
plt.show()

copy_to_latex = input(
    "Do you want to copy the generated image to the LaTeX project? (y/n): ").strip().lower()
if copy_to_latex == 'y':
    latex_project_path = os.path.normpath(os.path.join(
        SCRIPT_DIR,
        "../QWAK-Paper_Revised/img/newFigures"
    ))
    shutil.copy(params['save_path'], latex_project_path)
    print(f"Image copied to {latex_project_path}")
else:
    print("Image not copied.")
