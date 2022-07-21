import networkx as nx

from utils.QwakBenchmark import QWAKBenchmark
from OperatorBenchmark import OperatorBenchmark

if __name__ == "__main__":
    n = 1000
    t = 10
    graph = nx.cycle_graph(n)
    marked = [20]

    # qwController = QWAKBenchmark(graph, laplacian=False)
    # qwController.runWalk(t, marked)
    # qwController.getMean()
    # qwController.getSndMoment()
    # qwController.getStDev()
    # qwController.getSurvivalProb(19, 21)
    # qwController.getInversePartRatio()

    qwOperator = OperatorBenchmark()
    qwOperator.buildDiagonalOperator(graph,time=t)
    qwOperator.buildSlowDiagonalOperator(graph,time=t)