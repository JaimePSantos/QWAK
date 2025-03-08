from qwak.qwak import QWAK
import networkx as nx
import numpy as np
import matplotlib as mpl
from matplotlib import pyplot as plt
import scipy.special as sp
from scipy.linalg import expm
import sympy as simp
from utils.plotTools import plot_qwak, plot_qwak_heatmap
import math
import copy
import os
import seaborn as sns
import pandas as pd
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
            markedProbability += probDist.searchNodeProbability(element[0])
        markedProbDistList.append(markedProbability)
        markedProbability = 0
    return markedProbDistList

def multiple_erdos_renyi_qwak(N, pList, timeList, numberOfWalks, markedElements):
    markedProbMatrix = []
    markedProbList = [0] * len(timeList)
    probDistList = []
    pValMatrix = []
    sampleCounter = 1
    for pVal in pList:
        print(f'PVAL {round(pVal, 4)}/{max(pList)} \t Sample {sampleCounter}/{len(pList)}')
        sampleCounter += 1
        for i in range(numberOfWalks):
            graph = nx.erdos_renyi_graph(N, pVal)
            gamma = 1 / (N * pVal) if pVal <= 1 else 1 / N
            initCond = list(range(len(graph)))
            qw = QWAK(graph=graph, gamma=gamma, markedElements=markedElements, laplacian=False)
            for t in timeList:
                qw.runWalk(time=t, initStateList=initCond)
                probDistList.append(copy.deepcopy(qw.getProbDist()))
            markedElementList = searchProbStepsPlotting2(qw, probDistList)
            markedProbList = [x + y for x, y in zip(markedProbList, markedElementList)]
            probDistList = []
        pValMatrix.append([pVal] * len(timeList))
        timeMatrix = [timeList] * len(timeList)
        markedProbListAvg = [x / numberOfWalks for x in markedProbList]
        markedProbMatrix.append(markedProbListAvg)
        markedProbList = [0] * len(timeList)

    return pValMatrix, timeMatrix, markedProbMatrix

n = 9
N = 2**n
p = math.log(N, 3/2) / N
pMax = 0.5
samples = 200
numberOfWalks = 40
t = np.pi / 2 * np.sqrt(N)
markedElements = [(0, -1)]

pAux = p / samples
pList = np.linspace(pAux, pMax, samples)

tAux = t / samples
timeList = np.linspace(0, 2 * t, samples)

SCRIPT_DIR = os.getcwd()
dataset_dir = os.path.normpath(os.path.join(SCRIPT_DIR,'Notebook', "Datasets", "ERSearch"))
output_dir = os.path.normpath(os.path.join(SCRIPT_DIR, 'Notebook',"Output", "ERSearch"))

time_file = os.path.join(dataset_dir, f'timeMatrix_N{N}_NGRAPHS{numberOfWalks}_S{samples}_PMAX{pMax}.txt')
pval_file = os.path.join(dataset_dir, f'pValMatrix_N{N}_NGRAPHS{numberOfWalks}_S{samples}_PMAX{pMax}.txt')
marked_prob_file = os.path.join(dataset_dir, f'markedProbMatrix_N{N}_NGRAPHS{numberOfWalks}_S{samples}_PMAX{pMax}.txt')

if os.path.exists(time_file) and os.path.exists(pval_file) and os.path.exists(marked_prob_file):
    x = load_nested_list_from_file(pval_file)
    y = load_nested_list_from_file(time_file)
    z = load_nested_list_from_file(marked_prob_file)
    print('File exists!')
else:
    x, y, z = multiple_erdos_renyi_qwak(N, pList, timeList, numberOfWalks, markedElements)
    if not os.path.exists(pval_file):
        write_nested_list_to_file(pval_file, x)
    if not os.path.exists(time_file):
        write_nested_list_to_file(time_file, y)
    if not os.path.exists(marked_prob_file):
        write_nested_list_to_file(marked_prob_file, z)

newP = math.log(N, 2) / N

x_num_ticks = 6
y_num_ticks = 7
x_round_val = 1
y_round_val = 1

xlabel = r'P values $\times 10^2$'
ylabel = 'Time'
cbar_label = 'Solution Probability'

font_size = 12
figsize = (11, 5)
colormap = sns.color_palette("icefire", as_cmap=True)
x_vline_value = newP
y_vline_value = t

heatMapPlotFile = os.path.join(output_dir, f'heatMapPlot_N{N}_NGRAPHS{numberOfWalks}_S{samples}_PMAX{pMax}.png')
params = {
    'font_size': 18,  # Decreased font size
    'figsize': (16, 10),  # Increased figure size
    'x_num_ticks': x_num_ticks,
    'y_num_ticks': y_num_ticks,
    'x_round_val': x_round_val,
    'y_round_val': y_round_val,
    'filepath': heatMapPlotFile,
    'N': N,
    'xlabel': xlabel,
    'ylabel': ylabel,
    'cbar_label': cbar_label,
    'cmap': colormap,
    'x_vline_value': x_vline_value,
    'y_hline_value': y_vline_value,
    'title_font_size': 34,  # Decreased font size
    'xlabel_font_size': 28,  # Decreased font size
    'ylabel_font_size': 28,  # Decreased font size
    'legend_font_size': 28,  # Decreased font size
    'legend_title_font_size': 30,  # Decreased font size
    'tick_font_size': 26,  # Decreased font size
    'cbar_label_font_size': 44,  # Kept font size for "Solution Probability"
}

plot_qwak_heatmap(p_values=x, t_values=y, prob_values=z, **params)

# Save the plot using the filepath in params
# plt.savefig(params['filepath'], bbox_inches='tight')
plt.show()

copy_to_latex = input("Do you want to copy the generated image to the LaTeX project? (y/n): ").strip().lower()
if copy_to_latex == 'y':
    latex_project_path = os.path.normpath(os.path.join(
        SCRIPT_DIR,
        "../QWAK-Paper_Revised/img/newFigures"
    ))
    shutil.copy(params['filepath'], latex_project_path)
    print(f"Image copied to {latex_project_path}")
else:
    print("Image not copied.")