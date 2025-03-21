from qwak.qwak import QWAK as QWAK
from qwak_cupy.qwak import QWAK as CQWAK
import matplotlib.pyplot as plt
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


def runTimedQWAK(n, pVal, t, seed, hpc=False):
    initNodes = [n // 2]
    graph = nx.erdos_renyi_graph(n, pVal, seed=seed)
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

    for n in tqdm(nList, desc=f"NPQWAK {len(nList)}:{
                  nList[0]}->{nList[-1]}" if not hpc else f"CuPyQWAK {len(nList)}:{nList[0]}->{nList[-1]}", leave=False):
        n_dir = os.path.join(base_dir, f"N{n}")
        os.makedirs(n_dir, exist_ok=True)
        avg_file = os.path.join(
            n_dir, f"AVG-t_P{pVal}_T{t}_sample{samples}.pkl")
        qwak_time_average = 0
        for sample in tqdm(
                range(
                    1,
                    samples + 1),
                desc=f"Samples for N = {n}",
                leave=False):
            t_file = os.path.join(
                n_dir, f"t_P{pVal}_T{t}_sample{sample}.pkl")
            qw_file = os.path.join(
                n_dir, f"qw_P{pVal}_T{t}_sample{sample}.pkl")

            if os.path.exists(t_file) and os.path.exists(qw_file):
                # print(f"Files for N={n}, Sample={sample} already exist. Skipping.")
                break

            qw, qwak_time = runTimedQWAK(n, pVal, t, 10, hpc=hpc)
            qwak_time_average += qwak_time

            # Save t and qw for the current sample
            with open(t_file, 'wb') as f:
                pickle.dump(qwak_time, f)

        qwak_time_average = qwak_time_average / samples

        with open(avg_file, 'wb') as f:
            pickle.dump(qwak_time_average, f)
        with open(qw_file, 'wb') as f:
            pickle.dump(qw, f)

    return


def load_runMultipleSimpleQWAK(nList, pVal, samples, t, base_dir):
    qwList = []
    tList = []
    avgList = []

    for n in tqdm(nList, desc="Loading NPQWAK data"):
        n_dir = os.path.join(base_dir, f"N{n}")

        qwList_n = []
        tList_n = []
        avg_file = os.path.join(
            n_dir, f"AVG-t_P{pVal}_T{t}_sample{samples}.pkl")

        if os.path.exists(avg_file):
            with open(avg_file, 'rb') as f:
                avgList.append(pickle.load(f))
        else:
            avgList.append(None)  # Handle missing averages gracefully

        sample = 1
        while True:
            t_file = os.path.join(
                n_dir, f"t_P{pVal}_T{t}_sample{sample}.pkl")
            qw_file = os.path.join(
                n_dir, f"qw_P{pVal}_T{t}_sample{sample}.pkl")

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


def load_runMultipleSimpleQWAK_legacy(
        nList, pVal, samples, t, base_dir):
    qwList = []
    tList = []
    avgList = []

    for n in tqdm(nList, desc="Loading NPQWAK data"):
        n_dir = os.path.join(base_dir, f"N{n}")

        qwList_n = []
        tList_n = []
        avg_file = os.path.join(
            n_dir, f"AVG-t_P{pVal}_T{t}_sample{samples}.pkl")

        if os.path.exists(avg_file):
            with open(avg_file, 'rb') as f:
                avgList.append(pickle.load(f))
        else:
            print(f"{avg_file} not found.")
            avgList.append(None)  # Handle missing averages gracefully

    return avgList


def save_time_averages_from_txt(
        txt_file,
        nList,
        pVal,
        t,
        base_dir,
        samples):
    """
    Reads time averages from a text file and saves them in .pkl files, one per N.

    Parameters:
    - txt_file: Path to the text file containing time averages.
    - nList: List of values for N.
    - pVal: Value of p.
    - t: Value of t.
    - base_dir: Base directory where the folders and files will be saved.
    """
    # Read time averages from the text file
    with open(txt_file, 'r') as file:
        time_averages = [float(line.strip()) for line in file]

    # Ensure the number of time averages matches the number of N values
    if len(time_averages) != len(nList):
        raise ValueError(
            "The number of time averages in the text file does not match the number of N values.")

    # Iterate over each value of N
    for idx, n in enumerate(tqdm(nList, desc=f"Processing N values {
                            len(nList)}:{nList[0]}->{nList[-1]}", leave=False)):
        n_dir = os.path.join(base_dir, f"N{n}")
        os.makedirs(n_dir, exist_ok=True)

        # Create the average file path
        avg_file = os.path.join(
            n_dir, f"AVG-t_P{pVal}_T{t}_sample{samples}.pkl")

        # Save the time average for the current N
        with open(avg_file, 'wb') as f:
            pickle.dump(time_averages[idx], f)

    print("Time averages have been saved successfully.")

# import numpy as np
# import matplotlib.pyplot as plt

# # If you don't have statsmodels installed, do:
# #   pip install statsmodels
# from statsmodels.nonparametric.smoothers_lowess import lowess

# def smooth_data_lowess(x, y, frac=0.05):
#     """
#     Smooth data using a LOESS (Locally Weighted Scatterplot Smoothing) approach.
#     LOESS fits simple models to localized subsets of the data to capture
#     the overall trend while reducing noise or bumps.

#     :param x: 1D array-like of x data
#     :param y: 1D array-like of y data
#     :param frac: Between 0 and 1; the fraction of data used when estimating each y value.
#                  Smaller values of frac create a tighter fit (less smoothing),
#                  while larger values create a smoother curve.
#     :return: (x_smooth, y_smooth)
#     """
#     # lowess returns an Nx2 array where:
#     #   first column is the sorted x,
#     #   second column is the corresponding smoothed y.
#     smoothed = lowess(y, x, frac=frac)
#     x_smooth = smoothed[:, 0]
#     y_smooth = smoothed[:, 1]
#     return x_smooth, y_smooth

# # ------------------------------------------
# # Example usage within your code:
# # ------------------------------------------
# # Assume you have nList, avg_list, avg_list_cupy_970, and params from before.

# # 1) Smooth each data series using LOESS:
# x_smooth_0, y_smooth_0 = smooth_data_lowess(nList, avg_list, frac=0.05)
# x_smooth_1, y_smooth_1 = smooth_data_lowess(nList, avg_list_cupy_970, frac=0.05)

# # 2) Use these smoothed data arrays when calling plot_qwak:
# x_value_matrix_smooth = [x_smooth_0, x_smooth_1]
# y_value_matrix_smooth = [y_smooth_0, y_smooth_1]

# plot_qwak(x_value_matrix=x_value_matrix_smooth,
#           y_value_matrix=y_value_matrix_smooth,
#           **params)
# plt.show()

# base_dir = 'Datasets/Benchmark-SimpleQWAK_ER-NumPy'

# qwak_times_filename = f'LINUX-simpleQWAKTime_N{nMin}-{nMax-1}_P{pVal}_T{t}_S{samples}.txt'
# qwak_times_filename_cupy = f'3070-simpleQWAKTime_CuPy_N{nMin}-{nMax-1}_P{pVal}_T{t}_S{samples}.txt'

# qwak_times_file = f'Datasets/Benchmark-SimpleQWAK_ER/' + qwak_times_filename
# qwak_times_file_cupy = f'Datasets/Benchmark-SimpleQWAK_ER/' + qwak_times_filename_cupy

# # Example usage:
# save_time_averages_from_txt(qwak_times_file, nList=nList, pVal=pVal, t=t, samples=samples, base_dir=base_dir)

# qwak_times_filename = f'LINUX-simpleQWAKTime_N{nMin}-{nMax-1}_P{pVal}_T{t}_S{samples}.txt'
# qwak_times_file = f'Datasets/Benchmark-SimpleQWAK_ER/' + qwak_times_filename

# qwak_times_filename_cupy_970 = f'LINUX-simpleQWAKTime_CuPy_N{nMin}-{nMax-1}_P{pVal}_T{t}_S{samples}.txt'
# qwak_times_file_cupy_970 = f'Datasets/Benchmark-SimpleQWAK_ER/' + qwak_times_filename_cupy_970

# qwak_times_filename_cupy_3070_2 = f'3070-simpleQWAKTime_CuPy_N{nMin}-{nMax-1}_P{pVal}_T{t}_S{samples}.txt'
# qwak_times_file_cupy_3070_2 = f'Datasets/Benchmark-SimpleQWAK_ER/' + qwak_times_filename_cupy_3070_2


# directory = 'Datasets/Benchmark-SimpleQWAK_ER/'
# files = os.listdir(directory)
# print(qwak_times_filename_cupy_3070_2)
# print(files)

# Example usage:
# save_time_averages_from_txt(qwak_times_file_cupy_3070_2, nList=nList, pVal=pVal, t=t, base_dir=base_dir_cupy_3070_2,samples=samples)
