import networkx as nx
from scipy import linalg as ln
import numpy as np
import os
import pstats

from Profiler import profile
from qwak.Operator import Operator as Operator
from qwak_cupy.Operator import Operator as COperator
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
    def __init__(self, graph, tracked_attributes=None):
        self.init_time = 0
        self.walk_time = 0
        self.time_list = []
        self.graph = graph
        self.n = len(graph)
        
        # Configure tracking
        self.tracked_attributes = tracked_attributes or ['n','walk_time']
        
        # Generate path strings during initialization
        self.profile_directory = self._get_profile_directory()
        self.profile_filename = self._get_profile_filename()
        self.full_profile_path = os.path.join(self.profile_directory, self.profile_filename)
        print(self.full_profile_path )

    def _format_attribute_value(self, value):
        """Replicate the profiler's value formatting"""
        if isinstance(value, float):
            return f"{value:.4f}".replace('.', '_')
        return str(value).replace('.', '_')

    def _get_profile_directory(self):
        """Replicate directory structure logic from profiler"""
        if not self.tracked_attributes:
            return ""

        first_attr = self.tracked_attributes[0]
        value = getattr(self, first_attr, "")
        formatted_value = self._format_attribute_value(value)
        
        return os.path.join(
            "TestOutput",
            "Profiling",
            "operator_results",
            f"{first_attr}_{formatted_value}"
        )

    def _get_profile_filename(self):
        """Replicate filename logic from profiler"""
        parts = []
        for attr in self.tracked_attributes:
            value = getattr(self, attr, None)
            if value is not None:
                formatted = self._format_attribute_value(value)
                parts.append(f"{attr}_{formatted}")
                
        attr_str = '_'.join(parts)
        return f"init_operator-{attr_str}_.prof"

    @profile(
        output_path="operator_results",
        sort_by="cumulative",
        lines_to_print=None,
        strip_dirs=False,
        csv=False,
        tracked_attributes=['n']  # Attributes to use in path/name
    )
    def init_operator(self, graph=nx.cycle_graph(1), hpc=False):
        # Your initialization logic
        if hpc:
            self.operator = COperator(graph)
        else:
            self.operator = Operator(graph)

    def unmarshallFile(fileName, filePath):
        pass
        # numberOfEntries = 0
        # timeDict = {}
        # timeDictDict = []
        # n = 197
        # with open(fileName) as f:
        #     lines = f.readlines()
        #     for line in lines:
        #         if len(line) < 5 or "ncalls" in line:
        #             continue
        #         else:
        #             if "Next Entry" in line:
        #                 timeDictDict.append(timeDict)
        #                 n += 1
        #                 timeDict = {}
        #             else:
        #                 l = line.split(",")
        #                 timeDict[l[5]] = float(l[1])
        # return timeDict, numberOfEntries, timeDictDict

    def get_init_time(self):
        return self.init_time
    
    def get_walk_time(self):
        return self.time
    
    def set_walk_time(self, new_time):
        self.time = new_time
    
    
        