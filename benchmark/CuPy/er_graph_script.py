import os
import networkx as nx
import pickle
import numpy as np
from tqdm import tqdm
import random

def create_or_load_adjacency_matrices(base_dir, n_values, pVal, samples):
    """
    Checks if adjacency matrix files exist for each size `n` and each sample. If not, generates and saves them.

    Parameters:
        base_dir (str): The base directory to save/load the adjacency matrices.
        n_values (list of int): A list of n values (graph sizes).
        pVal (float): The probability for edge creation in the Erdos-Renyi model.
        samples (int): The number of adjacency matrices to generate for each n value.

    Returns:
        dict: A dictionary where keys are `n` values and values are lists of adjacency matrices.
    """
    adjacency_matrix_dict = {}

    for n in tqdm(n_values, desc="Processing graph sizes"):
        n_dir = os.path.join(base_dir, f"N{n}")  # Directory for this n value
        os.makedirs(n_dir, exist_ok=True)

        adjacency_matrix_list = []
        for sample in tqdm(range(samples), desc=f"Samples for N={n}", leave=False):
            sample_file = os.path.join(n_dir, f"AdjMatrix_N{n}_P{pVal}_Sample{sample}.pkl")

            if os.path.exists(sample_file):
                # Load existing adjacency matrix
                print('File Exists!')
                with open(sample_file, 'rb') as f:
                    adjacency_matrix = pickle.load(f)
            else:
                # Generate and save a new adjacency matrix
                graph = nx.erdos_renyi_graph(n, pVal)
                adjacency_matrix = nx.to_numpy_array(graph)
                with open(sample_file, 'wb') as f:
                    pickle.dump(adjacency_matrix, f)

            adjacency_matrix_list.append(adjacency_matrix)

        adjacency_matrix_dict[n] = adjacency_matrix_list

    return adjacency_matrix_dict

# Configuration variables
nMin = 3 
nMax = 4
nList = list(range(nMin, nMax, 1))  # List of n values
pVal = 0.8
samples = 100
t = 50  # Assuming 't' is a given parameter for the filename

## Base directory
#base_dir = "Datasets/Benchmark-SimpleQWAK_ER/AdjacencyMatrices"
#
## Generate or load the adjacency matrix dictionary
#adjacency_matrix_dict = create_or_load_adjacency_matrices(base_dir, nList, pVal, samples)

#print(list(adjacency_matrix_dict.values()))

def create_er_seed(base_dir, n_values, pVal, samples):
    graph_seed_dict = {}

    for n in tqdm(n_values, desc="Processing seed sizes"):
        n_dir = os.path.join(base_dir, f"N{n}")  # Directory for this n value
        os.makedirs(n_dir, exist_ok=True)

        graph_seed_list = []
        for sample in tqdm(range(samples), desc=f"Samples for N={n}", leave=False):
            sample_file = os.path.join(n_dir, f"GraphSeed_N{n}_P{pVal}_Sample{sample}.pkl")
            if os.path.exists(sample_file):
                print('File Exists!')
                continue
            else:
                # Generate and save a new adjacency matrix
                random.seed(sample)
                seed = random.random()
                print(seed)
                with open(sample_file, 'wb') as f:
                    pickle.dump(seed, f)

def load_er_seed(base_dir, n_values, pVal, samples):
    graph_seed_dict = {}

    for n in tqdm(n_values, desc="Processing seed sizes"):
        n_dir = os.path.join(base_dir, f"N{n}")  # Directory for this n value
        os.makedirs(n_dir, exist_ok=True)

        graph_seed_list = []
        for sample in tqdm(range(samples), desc=f"Samples for N={n}", leave=False):
            sample_file = os.path.join(n_dir, f"GraphSeed_N{n}_P{pVal}_Sample{sample}.pkl")
            if os.path.exists(sample_file):
               # Load existing adjacency matrix
               with open(sample_file, 'rb') as f:
                   seed = pickle.load(f)

            else:
                print('File not found!\nRun create_er_seed first.')
                return

            graph_seed_list.append(seed)

        graph_seed_dict[n] = graph_seed_list

    return graph_seed_dict


# Configuration variables
nMin = 3 
nMax = 1000
nList = list(range(nMin, nMax, 1))  # List of n values
pVal = 0.8
samples = 100
t = 50  # Assuming 't' is a given parameter for the filename

## Base directory
base_dir = "Datasets/Benchmark-SimpleQWAK_ER/GraphSeedFiles4"

create_er_seed(base_dir, nList, pVal, samples)
graph_seed_dict = load_er_seed(base_dir, nList, pVal, samples)
print(graph_seed_dict)
