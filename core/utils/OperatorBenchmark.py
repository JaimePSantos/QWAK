import networkx as nx
from scipy import linalg
import numpy as np

from utils.Profiler import profile
from qwak.Operator import Operator

linesToPrint = 15
sortBy = "tottime"
outPath = "operator/"
stripDirs = True
csv = True

class OperatorBenchmark:
    @profile(
        output_path=outPath,
        sort_by=sortBy,
        lines_to_print=linesToPrint,
        strip_dirs=stripDirs,
        csv=csv,
    )
    def __init__(
        self, graph: nx.Graph, laplacian: bool = False, markedSearch=None
    ) -> None:
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
        pass

    @profile(
        output_path=outPath,
        sort_by=sortBy,
        lines_to_print=linesToPrint,
        strip_dirs=stripDirs,
        csv=csv,
    )
    def buildDiagonalOperator(self, graph: nx.Graph, laplacian: bool = False, markedSearch=None,time: float = 0) -> None:
        self.operator = Operator(graph, laplacian, markedSearch)
        self.operator.buildDiagonalOperator(time)

    @profile(
        output_path=outPath,
        sort_by=sortBy,
        lines_to_print=linesToPrint,
        strip_dirs=stripDirs,
        csv=csv,
    )
    def buildSlowDiagonalOperator(self,graph: nx.Graph, laplacian: bool = False, markedSearch=None, time: float = 0) -> None:
        self._adjacencyMatrix = np.asarray(nx.laplacian_matrix(graph).todense().astype(complex))
        self.slowperator = linalg.expm(-1j*self._adjacencyMatrix*time)