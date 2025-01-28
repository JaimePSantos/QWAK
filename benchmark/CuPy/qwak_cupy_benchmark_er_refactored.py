import numpy as np
import cupy as cp
from scipy.linalg import inv, expm
import networkx as nx
import time
import cupyx.scipy.linalg as cpx_scipy
from cupyx.profiler import benchmark
from matplotlib import pyplot as plt
import os
import pickle
from tqdm import tqdm
from datetime import datetime

from qwak_cupy.qwak import QWAK as CQWAK
from qwak.qwak import QWAK as QWAK

def runTimedQWAK(n,pVal,t,seed, hpc = False):
    initNodes = [n//2]
    graph = nx.erdos_renyi_graph(n,pVal,seed=seed)
    start_time = time.time()
    qw = QWAK(graph) if not hpc else CQWAK(graph)
    qw.runWalk(t, initNodes)
    end_time = time.time()
    qwak_time = end_time - start_time
    final_state = qw.getProbVec()
    return final_state, qwak_time

def runMultipleSimpleQWAK(nList, pVal, t, samples, base_dir, hpc=False):
    qwList = []
    tList = []
    qw = 0

    for n in tqdm(nList, desc=f"NPQWAK {len(nList)}:{nList[0]}->{nList[-1]}" if not hpc else f"CuPyQWAK {len(nList)}:{nList[0]}->{nList[-1]}", leave=False):
        n_dir = os.path.join(base_dir, f"N{n}")
        os.makedirs(n_dir, exist_ok=True)
        avg_file = os.path.join(n_dir, f"AVG-t_P{pVal}_T{t}_sample{samples}.pkl")
        qwak_time_average = 0
        for sample in tqdm(range(1, samples + 1), desc=f"Samples for N = {n}", leave=False):
            t_file = os.path.join(n_dir, f"t_P{pVal}_T{t}_sample{sample}.pkl")
            qw_file = os.path.join(n_dir, f"qw_P{pVal}_T{t}_sample{sample}.pkl")

            if os.path.exists(t_file) and os.path.exists(qw_file):
                # print(f"Files for N={n}, Sample={sample} already exist. Skipping.")
                break
            
            qw, qwak_time = runTimedQWAK(n, pVal, t, 10, hpc = hpc)
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

def load_runMultipleSimpleQWAK(nList, pVal, t, base_dir):
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

# Parameters
nMin = 3
nMax = 300
nList = list(range(nMin, nMax, 1))
pVal = 0.8
samples = 3
t = 100

# base_dir = 'Datasets/Benchmark-SimpleQWAK-Test_ER2'
base_dir = 'Datasets/Benchmark-SimpleQWAK-Test_ER2'
base_dir_cupy = 'Datasets/Benchmark-SimpleQWAK_ER2_CuPy'
base_dir_cupy_3070 = 'Datasets/Benchmark-SimpleQWAK_ER2_CuPy_3070'

# Record start datetime
start_datetime = datetime.now()


runMultipleSimpleQWAK(nList, pVal, t, samples, base_dir, hpc = False)
tList, qwList, avg_list = load_runMultipleSimpleQWAK(nList, pVal, t, base_dir)
# print('Standard QWAK results computed and saved.')
# print(avg_list)
    
# tList_cupy, qwList_cupy,avg_list_cupy = load_runMultipleSimpleQWAK(nList, pVal, t, base_dir_cupy)

runMultipleSimpleQWAK(nList, pVal, t, samples, base_dir_cupy_3070, hpc = True)
tList_cupy_3070, qwList_cupy_3070,avg_list_cupy_3070 = load_runMultipleSimpleQWAK(nList, pVal, t, base_dir_cupy_3070)

print('CuPy QWAK results computed and saved.')

# Print elapsed time
elapsed_time = datetime.now() - start_datetime
print(f"Elapsed time: {elapsed_time}")

plt.plot(nList,avg_list,label='QWAK CPU_NumPy')
plt.plot(nList,avg_list_cupy_3070,label='QWAK GPU_CuPy')
plt.legend()
plt.show()
