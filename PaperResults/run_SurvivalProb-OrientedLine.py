from qwak.qwak import QWAK
from utils.plotTools import plot_qwak
import networkx as nx
import numpy as np
import matplotlib as mpl
from matplotlib import pyplot as plt
import scipy.special as sp
from scipy.linalg import expm
import sympy as simp
import os
import shutil

def write_nested_list_to_file(file_path, nested_lst):
    """
    Write a nested list of elements to a text file.
    
    :param file_path: the file path where to write the nested list
    :param nested_lst: the nested list of elements to write
    """
    with open(file_path, 'w') as f:
        for lst in nested_lst:
            for item in lst:
                f.write(f"{item} ")
            f.write("\n")

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

def getWeightedGraph(graph,weight):
    revGraph = graph.reverse()
    for u,v,d in graph.edges(data=True):
        d["weight"] = weight
    for u,v,d in revGraph.edges(data=True):
        d["weight"] = np.conj(weight)
    return nx.compose(graph,revGraph)

def multiple_oriented_decayRate(N, k,fromNode, toNode, timeList, baseGraph, alphaList, initCond):
    decayRateMatrix = []
    for alpha in alphaList:
        weight = np.exp(1j * alpha)
        graph = getWeightedGraph(baseGraph, weight)
        qw = QWAK(graph)
        qw.runMultipleWalks(timeList=timeList, customStateList=initCond)
        decayRateMatrix.append(qw.getSurvivalProbList(fromNode,toNode))
    return decayRateMatrix

n =  9
N = 2 ** n
print(N)

alpha = np.pi / 2
alphaList = [0, np.pi/ 3, np.pi/ 2 ]
print(alphaList)
alphaLabelList = [r'$0$', r'$\frac{\pi}{3}$', r'$\frac{\pi}{2}$']

baseGraph = nx.path_graph(N, create_using=nx.DiGraph)

k = 1
if k > 0:
    theta = np.pi / 4
else:
    theta = np.pi / 2

l = 0
gamma = l * np.pi

t = 100 
samples = 500
timeList = np.linspace(1, t, samples)
timeMatrix = [timeList]*len(alphaList)
initCond = [(N // 2 - k, np.cos(theta)), (N // 2 + k, np.exp(1j * gamma) * np.sin(theta))]

fromNode = N // 2 - k - 1
toNode = N // 2 + k + 1

SCRIPT_DIR = os.getcwd()

decayRateMatrix_file = os.path.normpath(os.path.join(SCRIPT_DIR, 'Datasets', 'OrientedDecayRate', 
    f'decayRateMatrix{N}_NWALKS{len(alphaList)}_Alphas{str([round(a, 2) for a in alphaList]).replace(", ", "-").replace("[", "").replace("]", "")}_S{samples}_TMAX{t}_FROM{fromNode}_TO{toNode}.txt'))

if os.path.exists(decayRateMatrix_file):
    decayRateMatrix = load_nested_list_from_file(decayRateMatrix_file)
    print('File exists!')
else:
    print('File Doesnt Exist!')
    decayRateMatrix = multiple_oriented_decayRate(N, k, fromNode, toNode, timeList, baseGraph, alphaList, initCond)
    if not os.path.exists(decayRateMatrix_file):
        write_nested_list_to_file(decayRateMatrix_file, decayRateMatrix)

output_dir = os.path.normpath(os.path.join(SCRIPT_DIR, 'Output', 'OrientedDecayRate'))
if not os.path.exists(output_dir):
    os.makedirs(output_dir)

save_path = os.path.join(output_dir, 
    f'decayRateMatrix{N}_NWALKS{len(alphaList)}_Alphas{str([round(a, 2) for a in alphaList]).replace(", ", "-").replace("[", "").replace("]", "")}_S{samples}_TMAX{t}_FROM{fromNode}_TO{toNode}.png')

params = {
    'font_size': 24,
    'figsize': (16, 10),
    'plot_title': f'Decay Rate N={N}',
    'x_label': 'Time',
    'y_label': r"$P_{[-%s,%s]}$" % (k, k),
    'legend_labels': alphaLabelList,
    'legend_loc': "lower left",
    'legend_title': r'$\alpha$',
    'legend_ncol': 3,
    'color_list': ['b', 'g', 'r'],
    'line_style_list': ['--', '-.', '-'],
    'save_path': save_path,
    'use_loglog': True,
    'use_cbar': False,
    'cbar_label': None,
    'cbar_ticks': None,
    'cbar_tick_labels': None,
    'x_lim': [timeList[1], timeList[-1]],
    'title_font_size': 46,
    'xlabel_font_size': 40,
    'ylabel_font_size': 40,
    'legend_font_size': 36,
    'legend_title_font_size': 38,
    'tick_font_size': 36,
}

plot_qwak(x_value_matrix=timeMatrix, y_value_matrix=decayRateMatrix, **params)

copy_to_latex = input("Do you want to copy the generated image to the LaTeX project? (y/n): ").strip().lower()
if copy_to_latex == 'y':
    latex_project_path = os.path.normpath(os.path.join(
        SCRIPT_DIR,
        "../QWAK-Paper_Revised/img/newFigures"
    ))
    shutil.copy(params['save_path'], latex_project_path)
    print(f"Image copied to {latex_project_path}")
else:
    print("Image not copied.")