import networkx as nx

from Tools.QwakBenchmarkStub import QWAKBenchmark

if __name__ == "__main__":
    n = 1000
    t = 10
    graph = nx.cycle_graph(n)
    marked = [20]

    qwController = QWAKBenchmark(graph, laplacian=False)
    qwController.runWalk(t, marked)
    qwController.getMean()
    qwController.getSndMoment()
    qwController.getStDev()
    qwController.getSurvivalProb(19, 21)
    qwController.getInversePartRatio()
