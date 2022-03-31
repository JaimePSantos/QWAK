import os
from QuantumWalkTest.QwakBenchmarkStub import QWAKBenchmark
import networkx as nx


retval = os.getcwd()
os.chdir(retval + "\\TestOutput\\Profiling\\")

def runQwakProfiler(graph,t,marked,k0,k1):
    qwController = QWAKBenchmark(graph, laplacian=False)
    qwController.runWalk(t, marked)
    qwController.getMean()
    qwController.getSndMoment()
    qwController.getStDev()
    qwController.getSurvivalProb(k0, k1)
    qwController.getInversePartRatio()

def unmarshallFile(fileName, filePath):
    os.chdir(filePath)
    timeDict = {}
    multipleEntries = 0
    with open(fileName) as f:
        lines = f.readlines()
        for line in lines:
            if len(line) < 6 or "ncalls" in line:
                continue
            elif "Next Entry" in line:
                multipleEntries += 1
                continue
            else:
                l = line.split(",")
                if multipleEntries < 1:
                    timeDict[l[5]] = float(l[1])
                else:
                    if l[5] not in timeDict:
                        continue
                    timeDict[l[5]] += float(l[1])

    return timeDict

n = 1000
t = 10
graph = nx.cycle_graph(n)
marked = [20]
k0 = 19
k1 = 21

runQwakProfiler(graph,t,marked,k0,k1)
timeDict = unmarshallFile("__init__.prof", "qwak/")
print(timeDict)
