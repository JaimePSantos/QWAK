import networkx as nx

from OperatorBenchmark import OperatorBenchmark

from typing import List, Dict

from Profiler import profile,find_exact_profiling_file,find_all_profiling_files
import os
import re

def extract_top_cumtime(profiling_data: List[str]) -> List[float]:
    """
    Extracts the cumtime value from the top row of the profiling output for each file's data.
    
    Args:
        profiling_data (List[str]): List of profiling report strings.
        
    Returns:
        List[float]: A list of cumtime values extracted from the first profiling entry in each file.
        
    Raises:
        ValueError: If the expected header or data row cannot be found or parsed.
    """
    cumtime_values = []
    
    for data in profiling_data:
        lines = data.splitlines()
        header_index = None
        
        # Find the header line containing the columns (e.g., "ncalls ... cumtime")
        for i, line in enumerate(lines):
            if line.strip().startswith("ncalls") and "cumtime" in line:
                header_index = i
                break
        if header_index is None:
            raise ValueError("Profiling header with 'ncalls' and 'cumtime' not found in the data.")
        
        # The first non-empty line after the header is assumed to be the top row of data.
        for line in lines[header_index+1:]:
            if line.strip():
                tokens = line.split()
                try:
                    # Expected token order:
                    # tokens[0]: ncalls, tokens[1]: tottime, tokens[2]: percall, tokens[3]: cumtime, tokens[4]: percall, ...
                    cumtime = float(tokens[3])
                except (IndexError, ValueError) as e:
                    raise ValueError(f"Failed to extract cumtime from the profiling line: {line}") from e
                cumtime_values.append(cumtime)
                break  # Stop after processing the first valid data row.
    
    return cumtime_values

def run_if_not_profiled(instance, method_name: str, **kwargs):
    """
    Checks if a profiling file exists for the method (using the current tracked attributes)
    and if not, runs the method with the provided kwargs.
    
    Args:
        instance: The instance containing the method.
        method_name (str): Name of the method to run.
        **kwargs: Keyword arguments that are passed to the method.
    """
    # Update instance attributes with the given kwargs.
    for key, value in kwargs.items():
        setattr(instance, key, value)
    
    # If 'graph' is provided, update 'n' accordingly since 'n' is used in the filename.
    if 'graph' in kwargs:
        setattr(instance, 'n', len(kwargs['graph']))
    
    method = getattr(instance, method_name)
    try:
        existing_file = find_exact_profiling_file(instance, method)
        print(f"Profiling file '{existing_file}' already exists for method '{method_name}' with sample {instance.sample}. Skipping execution.")
    except FileNotFoundError:
        print(f"Profiling file not found for method '{method_name}' with sample {instance.sample}. Running execution.")
        method(**kwargs)

def average_cumtime(cumtime_list: List[float]) -> float:
    """
    Calculates the average cumulative time from a list of cumtime values.

    Args:
        cumtime_list (List[float]): A list of cumulative time values.

    Returns:
        float: The average cumulative time.

    Raises:
        ValueError: If the list is empty.
    """
    if not cumtime_list:
        raise ValueError("The cumtime list is empty. Cannot compute average.")
    
    return sum(cumtime_list) / len(cumtime_list)

def run_profiling_for_ns(n_values: List[int], sample_range=range(0, 3), t: int = 10) -> Dict[int, float]:
    """
    Runs profiling for a variable number of n's.
    
    For each n in n_values:
      - Creates a cycle graph of size n.
      - Creates an instance of OperatorBenchmark with tracked_attributes ['n', 'sample'].
      - For each sample in sample_range, runs the profiled methods 
        (init_operator and build_operator) only if their profiling files don't exist.
      - Loads the profiling data for init_operator, extracts cumtime values, computes the average,
        and stores it in the results dictionary.
    
    Args:
        n_values (List[int]): List of n values (graph sizes) to run profiling for.
        sample_range (iterable, optional): Range of sample indices to run. Defaults to range(0, 3).
        t (int, optional): The time parameter to pass to build_operator. Defaults to 10.
    
    Returns:
        Dict[int, float]: A mapping from each n to the average cumtime (as computed from init_operator's profiling data).
    """
    results = {}
    for n in n_values:
        print(f"Running profiling for n = {n}")
        # Create a new benchmark instance per n, ensuring tracked attributes are updated
        bench = OperatorBenchmark(tracked_attributes=['n', 'sample'])
        graph = nx.cycle_graph(n)
        # Run profiled methods for each sample
        for sample in sample_range:
            run_if_not_profiled(bench, "init_operator", graph=graph, sample=sample)
            run_if_not_profiled(bench, "build_operator", time=t, sample=sample)
        
        # Load profiling data from init_operator and compute average cumtime
        init_files = bench.load_files("init_operator")
        if init_files is not None:
            cumtime_list = extract_top_cumtime(init_files)
            avg = average_cumtime(cumtime_list)
        else:
            avg = None
        results[n] = avg
        print(f"For n = {n}, average cumtime (init_operator): {avg}")
    return results

from typing import List, Dict

def create_profiling_data(n_values: List[int], sample_range=range(0, 3), t: int = 10):
    """
    Runs profiling for a variable number of n's, ensuring that profiling files are created if they do not exist.
    
    Args:
        n_values (List[int]): List of n values (graph sizes) to run profiling for.
        sample_range (iterable, optional): Range of sample indices to run. Defaults to range(0, 3).
        t (int, optional): The time parameter to pass to build_operator. Defaults to 10.
    """
    for n in n_values:
        print(f"Creating profiling data for n = {n}")
        bench = OperatorBenchmark(tracked_attributes=['n', 'sample'])
        graph = nx.cycle_graph(n)

        for sample in sample_range:
            run_if_not_profiled(bench, "init_operator", graph=graph, sample=sample)
            run_if_not_profiled(bench, "build_operator", time=t, sample=sample)


def load_profiling_results(n_values: List[int]) -> Dict[int, float]:
    """
    Loads profiling data for init_operator, extracts cumulative times, and computes the average for each n.
    
    Args:
        n_values (List[int]): List of n values (graph sizes) for which profiling data should be loaded.
    
    Returns:
        Dict[int, float]: A mapping from each n to the average cumtime (computed from init_operator's profiling data).
    """
    results = {}
    for n in n_values:
        print(f"Loading profiling results for n = {n}")
        bench = OperatorBenchmark(tracked_attributes=['n', 'sample'])

        # Load profiling data
        init_files = [f for f in bench.load_files("init_operator") if f"n_{n}_" in f]
        if init_files is not None:
            cumtime_list = extract_top_cumtime(init_files)
            avg = average_cumtime(cumtime_list)
        else:
            avg = None
        
        results[n] = avg
        print(f"For n = {n}, average cumtime (init_operator): {avg}")

    return results

def load_prof_data(path, method_name, nrange, sample_range):
    results = {}
    
    for n in nrange:
        cumtimes = []
        for sample in sample_range:
            file_name = f"{method_name}-n_{n}_sample_{sample}.prof"
            file_path = os.path.join(path, f"n_{n}", file_name)
            
            if os.path.exists(file_path):
                with open(file_path, "r") as file:
                    first_line = file.readline().strip()
                    match = re.search(r'\s+(\d+\.\d+)\s+(\d+\.\d+)$', first_line)
                    if match:
                        cumtime = float(match.group(1))
                        cumtimes.append(cumtime)
        
        if cumtimes:
            results[n] = sum(cumtimes) / len(cumtimes)
    
    return results

import os

def load_profiling_data(path, method_name, nrange, sample_range):
    results = {}
    for n in nrange:
        cumtimes = []
        for sample in sample_range:
            filename = f"{method_name}-n_{n}_sample_{sample}.prof"
            # Include the n_{n} directory in the file path
            filepath = os.path.join(path, f"n_{n}", filename)
            with open(filepath, 'r') as f:
                next(f)  # Skip the header line
                found = False
                for line in f:
                    line = line.strip()
                    if not line:
                        continue
                    parts = line.split()
                    if len(parts) < 6:
                        continue
                    try:
                        cumtime = float(parts[3])
                    except (IndexError, ValueError):
                        continue
                    func_part = ' '.join(parts[5:])
                    if '(' in func_part and ')' in func_part:
                        func_name = func_part.split('(')[-1].split(')')[0]
                        if func_name == method_name:
                            cumtimes.append(cumtime)
                            found = True
                            break
                if not found:
                    raise ValueError(f"Method '{method_name}' not found in {filepath}")
        average_cumtime = sum(cumtimes) / len(cumtimes)
        results[n] = average_cumtime
    return results

# The rest of the code remains the same


if __name__ == "__main__":
    # n = 100
    # t = 10
    # graph = nx.cycle_graph(n)
    # print(nx.cycle_graph.__name__)
    # marked = [20]

    # # Initialize benchmark
    # graph = nx.cycle_graph(n)
    # bench = OperatorBenchmark(tracked_attributes=['n','sample'])

    # # Run profiling only if profiling files are missing.
    # for sample in range(0, 10):
    #     run_if_not_profiled(bench, "init_operator", graph=graph, sample=sample)
    #     run_if_not_profiled(bench, "build_operator", time=t, sample=sample)

    # bench_init_file = bench.load_files('init_operator')
    # bench_operator_file = bench.load_files('build_operator')

    # cumtime = extract_top_cumtime(bench_init_file)
    # cumtime2 = extract_top_cumtime(bench_operator_file)

    # print(cumtime)
    # print(cumtime2)

    # print(average_cumtime(cumtime))
    # print(average_cumtime(cumtime2))
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