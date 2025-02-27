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
import datetime


from qwak_cupy.qwak import QWAK as CQWAK
from qwak.qwak import QWAK as QWAK

def runTimedQWAK(n,pVal,t,seed):
    start_time = time.time()
    initNodes = [n//2]
    graph = nx.erdos_renyi_graph(n,pVal,seed=seed) 
    qw = QWAK(graph)
    qw.runWalk(t, initNodes)
    end_time = time.time()
    qwak_time = end_time - start_time
    final_state = qw.getProbVec()
    return final_state, qwak_time

def runTimedQWAK_cupy(n,pVal,t,seed):
    start_time = time.time()
    initNodes = [n//2]
    graph = nx.erdos_renyi_graph(n,pVal,seed=seed) 
    qw = CQWAK(graph)
    qw.runWalk(t, initNodes)
    end_time = time.time()
    qwak_time = end_time - start_time
    final_state = qw.getProbVec()
    return final_state, qwak_time

def runMultipleSimpleQWAK(nList, pVal, t, samples):#, seed_list_dict):
    qwList = []
    tList = []
    qwak_time = 0
    qwak_time_average = 0

    for n in tqdm(nList, desc=f"NPQWAK {len(nList)}:{nList[0]}->{nList[-1]}", leave=False):
        for sample in tqdm(range(1, samples + 1), desc=f"Samples for N = {n}"):
            qw, qwak_time = runTimedQWAK(n, pVal, t, 10)
            qwak_time_average += qwak_time

        qwak_time_average = qwak_time_average / samples
        qwList.append(qw)
        tList.append(qwak_time_average)
        qwak_time_average = 0

    return tList, qwList

def runMultipleSimpleQWAK_cupy(nList, pVal, t, samples):#, seed_list_dict):
    qwList = []
    tList = []
    qwak_time = 0
    qwak_time_average = 0

    for n in tqdm(nList, desc=f"CuPyQWAK {len(nList)}:{nList[0]}->{nList[-1]}", leave=False):
        # Access the corresponding seed list for the current `n`
        for sample in tqdm(range(1, samples + 1), desc=f"Samples for N = {n}"):
            qw, qwak_time = runTimedQWAK_cupy(n, pVal, t, 10)
            qwak_time_average += qwak_time
        qwak_time_average = qwak_time_average / samples
        qwList.append(qw)
        tList.append(qwak_time_average)
        qwak_time_average = 0

    return tList, qwList

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
    # qwak_times, qw = runMultipleSimpleQWAK3(nList, pVal, t, samples)#, graph_seed_dict)
    # write_list_to_file(qwak_times_file, qwak_times)
    print('File not found!')

if os.path.exists(qwak_times_file_cupy):
    qwak_times_cupy = load_list_from_file(qwak_times_file_cupy)
    print('File Exists!')
else:
    # qwak_times_cupy, qw_cupy = runMultipleSimpleQWAK3_cupy(nList, pVal, t, samples)#, graph_seed_dict)
    # write_list_to_file(qwak_times_file_cupy, qwak_times_cupy)
    print('File not found!')

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

plt.plot(nList,qwak_times,label='QWAK CPU_NumPy')
plt.plot(nList,qwak_times_cupy,label='QWAK GPU_CuPy')
plt.legend()
plt.show()
