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

from qwak_cupy.qwak import QWAK as CQWAK
from qwak.qwak import QWAK as QWAK

def runTimedQWAK(n,t):
    start_time = time.time()
    initNodes = [n//2]
    qw = QWAK(nx.cycle_graph(n))
    qw.runWalk(t, initNodes)
    end_time = time.time()
    qwak_time = end_time - start_time
    return qw, qwak_time

def runTimedQWAK_cupy(n,t):
    start_time = time.time()
    initNodes = [n//2]
    qw = CQWAK(nx.cycle_graph(n))
    qw.runWalk(t, initNodes)
    end_time = time.time()
    qwak_time = end_time - start_time
    return qw, qwak_time

def runMultipleSimpleQWAK(nList,t,samples):
    qwList = []
    tList = []
    qwak_time = 0
    qwak_time_average = 0
    print(f"Running NP QWAK {len(nList)} walks up to n = {nList[-1]}")
    for n in nList:
        for sample in range(1,samples+1):
            print(f"----> Calculating NP QWAK for n = {n} \t Sample #{sample}",end='\r')
            qw, qwak_time = runTimedQWAK(n,t)
            qwak_time_average += qwak_time 
        qwak_time_average = qwak_time_average / samples
        qwList.append(qw)
        tList.append(qwak_time_average)
        qwak_time_average = 0
    return tList, qwList

def runMultipleSimpleQWAK_cupy(nList,t,samples):
    qwList = []
    tList = []
    qwak_time = 0
    qwak_time_average = 0
    print(f"Running CuPy QWAK {len(nList)} walks up to n = {nList[-1]}")
    for n in nList:
        # print(f"----> Calculating NP QWAK for n = {n}",end='\r')
        for sample in range(1,samples+1):
            print(f"----> Calculating CuPy QWAK for n = {n} \t Sample #{sample}",end='\r')
            qw, qwak_time = runTimedQWAK_cupy(n,t)
            qwak_time_average += qwak_time 
        qwak_time_average = qwak_time_average / samples
        qwList.append(qw)
        tList.append(qwak_time_average)
        qwak_time_average = 0
    return tList, qwList

def runMultipleSimpleQWAK_cupy2(nList,t,samples):
    #qwList = []
    tList = []
    qwak_time = 0
    qwak_time_average = 0
    print(f"Running CuPy QWAK {len(nList)} walks up to n = {nList[-1]}")
    for n in nList:
        # print(f"----> Calculating NP QWAK for n = {n}",end='\r')
        for sample in range(1,samples+1):
            print(f"----> Calculating CuPy QWAK for n = {n} \t Sample #{sample}",end='\r')
            qw, qwak_time = runTimedQWAK_cupy(n,t)
            qwak_time_average += qwak_time 
        qwak_time_average = qwak_time_average / samples
        # qwList.append(qw)
        tList.append(qwak_time_average)
        qwak_time_average = 0
    return tList#, qwList

def load_list_from_file(file_path):
    with open(file_path, 'r') as file:
        data_str = file.read()
    data = [json.loads(line) for line in data_str.splitlines()]
    return data

def write_list_to_file(file_path, data):
    data_str = [str(item) for item in data]  # Convert float values to strings
    with open(file_path, 'w') as file:
        file.write('\n'.join(data_str))
t = 50
nMin = 800
nMax = 1000
nList = list(range(nMin,nMax,1))
samples = 100

qwak_times_file = f'Datasets/Benchmark-SimpleQWAK_Cycle/simpleQWAKTime_N{nMin}-{nMax-1}_T{t}_S{samples}.txt'
qwak_times_file_cupy = f'Datasets/Benchmark-SimpleQWAK_Cycle/simpleQWAKTime_CuPy_N{nMin}-{nMax-1}_T{t}_S{samples}.txt'

# if os.path.exists(qwak_times_file):
#     qwak_times = load_list_from_file(qwak_times_file)
#     print('File Exists!')
# else:
#     qwak_times,qw = runMultipleSimpleQWAK(nList,t,samples)
#     write_list_to_file(qwak_times_file,qwak_times)

if os.path.exists(qwak_times_file_cupy):
    qwak_times_cupy = load_list_from_file(qwak_times_file_cupy)
    print('File Exists!')
else:
    qwak_times_cupy = runMultipleSimpleQWAK_cupy2(nList,t,samples)
    write_list_to_file(qwak_times_file_cupy,qwak_times)


plt.plot(nList,qwak_times,label='QWAK CPU_NumPy')
plt.plot(nList,qwak_times_cupy,label='QWAK GPU_CuPy')
plt.legend()
plt.show()
