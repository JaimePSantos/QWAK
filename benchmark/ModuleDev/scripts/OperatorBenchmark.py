import networkx as nx
from scipy import linalg as ln
import numpy as np
import os
import pstats

from Profiler import profile,find_exact_profiling_file
from qwak.Operator import Operator as Operator
from qwak_cupy.Operator import Operator as COperator
from qwak_cupy.qwak import QWAK as CQWAK
from qwak.qwak import QWAK as QWAK

class OperatorBenchmark:
    def __init__(self, graph, tracked_attributes=None):
        self.graph = graph
        self.n = len(graph)
        self.tracked_attributes = tracked_attributes or ['n', 'init_time', 'walk_time']
        self.init_time = 0.0
        self.walk_time = 0.0

    @profile(
        output_path="operator_results",
        sort_by="cumulative",
        lines_to_print=None,
        strip_dirs=False,
        csv=False,
        tracked_attributes=["n"],  # ✅ Ensure tracking
        benchmark=True  # ✅ Ensure profiling decorator runs
    )
    def init_operator(self, graph=nx.cycle_graph(1), hpc=False):
        if hpc:
            self.operator = COperator(graph)
        else:
            self.operator = Operator(graph)

    def load_files(self, method_name: str):
        """Finds the profiling file for the given method dynamically."""
        if not hasattr(self, method_name):
            raise AttributeError(f"Method {method_name} not found in {self.__class__.__name__}")

        method = getattr(self, method_name)

        # ✅ Check if the method has profiling config
        if not hasattr(method, "_profile_config"):
            raise ValueError(f"Method {method_name} was not decorated with @profile")

        try:
            profiling_file = find_exact_profiling_file(self, method)
            print(f"Profiling file found: {profiling_file}")
            return profiling_file
        except FileNotFoundError as e:
            print(e)
            return None
