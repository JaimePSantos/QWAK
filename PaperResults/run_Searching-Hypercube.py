from qwak.qwak import QWAK
import networkx as nx
import numpy as np
import matplotlib as mpl
from matplotlib import pyplot as plt
from math import sqrt, ceil, pow
from scipy.linalg import expm
import math
import copy
import os
from utils.plotTools import plot_qwak
import shutil


def write_nested_list_to_file(file_path, nested_lst):
    """
    Write a nested list of elements to a text file.

    :param file_path: the file path where to write the nested list
    :param nested_lst: the nested list of elements to write
    """
    with open(file_path, 'w') as f:
        for lst in nested_lst:
            f.write(" ".join(map(str, lst)) + "\n")


def load_nested_list_from_file(file_path):
    """
    Load a nested list of float elements from a text file.

    :param file_path: the file path to load the nested list from
    :return: the nested list of float elements loaded from the file
    """
    nested_lst = []
    with open(file_path, 'r') as f:
        for line in f:
            lst = [float(item) for item in line.strip().split()]
            nested_lst.append(lst)
    return nested_lst


def write_list_to_file(file_path, lst):
    """
    Write a list of elements to a text file.

    :param file_path: the file path where to write the list
    :param lst: the list of elements to write
    """
    with open(file_path, 'w') as f:
        f.write(" ".join(map(str, lst)) + "\n")


def load_list_from_file(file_path):
    """
    Load a list of float elements from a text file.

    :param file_path: the file path to load the list from
    :return: the list of float elements loaded from the file
    """
    with open(file_path, 'r') as f:
        line = f.readline()
        return [float(item) for item in line.strip().split()]


def gamma_hypercube(n):
    total = 0
    for r in range(1, n + 1):
        binomial_coefficient = math.comb(n, r)
        total += binomial_coefficient * (1 / r)
    return ((1 / (2 ** n)) * total) / 2


def searchProbStepsPlotting2(qwak: QWAK, probDistList):
    """Plots the probability of finding the target as a function of the number of steps.

    Parameters
    ----------
    qwak : QWAK
        QWAK object containing the results of the simulation.
    """
    markedProbability = 0
    markedProbDistList = []
    markdElements = qwak.getMarkedElements()
    if not probDistList:
        raise ValueError("The probability distribution list is empty.")
    for probDist in probDistList:
        for element in markdElements:
            markedProbability += probDist.searchNodeProbability(
                element[0])
        markedProbDistList.append(markedProbability)
        markedProbability = 0
    return markedProbDistList


def multiple_hypercube_qwak(
        N,
        gammaList,
        timeList,
        markedElements,
        initCond):
    markedProbMatrix = []
    sampleCounter = 1
    for gamma in gammaList:
        qw = QWAK(
            graph=graph,
            gamma=gamma,
            markedElements=markedElements,
            laplacian=False)
        print(f'GAMMA {round(gamma, 4)}/{max(gammaList)
                                         } \t Sample {sampleCounter}/{len(gammaList)}')
        sampleCounter += 1
        probDistList = []
        for time in timeList:
            qw.runWalk(time=time, initStateList=initCond)
            probDistList.append(copy.deepcopy(qw.getProbDist()))
        markedProbList = searchProbStepsPlotting2(qw, probDistList)
        markedProbMatrix.append(markedProbList)
    return markedProbMatrix


n = 9
graph = nx.hypercube_graph(n)
gamma = gamma_hypercube(n)
gammaMin = gamma / 1.10

N = len(graph)
t = np.pi / 2 * np.sqrt(N)
maxTime = 2.2 * t

print(f'N = {N}')
print(f'GammaMin = {gammaMin}')
print(f'T = {t}')

initCond = list(range(len(graph)))

samples = 200
timeList = np.linspace(0, maxTime, samples)
gammaList = np.linspace(gammaMin, gamma, samples).tolist()
markedElements = [(N // 2, -1)]

SCRIPT_DIR = os.getcwd()
dataset_dir = os.path.normpath(
    os.path.join(
        SCRIPT_DIR,
        "Datasets",
        "HypercubeSearch"))
output_dir = os.path.normpath(
    os.path.join(
        SCRIPT_DIR,
        "Output",
        "HypercubeSearch"))

time_file = os.path.join(
    dataset_dir,
    f'timeMatrix_N{N}_S{samples}_GMIN{
        round(
            gammaMin,
            3)}_TMAX{
                round(maxTime)}.txt')
marked_prob_file = os.path.join(
    dataset_dir,
    f'markedProbMatrix_N{N}_S{samples}_GMIN{
        round(
            gammaMin,
            3)}_TMAX{
                round(maxTime)}.txt')

if os.path.exists(time_file) and os.path.exists(marked_prob_file):
    timeList = load_list_from_file(time_file)
    markedProbMatrix = load_nested_list_from_file(marked_prob_file)
    print('File exists!')
else:
    print('File Doesnt Exist!')
    markedProbMatrix = multiple_hypercube_qwak(
        N, gammaList, timeList, markedElements, initCond)
    if not os.path.exists(time_file):
        write_list_to_file(time_file, timeList)
    if not os.path.exists(marked_prob_file):
        write_nested_list_to_file(marked_prob_file, markedProbMatrix)

colors = plt.cm.rainbow(np.linspace(0, 1, len(gammaList)))
lines = ['-'] * len(gammaList)
configVec = list(zip(colors, lines))

color_list = plt.cm.rainbow(np.linspace(0, 1, len(gammaList)))

v_line_values = [
    (timeList[np.argmax(markedProbMatrix[-1])], np.max(markedProbMatrix[-1]))]
print(v_line_values)

cbar_num_ticks = 10
params = {
    'font_size': 24,  # Increased font size
    'figsize': (16, 10),  # Increased figure size
    'plot_title': f'Hypercube N={N}',
    'x_label': 'Time',
    'y_label': 'Probability',
    'legend_labels': None,
    'legend_loc': None,
    'legend_title': 'Solutions',
    'legend_ncol': 1,
    'color_list': color_list,
    'save_path': os.path.join(output_dir, f'hypercubePlot_N{N}_S{samples}_GMIN{round(gammaMin, 3)}_TMAX{round(maxTime)}.png'),
    'use_loglog': False,
    'use_cbar': True,
    'cbar_label': 'Hopping Rate',
    'cbar_ticks': None,
    'cbar_tick_labels': [r' $\gamma = \frac{10}{11}\gamma_{opt}$'] + [f'{round(x, 3)}' for x in np.linspace(gammaMin, gamma, cbar_num_ticks - 2).tolist()] + [r' $\gamma = \gamma_{opt}$'],
    'cbar_num_ticks': cbar_num_ticks,
    'x_lim': None,
    # 'x_num_ticks': 7,
    'y_num_ticks': 7,
    'x_round_val': 1,
    'y_round_val': 3,
    'v_line_values': v_line_values,
    'v_line_style': '--',
    'v_line_list_index': len(gammaList) - 1,
    'title_font_size': 44,  # Increased font size
    'xlabel_font_size': 38,  # Increased font size
    'ylabel_font_size': 38,  # Increased font size
    'legend_font_size': 34,  # Increased font size
    'legend_title_font_size': 36,  # Increased font size
    'tick_font_size': 34,  # Increased font size
}

plot_qwak(
    x_value_matrix=[timeList] *
    len(markedProbMatrix),
    y_value_matrix=markedProbMatrix,
    **params)

# plt.savefig(params['save_path'], bbox_inches='tight')
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
