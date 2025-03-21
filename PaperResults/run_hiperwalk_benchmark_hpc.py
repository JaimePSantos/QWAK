import networkx as nx

from OperatorBenchmark import OperatorBenchmark

from typing import List, Dict

from scripts import load_profiling_data, separate_keys_and_values, git_branch_commit_push, create_profiling_data_hiperwalk_hpc
from datetime import datetime

import os
import re

from utils.plotTools import plot_qwak


nMin = 3
nMax = 1000
n_values = list(range(nMin, nMax, 1))
pVal = 0.8
seed = 10
sample_range = range(0, 100)
# Step 1: Create profiling data
# create_profiling_data(n_values,sample_range=range(0,10),t=10)
create_profiling_data_hiperwalk_hpc(
    n_values,
    sample_range=sample_range,
    t=10,
    pVal=pVal,
    seed=seed)

# SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
# Build relative path to profiling data
# path = os.path.normpath(os.path.join(
#    SCRIPT_DIR,
#    "TestOutput/Profiling/hiperwalk_results"
# ))
# Verify path exists
# if not os.path.exists(path):
#    print(f"ERROR: Path not found - {path}")
#    print("Current directory contents:", os.listdir(SCRIPT_DIR))
#    exit()
# Now load data
# result = load_profiling_data(
#    path=path,
#    method_name="init_hiperwalk",
#    nrange=n_values,
#    sample_range=sample_range,  # Assuming samples 0-9
#    pVal=pVal,
#    seed=seed
# )
# result2 = load_profiling_data(
#    path=path,
#    method_name="simulate",
#    nrange=n_values,
#    sample_range=sample_range,  # Assuming samples 0-9
#    pVal=pVal,
#    seed=seed
# )
#
# params = {
#    'figsize': (12, 8),
#    'plot_title' : f'Complete N',
#    'x_label' : 'Time',
#    'y_label' : "Probability",
#    'legend_labels' : ['init','build'],
#    'legend_loc': "best",
#    'legend_title' : 'Solutions',
#    'legend_ncol' : 1,
#    # 'color_list' : ['#0000FF', '#008000', '#525252'],
#    'color_list' : ['b','g','r'],
#    'line_style_list' : ['--', '-','-.' ],
#    # 'save_path' : f'Output/CompleteSearch/completePlot_N{N}_NWALKS{numberOfWalks}_S{samples}.png',
#    'use_loglog': False,
#    'use_cbar' : False,
#    'cbar_label' : None,
#    'cbar_ticks' : None,
#    'cbar_tick_labels' : None,
#    'x_lim' : None,
#    'x_num_ticks' : 7,
#    'y_num_ticks' : 5,
#    'x_round_val' : 2,
#    'y_round_val' : 3,
#    # 'v_line_values' : v_line_values,
#    # # 'v_line_style': '--',
#    'title_font_size': 20,
#    'xlabel_font_size': 22,
#    'ylabel_font_size': 22,
#    'legend_font_size': 14,
#    'legend_title_font_size': 14,
#    'tick_font_size': 18,}
#
# result_keys, result_values = separate_keys_and_values(result)
# result2_keys, result2_values = separate_keys_and_values(result2)
# x_value_matrix = [result_keys,result2_keys]
# y_value_matrix = [result_values,result2_values]
#
# plot_qwak(x_value_matrix = x_value_matrix, y_value_matrix = y_value_matrix,**params)
