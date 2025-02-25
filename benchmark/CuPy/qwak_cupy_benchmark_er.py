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

def load_list_from_file(file_path):
    with open(file_path, 'r') as file:
        data_str = file.read()
    data = [json.loads(line) for line in data_str.splitlines()]
    return data

def write_list_to_file(file_path, data):
    data_str = [str(item) for item in data]  # Convert float values to strings
    with open(file_path, 'w') as file:
        file.write('\n'.join(data_str))

def runTimedQWAK(n,t,adj):
    start_time = time.time()
    initNodes = [n//2]
    qw = QWAK(nx.from_numpy_array(adj))
    qw.runWalk(t, initNodes)
    end_time = time.time()
    qwak_time = end_time - start_time
    return qw, qwak_time

def runTimedQWAK_cupy(n,t,adj):
    start_time = time.time()
    initNodes = [n//2]
    qw = CQWAK(nx.from_numpy_array(adj))
    qw.runWalk(t, initNodes)
    end_time = time.time()
    qwak_time = end_time - start_time
    return qw, qwak_time

def runMultipleSimpleQWAK(nList,t,samples,adjList_list):
    qwList = []
    tList = []
    qwak_time = 0
    qwak_time_average = 0
#    print(f"Running NP QWAK {len(nList)} walks up to n = {nList[-1]}")
    for n,adjList in tqdm(zip(nList,adjList_list),desc=f"NPQWAK {len(nList)}:{nList[0]}->{nList[-1]}", leave=False):
        for sample,adj in tqdm(zip(range(1,samples+1),adjList),desc=f"Samples for N = {n}"):
#            print(f"----> Calculating NP QWAK for n = {n} \t Sample #{sample}",end='\r')
            qw, qwak_time = runTimedQWAK(n,t,adj)
            qwak_time_average += qwak_time 
        qwak_time_average = qwak_time_average / samples
        qwList.append(qw)
        tList.append(qwak_time_average)
        qwak_time_average = 0
    return tList, qwList

def runMultipleSimpleQWAK_cupy(nList,t,samples,adjList_list):
    qwList = []
    tList = []
    qwak_time = 0
    qwak_time_average = 0
#    print(f"Running CuPy QWAK {len(nList)} walks up to n = {nList[-1]}")
    for n,adjList in tqdm(zip(nList,adjList_list),desc=f"CPQWAK {len(nList)}:{nList[0]}->{nList[-1]}", leave=False):
        for sample,adj in tqdm(zip(range(1,samples+1),adjList),desc=f"Samples for N = {n}"):
#            print(f"----> Calculating CuPy QWAK for n = {n} \t Sample #{sample}",end='\r')
            qw, qwak_time = runTimedQWAK_cupy(n,t,adj)
            qwak_time_average += qwak_time 
        qwak_time_average = qwak_time_average / samples
        qwList.append(qw)
        tList.append(qwak_time_average)
        qwak_time_average = 0
    return tList, qwList

def create_or_load_adjacency_matrices(base_dir, n_values, pVal, samples):
    """
    Checks if adjacency matrix files exist for each size `n` and each sample. If not, generates and saves them.

    Parameters:
        base_dir (str): The base directory to save/load the adjacency matrices.
        n_values (list of int): A list of n values (graph sizes).
        pVal (float): The probability for edge creation in the Erdos-Renyi model.
        samples (int): The number of adjacency matrices to generate for each n value.

    Returns:
        dict: A dictionary where keys are `n` values and values are lists of adjacency matrices.
    """
    adjacency_matrix_dict = {}

    for n in tqdm(n_values, desc="Processing graph sizes"):
        n_dir = os.path.join(base_dir, f"N{n}")  # Directory for this n value
        os.makedirs(n_dir, exist_ok=True)

        adjacency_matrix_list = []
        for sample in tqdm(range(samples), desc=f"Samples for N={n}", leave=False):
            sample_file = os.path.join(n_dir, f"AdjMatrix_N{n}_P{pVal}_Sample{sample}.pkl")

            if os.path.exists(sample_file):
                # Load existing adjacency matrix
                print('File Exists!',end='\r')
                with open(sample_file, 'rb') as f:
                    adjacency_matrix = pickle.load(f)
            else:
                # Generate and save a new adjacency matrix
                graph = nx.erdos_renyi_graph(n, pVal)
                adjacency_matrix = nx.to_numpy_array(graph)
                with open(sample_file, 'wb') as f:
                    pickle.dump(adjacency_matrix, f)

            adjacency_matrix_list.append(adjacency_matrix)

        adjacency_matrix_dict[n] = adjacency_matrix_list

    return adjacency_matrix_dict

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
        
        status_output = subprocess.check_output(['git', 'status', '--porcelain'], text=True).strip()
        if not status_output:
            print("No changes to commit. Exiting.")
            return

        # Create and switch to the new branch
        subprocess.check_call(['git', 'checkout', '-b', branch_name])
        print(f"Switched to new branch: {branch_name}")
        
        # Add changes
        subprocess.check_call(['git', 'add', '.'])
        print("Added changes to staging area.")
        
        # Commit changes
        subprocess.check_call(['git', 'commit', '-m', "PYTHON:"+commit_message])
        print(f"Committed changes with message: {commit_message}")
        
        # Push branch to remote
        subprocess.check_call(['git', 'push', '-u', 'origin', branch_name])
        print(f"Pushed branch '{branch_name}' to remote.")
    
    except subprocess.CalledProcessError as e:
        print(f"Error occurred while executing git command: {e}")
    except Exception as ex:
        print(f"An unexpected error occurred: {ex}")

def create_or_generate_adjacency_matrices(base_dir, n_values, pVal, samples):
    """
    Ensures adjacency matrix files exist for each size `n` and each sample. Creates new matrices if files are missing.

    Parameters:
        base_dir (str): The base directory to save/load the adjacency matrices.
        n_values (list of int): A list of n values (graph sizes).
        pVal (float): The probability for edge creation in the Erdos-Renyi model.
        samples (int): The number of adjacency matrices to generate for each n value.

    Returns:
        dict: A dictionary where keys are `n` values and values are lists of paths to adjacency matrices.
    """
    adjacency_matrix_paths = {}

    for n in tqdm(n_values, desc="Processing graph sizes"):
        n_dir = os.path.join(base_dir, f"N{n}")  # Directory for this n value
        os.makedirs(n_dir, exist_ok=True)

        matrix_paths = []
        for sample in range(samples):
            sample_file = os.path.join(n_dir, f"AdjMatrix_N{n}_P{pVal}_Sample{sample}.pkl")

            if not os.path.exists(sample_file):
                # Generate and save a new adjacency matrix if it does not exist
                graph = nx.erdos_renyi_graph(n, pVal)
                adjacency_matrix = nx.to_numpy_array(graph)
                with open(sample_file, 'wb') as f:
                    pickle.dump(adjacency_matrix, f)

            # Add the path to the list (only paths are stored in memory here)
            matrix_paths.append(sample_file)

        adjacency_matrix_paths[n] = matrix_paths

    return adjacency_matrix_paths


def runMultipleSimpleQWAK2(nList, t, samples, adjList_paths):
    qwList = []
    tList = []
    
    for n, adj_paths in tqdm(zip(nList, adjList_paths.values()), desc=f"NPQWAK {len(nList)}:{nList[0]}->{nList[-1]}", leave=False):
        for sample_idx, adj_path in tqdm(enumerate(adj_paths, start=1), desc=f"Samples for N = {n}", leave=False):
            # Load adjacency matrix only when needed
            with open(adj_path, 'rb') as f:
                adj = pickle.load(f)

            qw, qwak_time = runTimedQWAK(n, t, adj)
            tList.append(qwak_time)
            qwList.append(qw)

    return tList, qwList

def runMultipleSimpleQWAK_cupy2(nList, t, samples, adjList_paths):
    qwList = []
    tList = []

    for n, adj_paths in tqdm(zip(nList, adjList_paths.values()), desc=f"CPQWAK {len(nList)}:{nList[0]}->{nList[-1]}", leave=False):
        for sample_idx, adj_path in tqdm(enumerate(adj_paths, start=1), desc=f"Samples for N = {n}", leave=False):
            # Load adjacency matrix only when needed
            with open(adj_path, 'rb') as f:
                adj = pickle.load(f)

            qw, qwak_time = runTimedQWAK_cupy(n, t, adj)
            tList.append(qwak_time)
            qwList.append(qw)

    return tList, qwList

#nMin = 300
#nMax = 302
#nList = list(range(nMin,nMax,1))
#pVal = 0.8
#samples = 100 
#
#t = 10
#
#qwak_times_filename = f'LINUX-simpleQWAKTime_N{nMin}-{nMax-1}_P{pVal}_T{t}_S{samples}.txt'
#qwak_times_filename_cupy = f'LINUX-simpleQWAKTime_CuPy_N{nMin}-{nMax-1}_P{pVal}_T{t}_S{samples}.txt'
#
#qwak_times_file = f'Datasets/Benchmark-SimpleQWAK_ER/' + qwak_times_filename
#qwak_times_file_cupy = f'Datasets/Benchmark-SimpleQWAK_ER/' + qwak_times_filename_cupy
#
## Base directory
#base_dir = "Datasets/Benchmark-SimpleQWAK_ER/AdjacencyMatrices"
#
## Generate or load the adjacency matrix dictionary
##adjacency_matrix_dict = list(create_or_load_adjacency_matrices(base_dir, nList, pVal, samples).values())
##create_or_load_adjacency_matrices(base_dir, nList, pVal, samples)
#adjacency_matrix_dict = create_or_generate_adjacency_matrices(base_dir, nList, pVal, samples)
#
#if os.path.exists(qwak_times_file):
#     qwak_times = load_list_from_file(qwak_times_file)
#     print('File Exists!')
#else:
#     qwak_times,qw = runMultipleSimpleQWAK2(nList,t,samples,adjacency_matrix_dict )
#     write_list_to_file(qwak_times_file,qwak_times)
#
#if os.path.exists(qwak_times_file_cupy):
#    qwak_times_cupy = load_list_from_file(qwak_times_file_cupy)
#    print('File Exists!')
#else:
#    qwak_times_cupy,qw_cupy = runMultipleSimpleQWAK_cupy2(nList,t,samples,adjacency_matrix_dict)
#    write_list_to_file(qwak_times_file_cupy,qwak_times_cupy)
#
#git_branch_commit_push("new-feature-branch", "Initial commit for the new feature")
#
#plt.plot(nList,qwak_times,label='QWAK CPU_NumPy')
#plt.plot(nList,qwak_times_cupy,label='QWAK GPU_CuPy')
#plt.legend()
#plt.show()

def create_er_seed(base_dir, n_values, pVal, samples):
    graph_seed_dict = {}

    for n in tqdm(n_values, desc="Processing seed sizes"):
        n_dir = os.path.join(base_dir, f"N{n}")  # Directory for this n value
        os.makedirs(n_dir, exist_ok=True)

        graph_seed_list = []
        for sample in tqdm(range(samples), desc=f"Samples for N={n}", leave=False):
            sample_file = os.path.join(n_dir, f"GraphSeed_N{n}_P{pVal}_Sample{sample}.pkl")
            if os.path.exists(sample_file):
                print('File Exists!')
                continue
            else:
                # Generate and save a new adjacency matrix
                random.seed(sample)
                seed = random.random()
                print(seed)
                with open(sample_file, 'wb') as f:
                    pickle.dump(seed, f)

def load_er_seed(base_dir, n_values, pVal, samples):
    graph_seed_dict = {}

    for n in tqdm(n_values, desc="Processing seed sizes"):
        n_dir = os.path.join(base_dir, f"N{n}")  # Directory for this n value
        os.makedirs(n_dir, exist_ok=True)

        graph_seed_list = []
        for sample in tqdm(range(samples), desc=f"Samples for N={n}", leave=False):
            sample_file = os.path.join(n_dir, f"GraphSeed_N{n}_P{pVal}_Sample{sample}.pkl")
            if os.path.exists(sample_file):
               # Load existing adjacency matrix
               with open(sample_file, 'rb') as f:
                   seed = pickle.load(f)

            else:
                print('File not found!\nRun create_er_seed first.')
                return

            graph_seed_list.append(seed)

        graph_seed_dict[n] = graph_seed_list

    return graph_seed_dict

def runTimedQWAK2(n,pVal,t,seed):
    start_time = time.time()
    initNodes = [n//2]
    graph = nx.erdos_renyi_graph(n,pVal,seed=seed) 
    qw = QWAK(graph)
    qw.runWalk(t, initNodes)
    end_time = time.time()
    qwak_time = end_time - start_time
    final_state = qw.getProbVec()
    return final_state, qwak_time

def runTimedQWAK2_cupy(n,pVal,t,seed):
    start_time = time.time()
    initNodes = [n//2]
    graph = nx.erdos_renyi_graph(n,pVal,seed=seed) 
    qw = CQWAK(graph)
    qw.runWalk(t, initNodes)
    end_time = time.time()
    qwak_time = end_time - start_time
    final_state = qw.getProbVec()
    return final_state, qwak_time

def runMultipleSimpleQWAK3(nList, pVal, t, samples):#, seed_list_dict):
    qwList = []
    tList = []
    qwak_time = 0
    qwak_time_average = 0

    for n in tqdm(nList, desc=f"NPQWAK {len(nList)}:{nList[0]}->{nList[-1]}", leave=False):
        for sample in tqdm(range(1, samples + 1), desc=f"Samples for N = {n}"):
            qw, qwak_time = runTimedQWAK2(n, pVal, t, 10)
            qwak_time_average += qwak_time

        qwak_time_average = qwak_time_average / samples
        qwList.append(qw)
        tList.append(qwak_time_average)
        qwak_time_average = 0

    return tList, qwList

def runMultipleSimpleQWAK3_cupy(nList, pVal, t, samples):#, seed_list_dict):
    qwList = []
    tList = []
    qwak_time = 0
    qwak_time_average = 0

    for n in tqdm(nList, desc=f"CuPyQWAK {len(nList)}:{nList[0]}->{nList[-1]}", leave=False):
        # Access the corresponding seed list for the current `n`
        for sample in tqdm(range(1, samples + 1), desc=f"Samples for N = {n}"):
            qw, qwak_time = runTimedQWAK2_cupy(n, pVal, t, 10)
            qwak_time_average += qwak_time

        qwak_time_average = qwak_time_average / samples
        qwList.append(qw)
        tList.append(qwak_time_average)
        qwak_time_average = 0

    return tList, qwList

import os
from datetime import datetime

nMin = 3
nMax = 1000
nList = list(range(nMin, nMax, 1))
pVal = 0.8
samples = 100

t = 100

qwak_times_filename = f'simpleQWAKTime_N{nMin}-{nMax-1}_P{pVal}_T{t}_S{samples}.txt'
qwak_times_filename_cupy = f'3070-simpleQWAKTime_CuPy_N{nMin}-{nMax-1}_P{pVal}_T{t}_S{samples}.txt'

qwak_times_file = f'Datasets/Benchmark-SimpleQWAK_ER/' + qwak_times_filename
qwak_times_file_cupy = f'Datasets/Benchmark-SimpleQWAK_ER/' + qwak_times_filename_cupy

# Record start datetime
start_datetime = datetime.now()

if os.path.exists(qwak_times_file):
    qwak_times = load_list_from_file(qwak_times_file)
    print('File Exists!')
else:
    qwak_times, qw = runMultipleSimpleQWAK3(nList, pVal, t, samples)#, graph_seed_dict)
    write_list_to_file(qwak_times_file, qwak_times)

if os.path.exists(qwak_times_file_cupy):
    qwak_times_cupy = load_list_from_file(qwak_times_file_cupy)
    print('File Exists!')
else:
    qwak_times_cupy, qw_cupy = runMultipleSimpleQWAK3_cupy(nList, pVal, t, samples)#, graph_seed_dict)
    write_list_to_file(qwak_times_file_cupy, qwak_times_cupy)

# Record end datetime and calculate execution time
end_datetime = datetime.now()
execution_time = (end_datetime - start_datetime).total_seconds() / 60

# Get current date and time
current_datetime = end_datetime.strftime('%Y-%m-%d_%H-%M-%S')
execution_time_str = f'{execution_time:.2f}m'

# Combine current date, time, and execution time for the branch name
branch_name = f'{current_datetime}_{execution_time_str}'

# git_branch_commit_push(branch_name, f'simpleQWAKTime_N{nMin}-{nMax-1}_P{pVal}_T{t}_S{samples}')

# for q, qcp in zip(qw,qw_cupy):
#     # Compare the two arrays using np.allclose
#     are_close = np.allclose(q, qcp, atol=1e-5)

#     # Print the result of the comparison
#     print(f"Are the two arrays approximately equal? {are_close}")

# plt.plot(nList,qwak_times,label='QWAK CPU_NumPy')
plt.plot(nList,qwak_times_cupy,label='QWAK GPU_CuPy')
plt.legend()
plt.show()
