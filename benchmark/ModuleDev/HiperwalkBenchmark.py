import networkx as nx
from scipy import linalg as ln
import numpy as np
import os
import pstats

from Profiler import profile,find_all_profiling_files

import hiperwalk as hpw


class HiperwalkBenchmark:
    def __init__(self,  tracked_attributes=None):
        self.time = 0
        self.graph = hpw.Graph(nx.to_numpy_array(nx.cycle_graph(1)))
        self.tracked_attributes = tracked_attributes or ['n']
        self.init_duration = 0.0
        self.walk_duration = 0.0
        self.sample=0
        self.n = 0

    @profile(
        output_path="hiperwalk_results",
        sort_by="cumulative",
        lines_to_print=None,
        strip_dirs=False,
        csv=False,
        tracked_attributes=['n', 'sample', 'pVal', 'seed'],  # ✅ Ensure tracking
        benchmark=True  # ✅ Ensure profiling decorator runs
    )
    def init_hiperwalk(self,graph,time,sample=None, hpc=False,pVal=0.8,seed=10):
        self.graph = hpw.Graph(nx.to_numpy_array(graph))
        self.n = len(graph)
        if sample is not None:
            self.sample = sample
        self.hiperwalk = hpw.ContinuousTime(graph=self.graph, gamma=1/(2*np.sqrt(2)),time=time)
        self.state = self.hiperwalk.ket(self.n//2)

    @profile(
        output_path="hiperwalk_results",
        sort_by="cumulative",
        lines_to_print=None,
        strip_dirs=False,
        csv=False,
        tracked_attributes=['n', 'sample', 'pVal', 'seed'],  # ✅ Ensure tracking
        benchmark=True  # ✅ Ensure profiling decorator runs
    )
    def simulate(self,time=0,sample=None,pVal=0.8,seed=10):
        if sample is not None:
            self.sample = sample
        self.final_state = self.hiperwalk.simulate(range=(self.n//2,(self.n//2)+1), state=self.state)
        
        
    def load_files(self, method_name: str):
        """Loads the profiling data for all the files associated with the given method."""
        if not hasattr(self, method_name):
            raise AttributeError(f"Method {method_name} not found in {self.__class__.__name__}")

        method = getattr(self, method_name)

        # ✅ Check if the method has profiling config
        if not hasattr(method, "_profile_config"):
            raise ValueError(f"Method {method_name} was not decorated with @profile")

        try:
            profiling_files = find_all_profiling_files(self, method)
            all_data = []
            for file_path in profiling_files:
                with open(file_path, "r") as f:
                    data = f.read()
                    all_data.append(data)
            print(f"Loaded profiling data from files: {profiling_files}")
            return all_data
        except FileNotFoundError as e:
            print(e)
            return None
