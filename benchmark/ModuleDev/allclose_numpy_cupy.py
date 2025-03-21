import numpy as np
import networkx as nx
from qwak.qwak import QWAK as QWAK_numpy
from qwak_cupy.qwak import QWAK as QWAK_cupy
from tqdm import tqdm
import os
import matplotlib.pyplot as plt

def run_qwak_walk_numpy_mode(graph_size,time):
    graph = nx.erdos_renyi_graph(graph_size, p=0.8, seed=10)
    # graph = nx.cycle_graph(graph_size)
    qwak_instance = QWAK_numpy(graph)
    qwak_instance.runWalk(time=time, initStateList=[graph_size//2])
    final_state_numpy = qwak_instance.getProbVec()
    return final_state_numpy

def run_qwak_walk_cupy_mode(graph_size,time):
    graph = nx.erdos_renyi_graph(graph_size, p=0.8, seed=10)
    # graph = nx.cycle_graph(graph_size)
    qwak_instance = QWAK_cupy(graph)
    qwak_instance.runWalk(time=time, initStateList=[graph_size//2])
    final_state_cupy = qwak_instance.getProbVec()
    return final_state_cupy

def compare_final_states(state1, state2):
    return np.allclose(state1, state2)

def create_results_folder(nlist, time):
    path = os.path.dirname(os.path.abspath(__file__))
    folder_name = f"AllCloseDatasets_Numpy-Cupy_n{min(nlist)}-{max(nlist)}_t{time:.1f}"
    results_folder = os.path.join(path, folder_name)
    os.makedirs(results_folder, exist_ok=True)
    return results_folder

def plot_final_states(n, results_folder):
    n_folder = os.path.join(results_folder, f"n{n}")
    numpy_prob_vec_file = os.path.join(n_folder, f"numpy_prob_vec_n{n}.txt")
    cupy_prob_vec_file = os.path.join(n_folder, f"cupy_prob_vec_n{n}.txt")
    
    numpy_prob_vec = np.loadtxt(numpy_prob_vec_file)
    cupy_prob_vec = np.loadtxt(cupy_prob_vec_file)
    
    plt.figure(figsize=(10, 6))
    plt.plot(numpy_prob_vec, label=f'Numpy Prob Vec n{n}')
    plt.plot(cupy_prob_vec, label=f'Cupy Prob Vec n{n}')
    plt.xlabel('Node')
    plt.ylabel('Probability')
    plt.title(f'Probability Vectors for Graph Size {n}')
    plt.legend()
    plt.show()

def main(nlist, time):
    results_folder = create_results_folder(nlist, time)
    allclose_list = []
    for n in tqdm(nlist, desc="Processing graph sizes"):
        n_folder = os.path.join(results_folder, f"n{n}")
        os.makedirs(n_folder, exist_ok=True)
        
        numpy_prob_vec_file = os.path.join(n_folder, f"numpy_prob_vec_n{n}.txt")
        cupy_prob_vec_file = os.path.join(n_folder, f"cupy_prob_vec_n{n}.txt")
        
        if not os.path.exists(numpy_prob_vec_file):
            final_state_numpy = run_qwak_walk_numpy_mode(n,time)
            np.savetxt(numpy_prob_vec_file, final_state_numpy)
        else:
            final_state_numpy = np.loadtxt(numpy_prob_vec_file)
        
        if not os.path.exists(cupy_prob_vec_file):
            final_state_cupy = run_qwak_walk_cupy_mode(n,time)
            np.savetxt(cupy_prob_vec_file, final_state_cupy)
        else:
            final_state_cupy = np.loadtxt(cupy_prob_vec_file)
        
        comparison_result = compare_final_states(final_state_numpy, final_state_cupy)
        allclose_list.append(comparison_result)
    
    print("Allclose list:", allclose_list)
    
    while True:
        plot_prompt = input("Do you want to plot any of the final states? (y/n): ").strip().lower()
        if plot_prompt == 'n':
            break
        graph_size = int(input("Enter the graph size to plot: ").strip())
        if graph_size in nlist:
            plot_final_states(graph_size, results_folder)
        else:
            print(f"Graph size {graph_size} is not in the provided range.")

if __name__ == "__main__":
    nlist = range(3, 1000)  # Graph sizes from 3 to 1000
    time = 100 # Default time parameter
    main(nlist, time)
