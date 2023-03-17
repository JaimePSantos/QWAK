from qwak.qwak import QWAK
from utils.plotTools import searchProbStepsPlotting,searchProbStepsPlotting2

import networkx as nx
import numpy as np
import matplotlib as mpl
from matplotlib import pyplot as plt
from math import sqrt, ceil, pow
import scipy.special as sp
from scipy.linalg import expm
import sympy as simp
import math
from qwak.State import State
from qwak.Operator import Operator
from qwak.QuantumWalk import QuantumWalk
from qwak.ProbabilityDistribution import ProbabilityDistribution
from qwak.qwak import QWAK
import copy
import plotly.graph_objects as go
import seaborn as sns
import matplotlib.pyplot as plt
import pandas as pd
import os
from matplotlib.colors import ListedColormap, BoundaryNorm, LinearSegmentedColormap
from scipy.ndimage import gaussian_filter


def modify_marked_prob_list(marked_prob_list):
    modified_list = []
    for sublist in marked_prob_list:
        new_sublist = sublist.copy()

        max_idx = new_sublist.index(max(new_sublist))
        min_found = False
        last_min_value = None

        for idx, elem in enumerate(new_sublist[max_idx:]):
            if idx + max_idx > 0 and new_sublist[idx + max_idx - 1] > elem:
                min_found = True
                last_min_value = elem
            if min_found and new_sublist[idx + max_idx - 1] < elem:
                new_sublist[idx + max_idx:] = [last_min_value] * len(new_sublist[idx + max_idx:])
                break

        modified_list.append(new_sublist)
    return modified_list


def smooth_matrices(matrix1, matrix2, matrix3, sigma=1):
    """
    Applies 2D Gaussian smoothing to three input matrices.

    Parameters:
        matrix1 (numpy array): first input matrix
        matrix2 (numpy array): second input matrix
        matrix3 (numpy array): third input matrix
        sigma (float): standard deviation of the Gaussian filter

    Returns:
        tuple: a tuple of three smoothed matrices
    """
    smoothed_matrix1 = gaussian_filter(matrix1, sigma=sigma)
    smoothed_matrix2 = gaussian_filter(matrix2, sigma=sigma)
    smoothed_matrix3 = gaussian_filter(matrix3, sigma=sigma)

    return (smoothed_matrix1, smoothed_matrix2, smoothed_matrix3)

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

def gamma_hypercube(n):
    total = 0
    for r in range(1, n + 1):
        binomial_coefficient = math.comb(n, r)
        total += binomial_coefficient * (1 / r)
    return ((1 / (2 ** n)) * total) / 2



def plot_search(markedList, probT, tSpace, configVec, gamma_range, x_num_ticks=5, y_num_ticks=5, round_val=3, filepath=None,
                xlabel='Number of steps', ylabel='Probability of marked elements', cbar_label='Gamma', font_size=12, figsize=(8, 6),
                cbar_num_ticks=None, cbar_tick_labels=None, plot_title='Hypercube Search'):

    fig, ax = plt.subplots(figsize=figsize)

    max_prob = np.max(np.array(probT))

    for T, walk, config, marked in zip(tSpace, probT, configVec, markedList):
        ax.plot(T, walk, color=config[0], linestyle=config[1])
        ax.set_xlabel(xlabel, fontsize=font_size + 2)
        ax.set_ylabel(ylabel, fontsize=font_size + 2)
        ax.set_title(plot_title, fontsize=font_size+4)

    ax.tick_params(axis='both', which='major', labelsize=font_size)

    num_t_ticks = min(y_num_ticks, len(tSpace[0]))
    t_tick_labels = np.round(np.linspace(min(tSpace[0]), max(tSpace[0]), num_t_ticks), round_val)

    ax.set_yticks(np.linspace(0, max_prob, num_t_ticks))
    ax.set_yticklabels(np.round(np.linspace(0, max_prob, num_t_ticks), round_val))

    colors = [config[0] for config in configVec]
    cmap = LinearSegmentedColormap.from_list('custom_cmap', colors, N=len(colors))
    norm = BoundaryNorm(gamma_range, len(gamma_range)-1)

    if cbar_num_ticks is not None:
        cbar_ticks = np.linspace(gamma_range[0], gamma_range[-1], cbar_num_ticks)
    else:
        cbar_ticks = None

    cbar = plt.colorbar(plt.cm.ScalarMappable(norm=norm, cmap=cmap), ax=ax, ticks=cbar_ticks)
    cbar.set_label(cbar_label, fontsize=font_size + 2)
    cbar.ax.tick_params(labelsize=font_size)

    if cbar_tick_labels is not None:
        cbar.ax.set_yticklabels(cbar_tick_labels)

    if filepath is not None:
        plt.savefig(filepath, bbox_inches='tight')
        plt.show()
    else:
        plt.show()

def multiple_hypercube_qwak(N,gammaList,timeList,markedElements,initCond):
    markedProbList = []
    markedElementsMatrix = []
    timeMatrix = []
    probDistList = []
    markedProbMatrix = []
    sampleCounter = 1
    for gamma in gammaList:
        qw = QWAK(graph=graph,gamma=gamma,markedElements=markedElements,laplacian=False)
        print(f'GAMMA {round(gamma, 4)}/{max(gammaList)} \t Sample {sampleCounter}/{len(gammaList)}')
        sampleCounter += 1
        for time in timeList:
            qw.runWalk(time=time,initStateList=initCond)
            probDistList.append(copy.deepcopy(qw.getProbDist()))
        markedProbList = searchProbStepsPlotting2(qw,probDistList)
        markedProbMatrix.append(markedProbList)
        probDistList = []
        markedElementsMatrix.append(markedElements)
        timeMatrix.append( timeList)
    return markedProbMatrix,markedElementsMatrix,timeMatrix


n=9
graph = nx.hypercube_graph(n)
gamma = gamma_hypercube(n)
gammaMin = gamma/1.10
t =  (np.pi/(2) * np.sqrt(N))
maxTime = 2.2*t

N = len(graph)
print(f'N = {N}')
print(f'GammaMin = {gammaMin}')
print(f'T = {2.2*t}')

initCond = list(range(0,len(graph)))

samples = 200
timeList = np.linspace(0,maxTime,samples)
print(max(timeList))
gammaList =  np.linspace(gammaMin,gamma ,samples).tolist()
markedElements = [(N//2,-1)]

colors = plt.cm.rainbow(np.linspace(0, 1, len(gammaList)))
lines = ['-']*len(gammaList)
configVec = list(zip(colors,lines))

time_file = f'Datasets/HypercubeSearch/timeMatrix_N{N}_S{samples}_GMIN{round(gammaMin,3)}_TMAX{round(maxTime)}.txt'
markedElements_file = f'Datasets/HypercubeSearch/markedElementsMatrix_N{N}_S{samples}_GMIN{round(gammaMin,3)}_TMAX{round(maxTime)}.txt'
marked_prob_file = f'Datasets/HypercubeSearch/markedProbMatrix_N{N}_S{samples}_GMIN{round(gammaMin,3)}_TMAX{round(maxTime)}.txt'

if os.path.exists(time_file) and os.path.exists(markedElements_file) and os.path.exists(marked_prob_file):
    markedProbMatrix = load_nested_list_from_file(marked_prob_file)
    markedElementsMatrix = load_nested_list_from_file(markedElements_file)
    timeMatrix = load_nested_list_from_file(time_file)
    print('File exists!')
else:
    print('File Doesnt Exist!')
    markedProbMatrix,markedElementsMatrix,timeMatrix = multiple_hypercube_qwak(N,gammaList,timeList,markedElements,initCond)
    if not os.path.exists(markedElements_file):
        write_nested_list_to_file(markedElements_file, markedProbMatrix)
    if not os.path.exists(time_file):
        write_nested_list_to_file(time_file, timeMatrix)
    if not os.path.exists(marked_prob_file):
        write_nested_list_to_file(marked_prob_file, markedProbMatrix)
        
gamma_range=gammaList
x_num_ticks=10
y_num_ticks=10
round_val=2

filepath=f'Output/HypercubeSearch/hypercubePlot_N{N}_S{samples}_GMIN{round(gammaMin,3)}_TMAX{round(maxTime)}.png'

plot_title = f'N={N}'

xlabel='Time'
ylabel='Solution Probability'
cbar_label='Hopping Rate'

font_size=14
figsize=(9, 6)

cbar_num_ticks=10

cbar_tick_labels=[r' $\gamma = \frac{10}{11}\gamma_{opt}$'] + [f'{round(x,3)}' for x in np.linspace(gammaMin,gamma ,cbar_num_ticks-2).tolist()] + [r' $\gamma = \gamma_{opt}$']

plot_search(markedList=markedElementsMatrix, probT=markedProbMatrix, tSpace=timeMatrix, configVec=configVec,
            gamma_range=gamma_range,x_num_ticks=x_num_ticks, y_num_ticks=y_num_ticks, round_val=round_val, 
            filepath=filepath,xlabel=xlabel, ylabel=ylabel, cbar_label=cbar_label, font_size=font_size, 
            figsize=figsize,cbar_num_ticks=cbar_num_ticks, cbar_tick_labels=cbar_tick_labels,plot_title=plot_title)