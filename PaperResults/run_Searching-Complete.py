from qwak.qwak import QWAK
from utils.plotTools import plot_qwak

import networkx as nx
import numpy as np
import matplotlib.pyplot as plt
import os
import copy
import shutil

SCRIPT_DIR = os.getcwd()


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


def searchProbStepsPlotting(qwak: QWAK):
    """Plots the probability of finding the target as a function of the number of steps.

    Parameters
    ----------
    qwak : QWAK
        QWAK object containing the results of the simulation.
    """
    markedProbability = 0
    markedProbDistList = []
    markdElements = qwak.getMarkedElements()
    probDistList = qwak.getProbDistList()
    for probDist in probDistList:
        for element in markdElements:
            markedProbability += probDist.searchNodeProbability(
                element[0])
        markedProbDistList.append(markedProbability)
        markedProbability = 0
    return markedProbDistList


def multiple_complete_qwak(
        N,
        markedElementMatrix,
        gamma,
        initCond,
        graph,
        numberOfWalks,
        samples):
    markedProbMatrix = []
    timeMatrix = []
    for markedElements in markedElementMatrix:
        t = (np.pi / 2) * np.sqrt(N / len(markedElements))
        print(t)
        timeList = [x for x in np.linspace(0, t, samples)]
        qw = QWAK(
            graph=graph,
            gamma=gamma,
            initStateList=initCond,
            markedElements=markedElements)
        qw.runMultipleWalks(timeList=timeList)
        solutionProbList = searchProbStepsPlotting(qw)
        markedProbMatrix.append(solutionProbList)
        timeMatrix.append(timeList)
    return timeMatrix, markedProbMatrix


numberOfWalks = 3
samples = 200

n = 9
N = 2**n
print(N)
t = (np.pi / 2) * np.sqrt(N)
timeList = [x for x in np.linspace(0, t, samples)]
gamma = 1 / N
initCond = list(range(0, N))
graph = nx.complete_graph(N)

markedElementsMatrix = [
    [(x, -1) for x in range(0, N // 16)],
    [(x, -1) for x in range(0, N // 8)],
    [(x, -1) for x in range(0, N // 4)]
]

dataset_dir = os.path.normpath(
    os.path.join(
        SCRIPT_DIR,
        "Datasets",
        "CompleteSearch"))
output_dir = os.path.normpath(
    os.path.join(
        SCRIPT_DIR,
        "Output",
        "CompleteSearch"))

timeMatrix_file = os.path.join(dataset_dir, f'timeMatrix_N{N}_NWALKS{
                               numberOfWalks}_S{samples}.txt')
markedProbMatrix_file = os.path.join(dataset_dir, f'markedProbMatrix_N{
                                     N}_NWALKS{numberOfWalks}_S{samples}.txt')

if os.path.exists(timeMatrix_file) and os.path.exists(
        markedProbMatrix_file):
    timeMatrix = load_nested_list_from_file(timeMatrix_file)
    markedProbMatrix = load_nested_list_from_file(markedProbMatrix_file)
    print('File exists!')
else:
    print('File Doesnt Exist!')
    timeMatrix, markedProbMatrix = multiple_complete_qwak(N=N, markedElementMatrix=markedElementsMatrix, gamma=gamma,
                                                          initCond=initCond, graph=graph, numberOfWalks=numberOfWalks,
                                                          samples=samples)
    if not os.path.exists(timeMatrix_file):
        write_nested_list_to_file(timeMatrix_file, timeMatrix)
    if not os.path.exists(markedProbMatrix_file):
        write_nested_list_to_file(
            markedProbMatrix_file, markedProbMatrix)

legend_labels = [f'{len(marked)}' for marked in markedElementsMatrix]

v_line_values = [(T[np.argmax(walk)], np.max(walk))
                 for T, walk in zip(timeMatrix, markedProbMatrix)]

params = {
    'font_size': 24,
    'figsize': (16, 10),  # Increased figure size
    'plot_title': f'Complete N={N}',
    'x_label': 'Time',
    'y_label': "Probability",
    'legend_labels': legend_labels,
    'legend_loc': "best",
    'legend_title': 'Solutions',
    'legend_ncol': 1,
    'color_list': ['b', 'g', 'r'],
    'line_style_list': ['--', '-', '-.'],
    'save_path': os.path.join(output_dir, f'completePlot_N{N}_NWALKS{numberOfWalks}_S{samples}.png'),
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
    'v_line_values': v_line_values,
    'v_line_style': '--',
    'title_font_size': 44,  # Increased font size
    'xlabel_font_size': 38,  # Increased font size
    'ylabel_font_size': 38,  # Increased font size
    'legend_font_size': 34,  # Increased font size
    'legend_title_font_size': 36,  # Increased font size
    'tick_font_size': 34,  # Increased font size
}

plot_qwak(
    x_value_matrix=timeMatrix,
    y_value_matrix=markedProbMatrix,
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
