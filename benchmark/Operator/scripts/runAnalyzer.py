import os

import networkx as nx
from matplotlib import pyplot as plt
import numpy as np
import pandas as pd
from scipy.optimize import curve_fit
from scipy.interpolate import interp1d
from scipy.signal import savgol_filter

from QwakBenchmark import QWAKBenchmark
from OperatorBenchmark import OperatorBenchmark

if __name__ == "__main__":
    retval = os.getcwd()
    os.chdir(os.path.join(retval, "TestOutput", "Profiling"))
    qwOperator2 = OperatorBenchmark(nx.cycle_graph(500))

    def removeFiles(path):
        for folder in os.listdir(path):
            for file_name in os.listdir(folder):
                # construct full file path
                file = os.path.join(folder, file_name)
                if os.path.isfile(file):
                    print("Deleting file:", file)
                    try:
                        os.remove(file)
                    except OSError as e:  # name the Exception `e`
                        # look what it says
                        print("Failed with:", e.strerror)
                        print("Error code:", e.code)

    def runQwakProfiler(graph, t, marked, k0, k1):
        qwController = QWAKBenchmark(graph, laplacian=False)
        qwController.runWalk(t, marked)
        qwController.getMean()
        qwController.getSndMoment()
        qwController.getStDev()
        qwController.getSurvivalProb(k0, k1)
        qwController.getInversePartRatio()

    def runOperatorProfiler(graph, t):
        qwOperator = OperatorBenchmark(graph)
        qwOperator.buildDiagonalOperator(graph, time=t)
        qwOperator.buildSlowDiagonalOperator(graph, time=t)

    def runOperatorProfiler2(graph, t):
        global qwOperator2
        qwOperator2.buildDiagonalOperator2(graph, time=t)
        qwOperator2.buildSlowDiagonalOperator(graph, time=t)

    def runMultipleQwakProfilers(N, t, marked, samples):
        for s in range(samples):
            graph = nx.cycle_graph(n)
            runQwakProfiler(graph, t, marked, 0, 1)

    def runMultipleOperatorProfilers(n, t, samples):
        for s in range(samples):
            graph = nx.cycle_graph(n)
            runOperatorProfiler(graph, t)

    def runMultipleOperatorProfilers2(n, t, samples):
        for s in range(samples):
            graph = nx.cycle_graph(n)
            runOperatorProfiler2(graph, t)

    def unmarshallFile(fileName, filePath):
        if (os.getcwd() != "C:\\Users\\jaime\\Documents\\GitHub\\QWAK\\benchmark\\TestOutput\\Profiling\\operator"):
            os.chdir(filePath)
        numberOfEntries = 0
        timeDict = {}
        timeDictDict = []
        n = 197
        with open(fileName) as f:
            lines = f.readlines()
            for line in lines:
                if len(line) < 5 or "ncalls" in line:
                    continue
                else:
                    if "Next Entry" in line:
                        timeDictDict.append(timeDict)
                        n += 1
                        timeDict = {}
                    else:
                        l = line.split(",")
                        timeDict[l[5]] = float(l[1])
        return timeDict, numberOfEntries, timeDictDict

    def createOperatorTimeDicts(
            N,
            samples,
            fileName,
            fileName2,
            filePath):
        if (os.getcwd() != "C:\\Users\\jaime\\Documents\\GitHub\\QWAK\\benchmark\\TestOutput\\Profiling\\operator"):
            os.chdir(filePath)
        timeDict = {}
        timeDict2 = {}
        tempTimeDictDict = []
        tempTimeDictDict2 = []
        timeDictDict = {}
        timeDictDict2 = {}
        if isinstance(N, list):
            for n in N:
                print(f"Running for graph of size: {n}")
                runMultipleOperatorProfilers(n, t, samples)
            timeDict, numberOfEntries, tempTimeDictDict = unmarshallFile(
                fileName, filePath)
            timeDict2, numberOfEntries2, tempTimeDictDict2 = unmarshallFile(
                fileName2, filePath)
            for n, d1, d2 in zip(
                    N, tempTimeDictDict, tempTimeDictDict2):
                timeDictDict[n] = d1
                timeDictDict2[n] = d2
        return timeDictDict, timeDictDict2

    def createOperatorTimeDicts2(
            N,
            time,
            samples,
            fileName,
            fileName2,
            filePath):
        if (os.getcwd() != "C:\\Users\\jaime\\Documents\\GitHub\\QWAK\\benchmark\\TestOutput\\Profiling\\operator"):
            os.chdir(filePath)
        timeDict = {}
        timeDict2 = {}
        tempTimeDictDict = []
        tempTimeDictDict2 = []
        timeDictDict = {}
        timeDictDict2 = {}
        for t in time:
            print(f"Running for time: {t}")
            runMultipleOperatorProfilers2(N, t, samples)
        timeDict, numberOfEntries, tempTimeDictDict = unmarshallFile(
            fileName, filePath)
        timeDict2, numberOfEntries2, tempTimeDictDict2 = unmarshallFile(
            fileName2, filePath)
        for t, d1, d2 in zip(time, tempTimeDictDict, tempTimeDictDict2):
            timeDictDict[t] = d1
            timeDictDict2[t] = d2
        return timeDictDict, timeDictDict2

    def normalizeTimeDict(timeDict, entryCount):
        for e in timeDict:
            timeDict[e] = timeDict[e] / entryCount
        return timeDict

    def getTimeDictFromFile(fileName, filePath):
        if (os.getcwd() != "C:\\Users\\jaime\\Documents\\GitHub\\QWAK\\benchmark\\TestOutput\\Profiling\\operator"):
            os.chdir(filePath)
        with open(fileName, "r+") as f:
            lines = f.readlines()
            for line in lines:
                print(line)
                multipleDicts = eval(line)
        return multipleDicts

    n = 100
    t = 10
    graph = nx.cycle_graph(n)
    marked = [0]
    k0 = 19
    k1 = 21
    samples = 1
    N = list(range(2, 500))
    time = list(range(0, 100))

    filePath = "operator"
    diagonalOperatorFileName = "buildDiagonalOperator.prof"
    diagonalOperatorFileName2 = "buildDiagonalOperator2.prof"
    diagonalSlowperatorFileName = "buildSlowDiagonalOperator.prof"
    diagonalOperatorTimeDictFileName = "DiagonalOperatorTimeDict"
    diagonalOperatorTimeDictFileName2 = "DiagonalOperatorTimeDict2"
    diagonalSlowperatorTimeDictFileName = "DiagonalSlowperatorTimeDict"

    # removeFiles(os.curdir)
    # diagonlOperatorTimeDicts,diagonalSlowperatorTimeDicts = createOperatorTimeDicts2(n,time,samples, diagonalOperatorFileName2,diagonalSlowperatorFileName,filePath)
    # with open(diagonalOperatorTimeDictFileName2, 'a+') as f:
    #     f.write(str(diagonlOperatorTimeDicts))
    # with open(diagonalSlowperatorTimeDictFileName, 'a+') as f:
    #     f.write(str(diagonalSlowperatorTimeDicts))

    # removeFiles(os.curdir)
    # diagonlOperatorTimeDicts,diagonalSlowperatorTimeDicts = createOperatorTimeDicts(N,samples, diagonalOperatorFileName,diagonalSlowperatorFileName,filePath)
    # with open(diagonalOperatorTimeDictFileName, 'a+') as f:
    #     f.write(str(diagonlOperatorTimeDicts))
    # with open(diagonalSlowperatorTimeDictFileName, 'a+') as f:
    #     f.write(str(diagonalSlowperatorTimeDicts))

    diagonlOperatorTimeDicts = getTimeDictFromFile(
        diagonalOperatorTimeDictFileName2, filePath)
    diagonalSlowperatorTimeDicts = getTimeDictFromFile(
        diagonalSlowperatorTimeDictFileName, filePath)
    nodes = list(diagonlOperatorTimeDicts.keys())

    eighTime = list(diagonlOperatorTimeDicts.values())
    eighTimeList = []
    for i in range(len(eighTime)):
        # eighTimeList.append(eighTime[i]["linalg.py:1324(eigh)\n"])
        eighTimeList.append(sum(eighTime[i].values()))
        print(f"Fast: {i} -- {sum(eighTime[i].values())}")

    eighTime2 = list(diagonalSlowperatorTimeDicts.values())
    eighTimeList2 = []
    for i in range(len(eighTime2)):
        # eighTimeList2.append(eighTime2[i]["_basic.py:40(solve)\n"])
        eighTimeList2.append(sum(eighTime2[i].values()))
        print(f"Slow: {i} -- {sum(eighTime2[i].values())}")

    # itp = interp1d(nodes,eighTimeList2, kind='linear',fill_value="interp/extrap")
    # window_size, poly_order = 70, 3
    # xx = np.linspace(min(eighTimeList2), max(eighTimeList2), 298)
    # eighTimeList2 = savgol_filter(eighTimeList2, window_size, poly_order)
    # print(eighTimeList2[-1])
    # eighTimeList2 = savgol_filter(eighTimeList2, 15, 5)
    # print(eighTimeList2)

    series = pd.Series(eighTimeList2)
    eighTimeList2 = series.rolling(5).mean().to_numpy()

    font = {'family': 'sans-serif',
            'size': 12}
    plt.rc('font', **font)
    plt.plot(
        nodes,
        eighTimeList,
        linewidth=1.5,
        color='blue',
        label='Spectral Decomp.')
    plt.plot(
        nodes,
        eighTimeList2,
        linestyle='-.',
        linewidth=1.5,
        color='red',
        label='Matrix exp.')
    plt.xlabel("CTQW Time Evolution")
    plt.ylabel("Execution Time (s)")
    plt.legend()
    plt.show()

    # font = {'family': 'sans-serif',
    #         'size': 12}
    # plt.rc('font', **font)
    # plt.plot(nodes, eighTimeList,linewidth=1.5,color='blue',label='Spectral Decomp.')
    # plt.plot(nodes, eighTimeList2,linestyle='-.',linewidth=1.5,color='red',label = 'Matrix exp.')
    # plt.xlabel("# of Nodes")
    # plt.ylabel("Time (s)")
    # plt.legend()
    # plt.show()

    # filePath = "qwak/"
    # initFileName = "__init__.prof"
    # removeFiles(os.curdir)
    # multipleDicts = createTimeDicts(N, t, marked, samples,initFileName,filePath)
    # with open("initTimeDict", 'a+') as f:
    #     f.write(str(multipleDicts))

    # os.chdir(filePath)
    # with open("initTimeDict", "r+") as f:
    #     lines = f.readlines()
    #     for line in lines:
    #         multipleDicts = eval(line)
    #
    # nodes = list(multipleDicts.keys())
    # eighTime = list(multipleDicts.values())
    # eighTimeList = []
    # for i in range(len(eighTime)):
    #     eighTimeList.append(eighTime[i]["linalg.py:1324(eigh)\n"])
    #
    # plt.plot(nodes, eighTimeList)
    # plt.show()
