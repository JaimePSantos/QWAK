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

def runTimedQWAK2(n,pVal,t,seed):
    initNodes = [n//2]
    graph = nx.erdos_renyi_graph(n,pVal,seed=seed)
    start_time = time.time()
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

def runMultipleSimpleQWAK3(nList, pVal, t, samples, base_dir):
    qwList = []
    tList = []
    qw = 0

    for n in tqdm(nList, desc=f"NPQWAK {len(nList)}:{nList[0]}->{nList[-1]}", leave=False):
        n_dir = os.path.join(base_dir, f"N{n}")
        os.makedirs(n_dir, exist_ok=True)
        avg_file = os.path.join(n_dir, f"AVG-t_P{pVal}_T{t}_sample{samples}.pkl")
        qwak_time_average = 0
        for sample in tqdm(range(1, samples + 1), desc=f"Samples for N = {n}", leave=False):
            t_file = os.path.join(n_dir, f"t_P{pVal}_T{t}_sample{sample}.pkl")
            qw_file = os.path.join(n_dir, f"qw_P{pVal}_T{t}_sample{sample}.pkl")

            if os.path.exists(t_file) and os.path.exists(qw_file):
                print(f"Files for N={n}, Sample={sample} already exist. Skipping.")
                continue

            qw, qwak_time = runTimedQWAK2(n, pVal, t, 10)
            qwak_time_average += qwak_time

            # Save t and qw for the current sample
            with open(t_file, 'wb') as f:
                pickle.dump(qwak_time, f)

        qwak_time_average = qwak_time_average/samples

        with open(avg_file, 'wb') as f:
            pickle.dump(qwak_time_average, f)
        with open(qw_file, 'wb') as f:
            pickle.dump(qw, f)

    return

def load_runMultipleSimpleQWAK3(nList, pVal, t, base_dir):
    qwList = []
    tList = []
    avgList = []

    for n in tqdm(nList, desc="Loading NPQWAK data"):
        n_dir = os.path.join(base_dir, f"N{n}")

        qwList_n = []
        tList_n = []
        avg_file = os.path.join(n_dir, f"AVG-t_P{pVal}_T{t}_sample{samples}.pkl")

        if os.path.exists(avg_file):
            with open(avg_file, 'rb') as f:
                avgList.append(pickle.load(f))
        else:
            avgList.append(None)  # Handle missing averages gracefully

        sample = 1
        while True:
            t_file = os.path.join(n_dir, f"t_P{pVal}_T{t}_sample{sample}.pkl")
            qw_file = os.path.join(n_dir, f"qw_P{pVal}_T{t}_sample{sample}.pkl")

            if os.path.exists(t_file) and os.path.exists(qw_file):
                with open(t_file, 'rb') as f:
                    tList_n.append(pickle.load(f))

                with open(qw_file, 'rb') as f:
                    qwList_n.append(pickle.load(f))
            else:
                break

            sample += 1

        if qwList_n and tList_n:
            tList.append(tList_n)
            qwList.append(qwList_n)

    return tList, qwList, avgList

def runMultipleSimpleQWAK3_cupy(nList, pVal, t, samples, base_dir):
    qwList = []
    tList = []
    qw = 0

    for n in tqdm(nList, desc=f"NPQWAK {len(nList)}:{nList[0]}->{nList[-1]}", leave=False):
        n_dir = os.path.join(base_dir, f"N{n}")
        os.makedirs(n_dir, exist_ok=True)
        avg_file = os.path.join(n_dir, f"AVG-t_P{pVal}_T{t}_sample{samples}.pkl")
        qwak_time_average = 0
        for sample in tqdm(range(1, samples + 1), desc=f"Samples for N = {n}", leave=False):
            t_file = os.path.join(n_dir, f"t_P{pVal}_T{t}_sample{sample}.pkl")
            qw_file = os.path.join(n_dir, f"qw_P{pVal}_T{t}_sample{sample}.pkl")

            if os.path.exists(t_file) and os.path.exists(qw_file):
                print(f"Files for N={n}, Sample={sample} already exist. Skipping.")
                continue

            qw, qwak_time = runTimedQWAK2_cupy(n, pVal, t, 10)
            qwak_time_average += qwak_time
            print()

            # Save t and qw for the current sample
            with open(t_file, 'wb') as f:
                pickle.dump(qwak_time, f)

        qwak_time_average = qwak_time_average/samples

        with open(avg_file, 'wb') as f:
            pickle.dump(qwak_time_average, f)
        with open(qw_file, 'wb') as f:
            pickle.dump(qw, f)


    return

def load_runMultipleSimpleQWAK3_cupy(nList, pVal, t, base_dir):
    qwList = []
    tList = []
    avgList = []

    for n in tqdm(nList, desc="Loading CuPyQWAK data"):
        n_dir = os.path.join(base_dir, f"N{n}")

        qwList_n = []
        tList_n = []
        avg_file = os.path.join(n_dir, f"AVG-t_P{pVal}_T{t}_sample{samples}.pkl")

        if os.path.exists(avg_file):
            with open(avg_file, 'rb') as f:
                avgList.append(pickle.load(f))
        else:
            avgList.append(None)  # Handle missing averages gracefully

        sample = 1
        while True:
            t_file = os.path.join(n_dir, f"t_P{pVal}_T{t}_sample{sample}_cupy.pkl")
            qw_file = os.path.join(n_dir, f"qw_P{pVal}_T{t}_sample{sample}_cupy.pkl")

            if os.path.exists(t_file) and os.path.exists(qw_file):
                with open(t_file, 'rb') as f:
                    tList_n.append(pickle.load(f))

                with open(qw_file, 'rb') as f:
                    qwList_n.append(pickle.load(f))
            else:
                break

            sample += 1

        if qwList_n and tList_n:
            tList.append(tList_n)
            qwList.append(qwList_n)

    return tList, qwList, avgList

import os
from datetime import datetime

# Parameters
nMin = 3
nMax = 300
nList = list(range(nMin, nMax, 1))
pVal = 0.8
samples = 3
t = 100

# base_dir = 'Datasets/Benchmark-SimpleQWAK-Test_ER2'
base_dir = 'benchmark/CuPy/Datasets/Benchmark-SimpleQWAK-Test_ER2'

# File paths for results
qwak_times_filename = f'simpleQWAKTime_N{nMin}-{nMax-1}_P{pVal}_T{t}_S{samples}.txt'
qwak_times_filename_cupy = f'3070-simpleQWAKTime_CuPy_N{nMin}-{nMax-1}_P{pVal}_T{t}_S{samples}.txt'

qwak_times_file = os.path.join(base_dir, qwak_times_filename)
qwak_times_file_cupy = os.path.join(base_dir, qwak_times_filename_cupy)

# Record start datetime
start_datetime = datetime.now()


runMultipleSimpleQWAK3(nList, pVal, t, samples, base_dir)
tList, qwList, avg_list = load_runMultipleSimpleQWAK3(nList, pVal, t, base_dir)
print('Standard QWAK results computed and saved.')
print(avg_list)
    
runMultipleSimpleQWAK3_cupy(nList, pVal, t, samples, base_dir)
tList_cupy, qwList_cupy,avg_list_cupy = load_runMultipleSimpleQWAK3_cupy(nList, pVal, t, base_dir)
print(avg_list_cupy)

print('CuPy QWAK results computed and saved.')

# Print elapsed time
elapsed_time = datetime.now() - start_datetime
print(f"Elapsed time: {elapsed_time}")

plt.plot(nList,avg_list,label='QWAK CPU_NumPy')
plt.plot(nList,avg_list_cupy,label='QWAK GPU_CuPy')
plt.legend()
plt.show()
