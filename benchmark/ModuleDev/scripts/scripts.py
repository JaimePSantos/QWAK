import networkx as nx

from OperatorBenchmark import OperatorBenchmark

from typing import List, Dict

from Profiler import profile,find_exact_profiling_file,find_all_profiling_files
import os
import re
import os
import cProfile
import pstats
from functools import wraps
from io import StringIO
from tqdm import tqdm
from typing import Callable, List
import inspect



def run_if_not_profiled(instance, method_name: str, **kwargs):
    """
    Checks if a profiling file exists for the method (using the current tracked attributes)
    and if not, runs the method with the provided kwargs.
    
    Args:
        instance: The instance containing the method.
        method_name (str): Name of the method to run.
        **kwargs: Keyword arguments that are passed to the method.
    """
    # Update instance attributes with the given kwargs.
    for key, value in kwargs.items():
        setattr(instance, key, value)
    
    # If 'graph' is provided, update 'n' accordingly since 'n' is used in the filename.
    if 'graph' in kwargs:
        setattr(instance, 'n', len(kwargs['graph']))
    
    method = getattr(instance, method_name)
    try:
        existing_file = find_exact_profiling_file(instance, method)
        print(f"Profiling file '{existing_file}' already exists for method '{method_name}' with sample {instance.sample}. Skipping execution.")
    except FileNotFoundError:
        print(f"Profiling file not found for method '{method_name}' with sample {instance.sample}. Running execution.")
        method(**kwargs)

def create_profiling_data(n_values: List[int], sample_range=range(0, 3), t: int = 10):
    """
    Runs profiling for a variable number of n's, ensuring that profiling files are created if they do not exist.
    
    Args:
        n_values (List[int]): List of n values (graph sizes) to run profiling for.
        sample_range (iterable, optional): Range of sample indices to run. Defaults to range(0, 3).
        t (int, optional): The time parameter to pass to build_operator. Defaults to 10.
    """
    for n in n_values:
        print(f"Creating profiling data for n = {n}")
        bench = OperatorBenchmark(tracked_attributes=['n', 'sample'])
        graph = nx.cycle_graph(n)

        for sample in sample_range:
            run_if_not_profiled(bench, "init_operator", graph=graph, sample=sample)
            run_if_not_profiled(bench, "build_operator", time=t, sample=sample)

def load_profiling_data(path, method_name, nrange, sample_range):
    results = {}
    for n in nrange:
        cumtimes = []
        for sample in sample_range:
            filename = f"{method_name}-n_{n}_sample_{sample}.prof"
            # Include the n_{n} directory in the file path
            filepath = os.path.join(path, f"n_{n}", filename)
            with open(filepath, 'r') as f:
                next(f)  # Skip the header line
                found = False
                for line in f:
                    line = line.strip()
                    if not line:
                        continue
                    parts = line.split()
                    if len(parts) < 6:
                        continue
                    try:
                        cumtime = float(parts[3])
                    except (IndexError, ValueError):
                        continue
                    func_part = ' '.join(parts[5:])
                    if '(' in func_part and ')' in func_part:
                        func_name = func_part.split('(')[-1].split(')')[0]
                        if func_name == method_name:
                            cumtimes.append(cumtime)
                            found = True
                            break
                if not found:
                    raise ValueError(f"Method '{method_name}' not found in {filepath}")
        average_cumtime = sum(cumtimes) / len(cumtimes)
        results[n] = average_cumtime
    return results