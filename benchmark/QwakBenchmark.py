import networkx as nx
from scipy import linalg
import numpy as np

from utils.Profiler import profile
from qwak.qwak import QWAK

linesToPrint = 15
sortBy = "tottime"
outPath = "qwak/"
stripDirs = True
csv = True


class QWAKBenchmark:
    @profile(
        output_path=outPath,
        sort_by=sortBy,
        lines_to_print=linesToPrint,
        strip_dirs=stripDirs,
        csv=csv,
    )
    def __init__(
            self,
            graph: nx.Graph,
            laplacian: bool = False,
            markedSearch=None) -> None:
        """_summary_

        Parameters
        ----------
        graph : nx.Graph
            _description_
        laplacian : bool, optional
            _description_, by default False
        markedSearch : _type_, optional
            _description_, by default None

        Returns
        -------
        _type_
            _description_
        """
        self.qwak = QWAK(graph, laplacian, markedSearch)

    @profile(
        output_path=outPath,
        sort_by=sortBy,
        lines_to_print=linesToPrint,
        strip_dirs=stripDirs,
        csv=csv,
    )
    def runWalk(
            self,
            time: float = 0,
            initStateList: list = [0]) -> None:
        self.qwak.runWalk(time, initStateList)

    @profile(
        output_path=outPath,
        sort_by=sortBy,
        lines_to_print=linesToPrint,
        strip_dirs=stripDirs,
        csv=csv,
    )
    def checkPST(self, nodeA, nodeB):
        nodeA = int(nodeA)
        nodeB = int(nodeB)
        return self.qwak.checkPST(nodeA, nodeB)

    @profile(
        output_path=outPath,
        sort_by=sortBy,
        lines_to_print=linesToPrint,
        strip_dirs=stripDirs,
        csv=csv,
    )
    def transportEfficiency(self):
        return self.qwak.transportEfficiency(
            self._initState.getStateVec())

    @profile(
        output_path=outPath,
        sort_by=sortBy,
        lines_to_print=linesToPrint,
        strip_dirs=stripDirs,
        csv=csv,
    )
    def getMean(self):
        return self.qwak.getMean()

    @profile(
        output_path=outPath,
        sort_by=sortBy,
        lines_to_print=linesToPrint,
        strip_dirs=stripDirs,
        csv=csv,
    )
    def getSndMoment(self):
        return self.qwak.getSndMoment()

    @profile(
        output_path=outPath,
        sort_by=sortBy,
        lines_to_print=linesToPrint,
        strip_dirs=stripDirs,
        csv=csv,
    )
    def getStDev(self):
        return self.qwak.getStDev()

    @profile(
        output_path=outPath,
        sort_by=sortBy,
        lines_to_print=linesToPrint,
        strip_dirs=stripDirs,
        csv=csv,
    )
    def getSurvivalProb(self, k0, k1):
        return self.qwak.getSurvivalProb(k0, k1)

    @profile(
        output_path=outPath,
        sort_by=sortBy,
        lines_to_print=linesToPrint,
        strip_dirs=stripDirs,
        csv=csv,
    )
    def getInversePartRatio(self):
        return self.qwak.getInversePartRatio()
