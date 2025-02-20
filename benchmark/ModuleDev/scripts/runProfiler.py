import networkx as nx

from OperatorBenchmark import OperatorBenchmark

from typing import List, Dict

from scripts import create_profiling_data, load_profiling_data

import os
import re

if __name__ == "__main__":

    n_values = [50, 100, 200,300,600,1000]

    # Step 1: Create profiling data
    create_profiling_data(n_values,sample_range=range(0,10),t=10)

    SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))

    # Build relative path to profiling data
    path = os.path.normpath(os.path.join(
        SCRIPT_DIR,
        "TestOutput/Profiling/operator_results"
    ))

    # Verify path exists
    if not os.path.exists(path):
        print(f"ERROR: Path not found - {path}")
        print("Current directory contents:", os.listdir(SCRIPT_DIR))
        exit()

    # Now load data
    result = load_profiling_data(
        path=path,
        method_name="init_operator",
        nrange=n_values,
        sample_range=range(10)  # Assuming samples 0-9
    )

    print(result)
    result2 = load_profiling_data(
        path=path,
        method_name="build_operator",
        nrange=n_values,
        sample_range=range(10)  # Assuming samples 0-9
    )

    print(result2)