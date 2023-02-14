import networkx as nx
from matplotlib import pyplot as plt
import numpy as np
import math
import scipy.special as sp
from scipy.linalg import expm
from utils.plotTools import searchProbStepsPlotting

from qwak.GraphicalQWAK import GraphicalQWAK
from qwak.qwak import QWAK
from qwak.State import State
from qwak.Operator import Operator
from qwak.QuantumWalk import QuantumWalk
from qwak.ProbabilityDistribution import ProbabilityDistribution


def plotSearch(N, probT, tSpace, configVec):
    plotName = ""
    for T, walk, config, n in zip(tSpace, probT, configVec, N):
        # print(config)
        plt.plot(T, walk, color=config[0], linestyle=config[1], label="N=%s" % n)
        plt.vlines(max(T), 0, 1, color=config[0], linestyle=config[2])
        plt.legend()
        plt.xlabel("Number of steps")
        plt.ylabel("Probability of marked elements")
    for n in N:
        plotName += '_' + str(n)
    plt.savefig(r"C:\Users\jaime\Documents\GitHub\QWAK\Notebook\Output\\" + f"Search{plotName}")
    # plt.clf()


def plotSearch2(markedList, probT, tSpace, configVec):
    plotName = ""
    for T, walk, config, marked in zip(tSpace, probT, configVec, markedList):
        plt.plot(T, walk, color=config[0], linestyle=config[1], label=f"{len(marked)} Solutions")
        plt.vlines(max(T), 0, max(probT[0]), color=config[0], linestyle=config[2])
        plt.legend()
        plt.xlabel("Number of steps")
        plt.ylabel("Probability of marked elements")
    for marked in markedList:
        plotName += '_' + str(len(marked))
    # plt.savefig(r"C:\Users\jaime\Documents\GitHub\QWAK\Notebook\Output\\"+f"Search{plotName}")
    # plt.clf()


def taylor_series_approximation(n, num_terms):
    approx = 0
    for i in range(num_terms):
        approx += ((-1) ** i) * (n ** (-2 * i - 2)) / math.factorial(2 * i + 2)
    return approx


def taylor_series_approximation2(n, order):
    taylor_series = 0
    for i in range(order):
        taylor_series += (-1) ** i * sp.binom(order, i) * (1 / n) ** (order - i)
    return taylor_series


def approx_1_over_n_squared(n, order):
    sum = 0
    for i in range(0, order):
        sum += 1 / (n ** (2 + i))
    return sum

colors = ['r','b','g','k']
lines = ['-','-','-','-']
lines2 = ['--','--','--','--']
configVec = zip(colors,lines,lines2)

n = 10
graph = nx.hypercube_graph(n)
gamma = (1 / n) + approx_1_over_n_squared(n, 20)

N = len(graph)
markedSearch = [(N//2,-1)]
initCond = list(range(0, len(graph)))

qw = QWAK(graph=graph, gamma=gamma, markedElements=markedSearch, laplacian=False)
timeList = np.linspace(0, (np.pi / (2) * np.sqrt(N)), 20)

qw.runMultipleWalks(timeList = timeList, initStateList=initCond)
markedProbList = searchProbStepsPlotting(qw)

plotSearch2([markedSearch],[markedProbList],[timeList],configVec)
plt.show()
