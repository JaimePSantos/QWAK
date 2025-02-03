import numpy as np
import cupy as cp
from scipy.linalg import inv, expm
import networkx as nx
import time
import cupyx.scipy.linalg as cpx_scipy
from cupyx.profiler import benchmark
import os
import pickle
from tqdm import tqdm
from datetime import datetime
import matplotlib
matplotlib.use('Qt5Agg')
import matplotlib.pyplot as plt

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

def runTimedQWAK_anim(qwak,t, hpc = False):
    start_time = time.time()
    qwak.runWalk(t)
    end_time = time.time()
    qwak_time = end_time - start_time
    final_state = qwak.getProbVec()
    return final_state, qwak_time

def runMultipleAnimQWAK(n, pVal, tList, samples,seed, base_dir, hpc=False):
    qwList = []
    tList_storage = []
    qw = 0

    initNodes = [n//2]
    graph = nx.erdos_renyi_graph(n,pVal,seed=seed)
    qwak = QWAK(graph,initStateList=initNodes)

    for t in tqdm(tList, desc=f"NPQWAK {len(tList)}:{tList[0]}->{tList[-1]}" if not hpc else f"CuPyQWAK {len(tList)}:{tList[0]}->{tList[-1]}", leave=False):
        t_dir = os.path.join(base_dir, f"t{t}")
        os.makedirs(t_dir, exist_ok=True)
        avg_file = os.path.join(t_dir, f"AVG-t_P{pVal}_N{n}_sample{samples}.pkl")
        qwak_time_average = 0
        for sample in tqdm(range(1, samples + 1), desc=f"Samples for t = {t}", leave=False):
            t_file = os.path.join(t_dir, f"t_P{pVal}_N{n}_sample{sample}.pkl")
            qw_file = os.path.join(t_dir, f"qw_P{pVal}_N{n}_sample{sample}.pkl")

            if os.path.exists(t_file) and os.path.exists(qw_file):
                # print(f"Files for N={n}, Sample={sample} already exist. Skipping.")
                break   
            
            qw, qwak_time = runTimedQWAK_anim(qwak, t, hpc = hpc)
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

def load_runMultipleAnimQWAK(n, pVal, tList, base_dir):
    qwList = []
    tList_storage = []
    avgList = []

    for t in tqdm(tList, desc="Loading NPQWAK data"):
        t_dir = os.path.join(base_dir, f"t{t}")

        qwList_n = []
        tList_n = []
        avg_file = os.path.join(t_dir, f"AVG-t_P{pVal}_N{n}_sample{samples}.pkl")

        if os.path.exists(avg_file):
            with open(avg_file, 'rb') as f:
                avgList.append(pickle.load(f))
        else:
            avgList.append(None)  # Handle missing averages gracefully

        sample = 1
        while True:
            t_file = os.path.join(t_dir, f"t_P{pVal}_N{n}_sample{sample}.pkl")
            qw_file = os.path.join(t_dir, f"qw_P{pVal}_N{n}_sample{sample}.pkl")
            # print(os.path.exists(qw_file))
            if os.path.exists(t_file) and os.path.exists(qw_file):
                with open(t_file, 'rb') as f:
                    
                    tList_n.append(pickle.load(f))

                with open(qw_file, 'rb') as f:
                    # print(f'lololol len{pickle.load(f)}')
                    qwList_n.append(pickle.load(f))
            else:
                break

            sample += 1

        if qwList_n and tList_n:
            # print('hi')
            tList_storage.append(tList_n)
            qwList.append(qwList_n)

    return tList_storage, qwList, avgList

# Parameters
n = 100
tMin = 1
tMax = 100
tList = list(range(tMin, tMax, 1))
# print(tList)
pVal = 0.8
samples = 2
seed = 10

base_dir_cupy_970 = f'Datasets/Benchmark-AnimQWAK_ER_N{n}-CuPy_970'
base_dir = f'Datasets/Benchmark-AnimQWAK_ER_N{n}-NumPy'


# # Record start datetime
start_datetime = datetime.now()

runMultipleAnimQWAK(n, pVal, tList, samples,seed, base_dir, hpc=False)
tBenchList, qwList,avg_list = load_runMultipleAnimQWAK(n, pVal, tList, base_dir)

runMultipleAnimQWAK(n, pVal, tList, samples,seed, base_dir_cupy_970, hpc=True)
tBenchList_cupy_970, qwList_cupy_970,avg_list_cupy_970 = load_runMultipleAnimQWAK(n, pVal, tList, base_dir_cupy_970)

print('CuPy QWAK results computed and saved.')


# print(avg_list_cupy_3070)
elapsed_time = datetime.now() - start_datetime
print(f"Elapsed time: {elapsed_time}")

plt.plot(tList,avg_list,label='QWAK CPU_NumPy')
plt.plot(tBenchList_cupy_970,avg_list_cupy_970,label='QWAK GPU_CuPy970')
plt.legend()
plt.show()
