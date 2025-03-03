import networkx as nx
from scipy import linalg as ln
import numpy as np
import time as tm
import matplotlib.pyplot as plt
from statistics import mean
import os
import csv
from qwak.Operator import Operator
from utils.plotTools import plot_qwak


from OperatorBenchmark3 import OperatorBenchmark3

def benchmark_operations(n, tList, base_filename, samples,pVal=0.8,seed=10):
    graph = nx.erdos_renyi_graph(n,pVal,seed=seed)
    eig_runTime = []
    expm_runTime = []
    eig_filename = f"{base_filename}_eig.csv"
    expm_filename = f"{base_filename}_expm.csv"
    
    if os.path.exists(eig_filename) and os.path.exists(expm_filename):
        print('Files found!')
        with open(eig_filename, "r") as f:
            reader = csv.reader(f)
            next(reader)  # Skip header
            eig_runTime = list(map(float, next(reader)))
            print(f'{eig_filename} exists!')
                
        with open(expm_filename, "r") as f:
            reader = csv.reader(f)
            next(reader)  # Skip header
            expm_runTime = list(map(float, next(reader)))
            print(f'{expm_filename} exists!')
        return eig_runTime, expm_runTime
    
    else:
        print('Files not found!')
        op = OperatorBenchmark3(graph)
        opAdjTime = op.buildAdjacencyTimed()
        opEigTime = op.buildEigenTimed()
        op_init_run_time = opAdjTime + opEigTime

        for time in tList:
            total_runOp_run_time = 0
            for _ in range(samples):
                for t in range(0, time):
                    runOp_run_time = op.buildDiagonalOperatorNoEigTimed(graph=graph, time=t)
                    total_runOp_run_time += runOp_run_time
            avg_runOp_run_time = total_runOp_run_time / samples
            eig_runTime.append(avg_runOp_run_time + op_init_run_time)
            op_init_run_time = 0

        # Time the buildDiagonalOperator method for expm
        op2 = OperatorBenchmark3(graph)
        op2AdjTime = op2.buildAdjacencyTimed()

        for time in tList:
            print(f'Expm time: {time}')
            total_runOp2_run_time = 0
            for s in range(samples):
                if s%20 == 0:
                    print(f'\t----> Sample: {s}')
                for t in range(0, time):
                    runOp2_run_time = op2.buildSlowDiagonalOperatorNoAdjTimed(graph=graph, time=t)
                    total_runOp2_run_time += runOp2_run_time
            avg_runOp2_run_time = total_runOp2_run_time / samples
            expm_runTime.append(avg_runOp2_run_time + op2AdjTime)
            op2AdjTime = 0
            
        with open(eig_filename, "w", newline="") as f:
            writer = csv.writer(f)
            writer.writerow(["Eig RunTime"])
            writer.writerow(eig_runTime)

        # Save to CSV
        with open(expm_filename, "w", newline="") as f:
            writer = csv.writer(f)
            writer.writerow(["Expm RunTime"])
            writer.writerow(expm_runTime)

        return eig_runTime, expm_runTime
    


# Example usage
n = 30
start = 1
stop = n
step = 1
samples = 200
legend_labels = ['Diagonal', 'Expm']

params = {
    'figsize': (12, 8),
    'plot_title' : f'Benchmark N={n}',
    'x_label' : 'Number of Walks',
    'y_label' : "Time",
    'legend_labels' : legend_labels,
    'legend_loc': "best",
    # 'legend_title' : 'Solutions',
    'legend_ncol' : 1,
    # 'color_list' : ['#0000FF', '#008000', '#525252'],
    'color_list' : ['b','g','r'],
    # 'line_style_list' : ['--', '-','-.' ],
    'save_path' : f'img/ER/dynamicBenchmark_WSTART{start}_WEND{stop}_WST{step}_SAMP{samples}.png',
    'use_loglog': False,
    'use_cbar' : False,
    'cbar_label' : None, 
    'cbar_ticks' : None,
    'cbar_tick_labels' : None,
    'x_lim' : None,
    'x_num_ticks' : 10,
    'y_num_ticks' : 5,
    'x_round_val' : 2,
    'y_round_val' : 3,
    # 'v_line_values' : v_line_values,
    # 'v_line_style': '--',
    'title_font_size': 20,
    'xlabel_font_size': 22,
    'ylabel_font_size': 22,
    'legend_font_size': 14,
    'legend_title_font_size': 14,
    'tick_font_size': 18,
    # 'cbar_label_font_size': 16,
    'use_grid':True,
    'marker_list': ['x', 'o']
}


tList = list(range(start, stop, step))

filename = f'Datasets/OperatorBenchmark/Dynamic-ER/dynamicBenchmark_WSTART{start}_WEND{stop}_WST{step}_SAMP{samples}'

eig_runTime, expm_runTime = benchmark_operations(n, tList, filename, samples)

y_values = [eig_runTime, expm_runTime]
x_values = [tList]*2
plot_qwak(x_value_matrix = x_values, y_value_matrix = y_values,**params)