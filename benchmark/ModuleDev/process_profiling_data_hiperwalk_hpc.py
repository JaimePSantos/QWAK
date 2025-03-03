import networkx as nx

from OperatorBenchmark import OperatorBenchmark

from typing import List, Dict

from scripts import load_profiling_data,create_profiling_data_ER,separate_keys_and_values,git_branch_commit_push,create_profiling_data_ER_HPC

from scripts_old import load_runMultipleSimpleQWAK, load_runMultipleSimpleQWAK_legacy
from datetime import datetime

import os
import re

from utils.plotTools import plot_qwak

import numpy as np
import cupy as cp
from scipy.linalg import inv, expm
import networkx as nx
import time
import cupyx.scipy.linalg as cpx_scipy
from cupyx.profiler import benchmark
from matplotlib import pyplot as plt
import os
import json
import pickle
from tqdm import tqdm
import subprocess
import random
from qwak_cupy.qwak import QWAK as CQWAK
from qwak.qwak import QWAK as QWAK
from datetime import datetime
import shutil


def process_profiling_data(path, method_name, nrange, sample_range, seed=None):
    for n in tqdm(nrange, desc="Processing n-values"):
        cumtimes = []
        for sample in sample_range:
            filename = f"{method_name}-n_{n}_sample_{sample}_pVal_0_8000_seed_{seed}.prof"
            filepath = os.path.join(path, f"n_{n}", filename)
            print(f"Checking for file: {filepath}")
            if not os.path.exists(filepath):
                print(f"ERROR: File not found - {filepath}")
                return
            with open(filepath, 'r') as f:
                next(f)  # Skip the header line
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
                            break
        
        if cumtimes:
            average_cumtime = sum(cumtimes) / len(cumtimes)
            avg_folder = os.path.join(path, f"n_{n}_avg")
            os.makedirs(avg_folder, exist_ok=True)
            avg_filename = f"AVG-{method_name}-n_{n}_seed_{seed}.prof"
            avg_filepath = os.path.join(avg_folder, avg_filename)
            with open(avg_filepath, 'w') as avg_file:
                avg_file.write(f"{average_cumtime}\n")

def load_profiling_averages(path, method_name, nrange, seed=None):
    results = {}
    for n in tqdm(nrange, desc="Loading average times"):
        avg_folder = os.path.join(path, f"n_{n}_avg")
        avg_filename = f"AVG-{method_name}-n_{n}_seed_{seed}.prof"
        avg_filepath = os.path.join(avg_folder, avg_filename)
        try:
            with open(avg_filepath, 'r') as avg_file:
                results[n] = float(avg_file.readline().strip())
        except (FileNotFoundError, ValueError):
            raise ValueError(f"Average file not found or invalid format: {avg_filepath}")
    return results


nMin = 3
nMax = 1000 
n_values = list(range(nMin, nMax, 1))
pVal = 0.8
sample_range = range(0, 35, 1)
seed = 10


SCRIPT_DIR = os.getcwd()
path = os.path.normpath(os.path.join(
    SCRIPT_DIR,
    "benchmark/ModuleDev/Profiling/hiperwalk_results_hpc"
))



# def delete_n_folders(path, nrange):
#     for n in tqdm(nrange, desc="Deleting n_x folders"):
#         folder_path = os.path.join(path, f"n_{n}_avg")
#         if os.path.exists(folder_path) and os.path.isdir(folder_path):
#             shutil.rmtree(folder_path)
# delete_n_folders(path,n_values)
# print(f"Using base path: {path}")

process_profiling_data(
    path=path,
    method_name="init_hiperwalk",
    nrange=n_values,
    sample_range=sample_range,  # Assuming samples 0-9
    seed=seed
)

process_profiling_data(
    path=path,
    method_name="simulate",
    nrange=n_values,
    sample_range=sample_range,  # Assuming samples 0-9
    seed=seed
)

