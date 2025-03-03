import networkx as nx

from OperatorBenchmark import OperatorBenchmark

from typing import List, Dict

from scripts import create_profiling_data, load_profiling_data,create_profiling_data_ER,separate_keys_and_values,git_branch_commit_push,create_profiling_data_ER_HPC
from datetime import datetime

import os
import re

from utils.plotTools import plot_qwak


nMin = 3
nMax = 1000
n_values = list(range(nMin, nMax, 1))
pVal = 0.8
seed = 10
sample_range = range(0,100)
# Step 1: Create profiling data
# create_profiling_data(n_values,sample_range=range(0,10),t=10)
#create_profiling_data_ER(n_values,sample_range=sample_range,t=10, pVal=pVal, seed=seed)
#git_branch_commit_push('1', f'Completed NumPy calculations')
create_profiling_data_ER_HPC(n_values,sample_range=sample_range,t=10, pVal=pVal, seed=seed)
git_branch_commit_push('2', f'Completed CuPy calculations')
