import numpy as np
import matplotlib as mpl
from matplotlib import pyplot as plt
from qwak.qwak import QWAK
from qwak.Errors import EmptyProbDistList

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
    probDistList  = qwak.getProbDistList()
    if probDistList == []:
        raise EmptyProbDistList("The probability distribution list is empty.")
    for probDist in probDistList:
        for element in markdElements:
            markedProbability += probDist.searchNodeProbability(element[0])
        markedProbDistList.append(markedProbability)
        markedProbability = 0
    return markedProbDistList

def searchProbStepsPlotting2(qwak: QWAK,probDistList):
    """Plots the probability of finding the target as a function of the number of steps.

    Parameters
    ----------
    qwak : QWAK
        QWAK object containing the results of the simulation.
    """
    markedProbability = 0
    markedProbDistList = []
    markdElements = qwak.getMarkedElements()
    probDistList  = probDistList
    if probDistList == []:
        raise EmptyProbDistList("The probability distribution list is empty.")
    for probDist in probDistList:
        for element in markdElements:
            markedProbability += probDist.searchNodeProbability(element[0])
        markedProbDistList.append(markedProbability)
        markedProbability = 0
    # print(markedProbDistList)
    return markedProbDistList