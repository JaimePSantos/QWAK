import networkx as nx
from scipy import linalg as ln
import numpy as np
import os

from Profiler import profile
from qwak.Operator import Operator
from qwak_cupy.qwak import QWAK as CQWAK
from qwak.qwak import QWAK as QWAK

# linesToPrint = 15
# sortBy = "tottime"
# outPath = "operator/"
# stripDirs = True
# csv = True

# # Ensure the output directory exists
# os.makedirs(outPath, exist_ok=True)

class OperatorBenchmark:
    def __init__(self, graph):
        self.init_time = 0
        self.walk_time = 0
        self.time_list = []

    @profile(
        output_path="operator_results",
        sort_by="cumulative",
        lines_to_print=None,
        strip_dirs=False,
        csv=False,
        time_attributes=['init_time', 'walk_time']  # Attributes to use in path/name
    )
    def init_operator(self, graph, hpc=False):
        # Your initialization logic
        self.init_time = 1.2345  # Example value
        self.walk_time = 6.7890  # Example value
        if hpc:
            self.operator = CQWAK(graph)
        else:
            self.operator = QWAK(graph)

    def load_operator():
        pass
    
    def get_walk_time(self):
        return self.time
    
    def set_walk_time(self, new_time):
        self.time = new_time
    
    
        