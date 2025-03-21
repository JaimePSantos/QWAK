import networkx as nx
from scipy import linalg as ln
import numpy as np
import os
import pstats

from Profiler import profile, find_all_profiling_files
from qwak.Operator import Operator as Operator
from qwak_cupy.Operator import Operator as COperator
from qwak_cupy.qwak import QWAK as CQWAK
from qwak.qwak import QWAK as QWAK


class OperatorBenchmark_HPC:
    def __init__(self, tracked_attributes=None):
        self.time = 0
        self.graph = nx.cycle_graph(1)
        self.tracked_attributes = tracked_attributes or ['n']
        self.init_duration = 0.0
        self.walk_duration = 0.0
        self.sample = 0
        self.n = 0

    @profile(
        output_path="operator_results_hpc",
        sort_by="cumulative",
        lines_to_print=None,
        strip_dirs=False,
        csv=False,
        tracked_attributes=[
            'n',
            'sample',
            'pVal',
            'seed'],
        # ✅ Ensure tracking
        benchmark=True  # ✅ Ensure profiling decorator runs
    )
    def init_operator(
            self,
            graph,
            sample=None,
            hpc=False,
            pVal=0.8,
            seed=10):
        self.graph = graph
        self.n = len(graph)
        if sample is not None:
            self.sample = sample
        self.operator = COperator(self.graph)

    @profile(
        output_path="operator_results_hpc",
        sort_by="cumulative",
        lines_to_print=None,
        strip_dirs=False,
        csv=False,
        tracked_attributes=[
            'n',
            'sample',
            'pVal',
            'seed'],
        # ✅ Ensure tracking
        benchmark=True  # ✅ Ensure profiling decorator runs
    )
    def build_operator(self, time=0, sample=None, pVal=0.8, seed=10):
        if sample is not None:
            self.sample = sample
        self.operator.buildDiagonalOperator(time=time)

    @profile(
        output_path="operator_results_hpc",
        sort_by="cumulative",
        lines_to_print=None,
        strip_dirs=False,
        csv=False,
        tracked_attributes=[
            'n',
            'sample',
            'pVal',
            'seed'],
        # ✅ Ensure tracking
        benchmark=True  # ✅ Ensure profiling decorator runs
    )
    def build_expm_operator(
            self,
            time=0,
            sample=None,
            pVal=0.8,
            seed=10):
        if sample is not None:
            self.sample = sample
        self.operator.buildExpmOperator(time=time)

    def load_files2(self, method_name: str):
        """Finds the profiling file for the given method dynamically."""
        if not hasattr(self, method_name):
            raise AttributeError(
                f"Method {method_name} not found in {
                    self.__class__.__name__}")

        method = getattr(self, method_name)

        # ✅ Check if the method has profiling config
        if not hasattr(method, "_profile_config"):
            raise ValueError(
                f"Method {method_name} was not decorated with @profile")

        try:
            # profiling_file = find_exact_profiling_file(self, method)
            profiling_file = find_all_profiling_files(self, method)
            print(f"Profiling file found: {profiling_file}")
            return profiling_file
        except FileNotFoundError as e:
            print(e)
            return None

    def load_files(self, method_name: str):
        """Loads the profiling data for all the files associated with the given method."""
        if not hasattr(self, method_name):
            raise AttributeError(
                f"Method {method_name} not found in {
                    self.__class__.__name__}")

        method = getattr(self, method_name)

        # ✅ Check if the method has profiling config
        if not hasattr(method, "_profile_config"):
            raise ValueError(
                f"Method {method_name} was not decorated with @profile")

        try:
            profiling_files = find_all_profiling_files(self, method)
            all_data = []
            for file_path in profiling_files:
                with open(file_path, "r") as f:
                    data = f.read()
                    all_data.append(data)
            print(f"Loaded profiling data from files: {
                  profiling_files}")
            return all_data
        except FileNotFoundError as e:
            print(e)
            return None
