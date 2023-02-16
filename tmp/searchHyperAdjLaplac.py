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


def plotSearch2(markedList, probT, tSpace, configVec,labels):
    plotName = ""
    print(f'probT: {len(probT)}\t markedList: {len(markedList)}\t tspace: {len(tSpace)}')
    for T, walk, config, marked, label in zip(tSpace, probT, configVec, markedList,labels):
        plt.plot(T, walk, color=config[0], linestyle=config[1], label=label)
        # plt.vlines(max(T), 0, max(probT[0]), color=config[0], linestyle=config[2])
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

def get_cmap(n, name='hsv'):
    '''Returns a function that maps each index in 0, 1, ..., n-1 to a distinct
    RGB color; the keyword argument name must be a standard mpl colormap name.'''
    return plt.cm.get_cmap(name, n)

colors = ['r','b','g','k','c','m','y']
lines = ['-','-','-','-',':',':',':']
lines2 = ['--','--','--','--','--','--','--']
configVec = zip(colors,lines,lines2)


# n = 10
# graph = nx.hypercube_graph(n)
# gamma = (1 / n) + approx_1_over_n_squared(n, 20)
# gammaLapla = (2 / n) + approx_1_over_n_squared(n, 20)
#
# N = len(graph)
# markedSearch = [(N//2,-1)]
# initCond = list(range(0, len(graph)))
#
# qw = QWAK(graph=graph, gamma=gamma, markedElements=markedSearch, laplacian=False)
# qwLapla = QWAK(graph=graph, gamma=gamma, markedElements=markedSearch, laplacian=True)
#
# timeList = np.linspace(0, (np.pi / (2) * np.sqrt(N)), 20)
# timeListLapla = np.linspace(0, (np.pi / (2) * np.sqrt(N)), 20)
#
# qw.runMultipleWalks(timeList = timeList, initStateList=initCond)
# qwLapla.runMultipleWalks(timeList = timeList, initStateList=initCond)
#
# markedProbList = searchProbStepsPlotting(qw)
# markedProbListLapla = searchProbStepsPlotting(qwLapla)
#
# plotSearch2([markedSearch,markedSearch],[markedProbList,markedProbListLapla],[timeList,timeListLapla],configVec,[ "QWAK", "QWAKLapla"])
# plt.show()

n=3
graph = nx.hypercube_graph(n)
# gamma = 1/n + approx_1_over_n_squared(n,10)# Gamma do paper do renato https://arxiv.org/pdf/2212.08889.pdf
# o melhor gamma para n = 10 parece estar entre 0.113 e 0.115
gamma = 0
for k in range(1,n+1):
    gamma += ( math.factorial(n) / (math.factorial(k)*math.factorial(n-k)) ) * 1/k
gamma = gamma * (1/(2**n))/2
# gamma = 1/n

N = len(graph)
print(f'N = {N}')
initCond = list(range(0,len(graph)))

maxFoundGamma = 0.11436917138223161

timeList = np.linspace(0, 2*(np.pi/(2) * np.sqrt(N)),50)
gammaList = [gamma] #+ #np.linspace(gamma,2*gamma ,10).tolist()+ [maxFoundGamma] +
print(f'gammaList = {gammaList} \n gamma = {gamma}' )#-> 0.7880258300395853')
# print(f'(0.7880803569765136, 0.11436917138223161)')
markedProbList = []
markedSearch = []
timeListList = []
labelList = []
probDistList = []

colors = plt.cm.rainbow(np.linspace(0, 1, len(gammaList)))
lines = ['-']*len(gammaList)
lines2 = ['--']*len(gammaList)
configVec = zip(colors,lines,lines2)

for gamma in gammaList:
    qw = QWAK(graph=graph,gamma=gamma,markedElements=[(N//2,-1)],laplacian=False)
    for time in timeList:
        qw.runWalk(time=time,initStateList=initCond)
        probDistList.append(copy.deepcopy(qw.getProbDist()))
    markedProbList.append(searchProbStepsPlotting2(qw,probDistList))
    probDistList = []
    markedSearch.append( [(N//2,-1)])
    timeListList.append( timeList)
    labelList.append(f'{round(gamma,7)}')
    qw.resetWalk()


plotAux = []
plotS = plotSearch2(markedSearch,markedProbList,timeListList,configVec,labelList)
for plot,gamma in zip(markedProbList,gammaList):
    plotAux.append((max(plot),gamma))
    # print(f'gamma = {gamma} -> {plot}')
max_pair = max(plotAux, key=lambda pair: pair[0])
print(max_pair)
plt.show()
