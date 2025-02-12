import networkx as nx

from OperatorBenchmark import OperatorBenchmark

if __name__ == "__main__":
    n = 1000
    t = 10
    graph = nx.cycle_graph(n)
    print(nx.cycle_graph.__name__)
    marked = [20]

    # qwController = QWAKBenchmark(graph, laplacian=False)
    # qwController.runWalk(t, marked)
    # qwController.getMean()
    # qwController.getSndMoment()
    # qwController.getStDev()
    # qwController.getSurvivalProb(19, 21)
    # qwController.getInversePartRatio()

    qwOperator = OperatorBenchmark(graph)
    # qwOperator.buildDiagonalOperator(graph, time=t)
    # qwOperator.buildSlowDiagonalOperator(graph, time=t)
    qwOperator.init_operator(graph)
