import networkx as nx
import numpy as np
import matplotlib.pyplot as plt
from qwak.StochasticQwak import StochasticQWAK
from Maze import Maze
import os
import shutil
from utils.plotTools import plot_qwak  # Import plot_qwak

maze_graph = Maze(maze_size=(10,10))
maze_graph.plot_maze()
plt.show()

graph = nx.from_numpy_array(maze_graph.adjacency)
qwak = StochasticQWAK(graph, noiseParam=0.1, sinkNode=99, sinkRate=0.99)

exit_prob = []
exit_prob_opt = []
exit_prob_class = []

times = []

for i in range(10):
    t = 100 * i
    initState = [0]
    qwak.runWalk(t, initState)

    probVec = qwak.getProbVec()
    exit_prob_opt.append(probVec[-1])
    exit_prob.append(probVec[-1])
    exit_prob_class.append(probVec[-1])
    times.append(t)

params = {
    'font_size': 24,
    'figsize': (16, 10),
    'plot_title': 'Stochastic QWAK',
    'x_label': 'Time',
    'y_label': "Exit probability",
    'legend_labels': [r'$p=0$', r'$p=1$', r'$p=0.1$'],
    'legend_loc': "best",
    'legend_title': 'Noise Parameters',
    'legend_ncol': 1,
    'color_list': ['b', 'g', 'r'],
    'line_style_list': ['--', '-', '-.'],
    'save_path': os.path.join('output_dir', 'stochasticPlot.png'),
    'use_loglog': False,
    'use_cbar': False,
    'cbar_label': None,
    'cbar_ticks': None,
    'cbar_tick_labels': None,
    'x_lim': None,
    'x_num_ticks': 7,
    'y_num_ticks': 5,
    'x_round_val': 2,
    'y_round_val': 3,
    'v_line_values': None,
    'v_line_style': '--',
    'title_font_size': 44,
    'xlabel_font_size': 38,
    'ylabel_font_size': 38,
    'legend_font_size': 34,
    'legend_title_font_size': 36,
    'tick_font_size': 34,
}

# Use plot_qwak for plotting
plot_qwak(
    x_value_matrix=[times, times, times],
    y_value_matrix=[exit_prob, exit_prob_class, exit_prob_opt],
    **params
)
plt.show()

copy_to_latex = input("Do you want to copy the generated image to the LaTeX project? (y/n): ").strip().lower()
if copy_to_latex == 'y':
    latex_project_path = os.path.normpath(os.path.join(
        os.getcwd(),
        "../QWAK-Paper_Revised/img/newFigures"
    ))
    shutil.copy(params['save_path'], latex_project_path)
    print(f"Image copied to {latex_project_path}")
else:
    print("Image not copied.")