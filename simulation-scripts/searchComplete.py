import networkx as nx
from matplotlib import pyplot as plt
import numpy as np
import math
import scipy.special as sp
from scipy.linalg import expm
from utils.plotTools import searchProbStepsPlotting,searchProbStepsPlotting2
import copy

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


def plotSearch2(markedList, probT, tSpace, configVec, labels):
    plotName = ""
    fig = plt.figure()
    for T, walk, config, marked, label in zip(tSpace, probT, configVec, markedList, labels):
        plt.plot(T, walk, color=config[0], linestyle=config[1], label=label)
        plt.vlines(max(T), 0, max(probT[0]), color=config[0], linestyle=config[2])
        plt.legend()
        plt.xlabel("Time")
        plt.ylabel("Probability of marked elements")
    for marked in markedList:
        plotName += '_' + str(len(marked))
    return fig


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

def init(N):
    psi0 = np.ones((N, 1)) / np.sqrt(N)
    return psi0


def adjMatrix(N):
    adjM = np.ones((N, N), dtype='complex') - np.eye(N)
    return adjM


def hamiltonean(N, adjM, marked, gamma):
    H = -(gamma * adjM)
    H[marked][marked] = -1
    return H


def evo(H, t):
    U = expm(-1j * H * t)
    return U


def fin(N, evo):
    psiN = init(N)
    psiN = evo.dot(psiN)
    return psiN


def ampToProb(N, psiN, marked):
    prob = np.zeros((N, 1))
    probMarked = np.zeros((N, 1))
    for x in range(N):
        prob[x] += (np.absolute(psiN[x]) ** 2)
        probMarked[x] += (np.absolute(psiN[marked]) ** 2)
    return prob, probMarked

n=50
markedSearch = [(x,-1) for x in range(1,n//16)]
t = (np.pi/2) * np.sqrt(n/len(markedSearch))

gamma = 1/n
initCond = list(range(0,n))
graph = nx.complete_graph(n)

timeList = [ x for x in np.linspace(0,t,50)]

qw = QWAK(graph=graph,gamma=gamma,markedElements=markedSearch,laplacian=True)
qw.runMultipleWalks(timeList=timeList,initStateList=initCond)
markedProbList = searchProbStepsPlotting(qw)

######

markedSearch2 = [(x,-1) for x in range(1,n//8)]

t = (np.pi/2) * np.sqrt(n/len(markedSearch2))
gamma = 1/n
initCond = list(range(0,n))
graph = nx.complete_graph(n)

timeList2 = [ x for x in np.linspace(0,t,50)]

qw2 = QWAK(graph=graph,gamma=gamma,markedElements=markedSearch2,laplacian=True)
qw2.runMultipleWalks(timeList=timeList2,initStateList=initCond)
markedProbList2 = searchProbStepsPlotting(qw2)

########

markedSearch3 = [(x,-1) for x in range(1,n//4)]

t = (np.pi/2) * np.sqrt(n/len(markedSearch3))
gamma = 1/n
initCond = list(range(0,n))
graph = nx.complete_graph(n)

timeList3 = [ x for x in np.linspace(0,t,50)]

qw3 = QWAK(graph=graph,gamma=gamma,markedElements=markedSearch3,laplacian=True)
qw3.runMultipleWalks(timeList=timeList3,initStateList=initCond)
markedProbList3 = searchProbStepsPlotting(qw3)

######

markedSearchList = [markedSearch,markedSearch2,markedSearch3]
markedProbListList = [markedProbList,markedProbList2,markedProbList3]
timeListList = [timeList,timeList2,timeList3]
labelList = [f'{len(markedSearch)} Solutions',f'{len(markedSearch2)} Solutions',f'{len(markedSearch3)} Solutions']

colors = plt.cm.rainbow(np.linspace(0, 1, len(markedSearchList)))
lines = ['-']*len(markedSearchList)
lines2 = ['--']*len(markedSearchList)
configVec = zip(colors,lines,lines2)

plotSearch2(markedSearchList,markedProbListList,timeListList,configVec,labels = labelList)
plt.show()
