import os
from Tools.QwakBenchmarkStub import QWAKBenchmark
import networkx as nx
from matplotlib import pyplot as plt

retval = os.getcwd()
os.chdir(retval + "\\TestOutput\\Profiling\\")


def removeFiles(path):
    for folder in os.listdir(path):
        for file_name in os.listdir(folder):
            # construct full file path
            file = os.path.join(folder, file_name)
            if os.path.isfile(file):
                print('Deleting file:', file)
                try:
                    os.remove(file)
                except OSError as e:  # name the Exception `e`
                    print("Failed with:", e.strerror)  # look what it says
                    print("Error code:", e.code)


def runQwakProfiler(graph, t, marked, k0, k1):
    qwController = QWAKBenchmark(graph, laplacian=False)
    qwController.runWalk(t, marked)
    qwController.getMean()
    qwController.getSndMoment()
    qwController.getStDev()
    qwController.getSurvivalProb(k0, k1)
    qwController.getInversePartRatio()


def runMultipleQwakProfilers(N, t, marked, samples):
    for s in range(samples):
        graph = nx.cycle_graph(N)
        runQwakProfiler(graph, t, marked, 0, 1)

def unmarshallFile(fileName, filePath,timeDict):
    os.chdir(filePath)
    numberOfEntries = 0
    with open(fileName) as f:
        lines = f.readlines()
        for line in lines:
            if len(line) < 6 or "ncalls" in line:
                continue
            elif "Next Entry" in line:
                numberOfEntries += 1
                continue
            else:
                l = line.split(",")
                if numberOfEntries < 1:
                    timeDict[l[5]] = float(l[1])
                else:
                    if l[5] not in timeDict:
                        continue
                    timeDict[l[5]] += float(l[1])
    return timeDict, numberOfEntries

def createTimeDicts(N, t, marked, samples,fileName,filePath):
    timeDict = {}
    timeDictDict = {}
    if type(N) is list:
        for n in N:
            print(n)
            runMultipleQwakProfilers(n,t,marked,samples)
            timeDict,numberOfEntries = unmarshallFile(fileName,filePath,timeDict)
            timeDictDict[n] = normalizeTimeDict(timeDict,numberOfEntries)
            timeDict = {}
    else:
        timeDict, numberOfEntries = unmarshallFile(fileName, filePath,timeDict)
        timeDictDict[N] =  normalizeTimeDict(timeDict,numberOfEntries)
    return timeDictDict

def normalizeTimeDict(timeDict, entryCount):
    for e in timeDict:
        timeDict[e] = timeDict[e] / entryCount
    return timeDict


n = 1000
t = 10
graph = nx.cycle_graph(n)
marked = [0]
k0 = 19
k1 = 21
samples = 1
N = list(range(2,n))

filePath = "qwak/"
initFileName = "__init__.prof"

# removeFiles(os.curdir)
# multipleDicts = createTimeDicts(N, t, marked, samples,initFileName,filePath)
# with open("initTimeDict", 'a+') as f:
#     f.write(str(multipleDicts))

os.chdir(filePath)
with open("initTimeDict", 'r+') as f:
    lines = f.readlines()
    for line in lines:
        multipleDicts = eval(line)

nodes = list(multipleDicts.keys())
eighTime = list(multipleDicts.values())
eighTimeList = []
for i in range(len(eighTime)):
    eighTimeList.append(eighTime[i]['linalg.py:1324(eigh)\n'])

plt.plot(nodes,eighTimeList)
plt.show()