from qwak.qwak import QWAK
import networkx as nx
import numpy as np
import matplotlib as mpl
from matplotlib import pyplot as plt
import scipy.special as sp
from scipy.linalg import expm
import sympy as simp
from utils.plotTools import plot_qwak
import os
import shutil

SCRIPT_DIR = os.getcwd()


def inf_line_bessel_oriented10(k, nx, t, alpha, theta, gamma, l):
    domain = np.arange(0, nx) - nx // 2
    prob = np.zeros([nx, 1], dtype='complex')
    for x in range(1, nx):
        prob[x, 0] = ((np.cos(theta)**2) * (sp.jv(domain[x] + k, 2 * t)**2) + (np.sin(theta)**2) * (sp.jv(domain[x] - k, 2 * t)**2) + 2 * (
            (-1)**k) * np.cos(2 * alpha * k + gamma) * np.cos(theta) * np.sin(theta) * sp.jv(domain[x] + k, 2 * t) * sp.jv(domain[x] - k, 2 * t))

    return prob


def getMultipleProbs(k, n, theta, l, gamma, alphaList, timeList):
    timeListList = [timeList] * len(alphaList)
    probListAux = []
    probList = []

    for alpha in alphaList:
        for t in timeList:
            psi_oriented = inf_line_bessel_oriented10(
                k, n, t, alpha, theta, gamma, l)
            probListAux.append(
                np.sum(psi_oriented[n // 2 - k - 1:n // 2 + k + 2]))
        probList.append(probListAux)
        probListAux = []

    return probList


def getWeightedGraph(graph, weight):
    revGraph = graph.reverse()
    for u, v, d in graph.edges(data=True):
        d["weight"] = weight
    for u, v, d in revGraph.edges(data=True):
        d["weight"] = np.conj(weight)
    return nx.compose(graph, revGraph)


def multiple_oriented_walks(N, baseGraph, alphaList, initCond):
    probList = []
    for alpha in alphaList:
        weight = np.exp(1j * alpha)
        graph = getWeightedGraph(baseGraph, weight)
        qw = QWAK(graph)
        qw.runWalk(time=t, customStateList=initCond)
        probList.append(qw.getProbVec())
    return probList


n = 9
N = 2**n
print(N)

alpha = np.pi / 2
alphaList = [0, np.pi / 4, np.pi / 2]
alphaLabelList = [r'$0$', r'$\frac{\pi}{4}$', r'$\frac{\pi}{2}$']

baseGraph = nx.path_graph(N, create_using=nx.DiGraph)

k = 3
if k > 0:
    theta = np.pi / 4
else:
    theta = np.pi / 2

l = 0
gamma = l * np.pi

t = 110
initCond = [(N // 2 - k, np.cos(theta)), (N // 2 +
                                          k, np.exp(1j * gamma) * np.sin(theta))]

print(np.cos(theta))
print(N // 2 - k)
print(N // 2 + k)

probMatrix = multiple_oriented_walks(N, baseGraph, alphaList, initCond)


node_value_matrix = [list(range(0, N))] * len(probMatrix)
params = {
    'font_size': 24,
    'figsize': (16, 10),
    'plot_title': f'Directed N={N}',
    'x_label': 'Nodes',
    'y_label': "Probability",
    'legend_labels': alphaLabelList,
    'legend_loc': "best",
    'legend_title': r'$\alpha$',
    'legend_ncol': 3,
    'color_list': ['#0000FF', '#008000', '#525252'],
    'line_style_list': ['--', '-', '-.'],
    'save_path': f'Output/OrientedDynamics/orientedDynamics_N{N}_NWALKS{len(alphaList)}_Alphas{str([round(a, 2) for a in alphaList]).replace(", ", "-").replace("[", "").replace("]", "")}_TMAX{round(t)}.png',
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
    'title_font_size': 46,
    'xlabel_font_size': 40,
    'ylabel_font_size': 40,
    'legend_font_size': 36,
    'legend_title_font_size': 38,
    'tick_font_size': 36,
}

output_dir = os.path.normpath(
    os.path.join(
        SCRIPT_DIR,
        'Notebook',
        "Output",
        "OrientedDynamics"))
if not os.path.exists(output_dir):
    os.makedirs(output_dir)

save_path = os.path.join(output_dir, f'orientedDynamics_N{N}_NWALKS{len(alphaList)}_Alphas{str(
    [round(a, 2) for a in alphaList]).replace(", ", "-").replace("[", "").replace("]", "")}_TMAX{round(t)}.png')

params['save_path'] = save_path

plot_qwak(x_value_matrix=node_value_matrix,
          y_value_matrix=probMatrix, **params)

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
