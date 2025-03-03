import networkx as nx

from OperatorBenchmark import OperatorBenchmark
from OperatorBenchmark_HPC import OperatorBenchmark_HPC
from HiperwalkBenchmark import HiperwalkBenchmark

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
import subprocess




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

def create_profiling_data_cycle(n_values: List[int], sample_range=range(0, 3), t: int = 10):
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

def create_profiling_data_ER(n_values: List[int], sample_range=range(0, 3), t: int = 10, pVal=0.8, seed = 10):
    """
    Runs profiling for a variable number of n's, ensuring that profiling files are created if they do not exist.
    
    Args:
        n_values (List[int]): List of n values (graph sizes) to run profiling for.
        sample_range (iterable, optional): Range of sample indices to run. Defaults to range(0, 3).
        t (int, optional): The time parameter to pass to build_operator. Defaults to 10.
    """
    for n in n_values:
        print(f"Creating profiling data for n = {n}")
        bench = OperatorBenchmark(tracked_attributes=['n', 'sample', 'pVal', 'seed'])
        graph = nx.erdos_renyi_graph(n,pVal,seed=seed)

        for sample in sample_range:
            run_if_not_profiled(bench, "init_operator", graph=graph, sample=sample,pVal=pVal,seed=seed)
            run_if_not_profiled(bench, "build_operator", time=t, sample=sample,pVal=pVal,seed=seed)
            run_if_not_profiled(bench, "build_expm_operator", time=t, sample=sample,pVal=pVal,seed=seed)

def create_profiling_data_ER_HPC(n_values: List[int], sample_range=range(0, 3), t: int = 10, pVal=0.8, seed = 10):
    """
    Runs profiling for a variable number of n's, ensuring that profiling files are created if they do not exist.
    
    Args:
        n_values (List[int]): List of n values (graph sizes) to run profiling for.
        sample_range (iterable, optional): Range of sample indices to run. Defaults to range(0, 3).
        t (int, optional): The time parameter to pass to build_operator. Defaults to 10.
    """
    for n in n_values:
        print(f"Creating profiling data for n = {n}")
        bench = OperatorBenchmark_HPC(tracked_attributes=['n', 'sample', 'pVal', 'seed'])
        graph = nx.erdos_renyi_graph(n,pVal,seed=seed)

        for sample in sample_range:
            run_if_not_profiled(bench, "init_operator", graph=graph, sample=sample,pVal=pVal,seed=seed)
            run_if_not_profiled(bench, "build_operator", time=t, sample=sample,pVal=pVal,seed=seed)
            run_if_not_profiled(bench, "build_expm_operator", time=t, sample=sample,pVal=pVal,seed=seed)

def create_profiling_data_hiperwalk(n_values: List[int], sample_range=range(0, 3), t: int = 10, pVal=0.8, seed = 10):
    """
    Runs profiling for a variable number of n's, ensuring that profiling files are created if they do not exist.
    
    Args:
        n_values (List[int]): List of n values (graph sizes) to run profiling for.
        sample_range (iterable, optional): Range of sample indices to run. Defaults to range(0, 3).
        t (int, optional): The time parameter to pass to build_operator. Defaults to 10.
    """
    for n in n_values:
        print(f"Creating profiling data for n = {n}")
        bench = HiperwalkBenchmark(tracked_attributes=['n', 'sample', 'pVal', 'seed'])
        graph = nx.erdos_renyi_graph(n,pVal,seed=seed)

        for sample in sample_range:
            run_if_not_profiled(bench, "init_hiperwalk", graph=graph,time=t, sample=sample,pVal=pVal,seed=seed)
            run_if_not_profiled(bench, "simulate", time=t, sample=sample,pVal=pVal,seed=seed)

def run_if_not_profiled_time_range(instance, method_name: str, time_range: List[int], **kwargs):
    """
    Checks if a profiling file exists for a given time value (using the current tracked attributes)
    and if not, runs the method with the provided kwargs for each time value in time_range.
    
    Args:
        instance: The instance containing the method.
        method_name (str): Name of the method to run.
        time_range (List[int]): List of time values to iterate over.
        **kwargs: Additional keyword arguments passed to the method.
    """
    for t in time_range:
        # Set the instance's time attribute and ensure it's in kwargs.
        setattr(instance, 't', t)
        kwargs['time'] = t
        
        # If 'graph' is provided, update 'n' accordingly since 'n' is used in the filename.
        if 'graph' in kwargs:
            setattr(instance, 'n', len(kwargs['graph']))
        
        method = getattr(instance, method_name)
        try:
            existing_file = find_exact_profiling_file(instance, method)
            print(f"Profiling file '{existing_file}' already exists for method '{method_name}' with time {t} and sample {instance.sample}. Skipping execution.")
        except FileNotFoundError:
            print(f"Profiling file not found for method '{method_name}' with time {t} and sample {instance.sample}. Running execution.")
            method(**kwargs)

def create_profiling_data_animation(time_range: List[int], sample_range=range(0, 3), n: int = 10, pVal=0.8, seed = 10):
    """
    Runs profiling for a variable number of n's, ensuring that profiling files are created if they do not exist.
    
    Args:
        n_values (List[int]): List of n values (graph sizes) to run profiling for.
        sample_range (iterable, optional): Range of sample indices to run. Defaults to range(0, 3).
        t (int, optional): The time parameter to pass to build_operator. Defaults to 10.
    """

    for t in time_range:
        print(f"Creating profiling data for t = {t}")
        bench = OperatorBenchmark(tracked_attributes=['t', 'sample', 'pVal', 'seed'])
        graph = nx.erdos_renyi_graph(n,pVal,seed=seed)
        bench.init_operator_untimed(graph=graph,pVal=pVal,seed=seed)
        for sample in sample_range:
            run_if_not_profiled(bench, "build_multiple_operators", time_range=time_range, sample=sample,pVal=pVal,seed=seed)
            run_if_not_profiled(bench, "build_multiple_expm_operator", time_range=time_range, sample=sample,pVal=pVal,seed=seed)

def load_profiling_data(path, method_name, nrange, sample_range,pVal=None,seed=None):
    results = {}
    for n in tqdm(nrange, desc="Processing n-values"):
        cumtimes = []
        for sample in sample_range:
            filename = f"{method_name}-n_{n}_sample_{sample}_pVal_0_8000_seed_{seed}.prof"
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

def separate_keys_and_values(input_dict):
    """
    Separates the keys and values of a dictionary into two separate lists.

    :param input_dict: The input dictionary.
    :return: Two lists, one containing the keys and the other containing the values.
    """
    keys = list(input_dict.keys())
    values = list(input_dict.values())
    return keys, values

def git_branch_commit_push(branch_name, commit_message):
    """
    Creates a new git branch, adds changes, commits, and pushes to remote.
    
    :param branch_name: The name of the new branch to create.
    :param commit_message: The commit message to use.
    """
    try:
        # Check current branch
        current_branch = subprocess.check_output(['git', 'branch', '--show-current'], text=True).strip()
        print(f"Current branch: {current_branch}")
        
        # Check for changes
        status_output = subprocess.check_output(['git', 'status', '--porcelain'], text=True).strip()
        if not status_output:
            print("No changes to commit. Exiting.")
            return

        # Create and switch to the new branch
        subprocess.check_call(['git', 'checkout', '-b', branch_name])
        print(f"Switched to new branch: {branch_name}")
        
        # Add changes to the new branch
        subprocess.check_call(['git', 'add', '.'])
        print("Added changes to staging area on the new branch.")
        
        # Commit changes on the new branch
        subprocess.check_call(['git', 'commit', '-m', "PYTHON:"+commit_message])
        print(f"Committed changes with message: {commit_message}")
        
        # Push the new branch to remote
        subprocess.check_call(['git', 'push', '-u', 'origin', branch_name])
        print(f"Pushed branch '{branch_name}' to remote.")
    
    except subprocess.CalledProcessError as e:
        print(f"Error occurred while executing git command: {e}")
    except Exception as ex:
        print(f"An unexpected error occurred: {ex}")