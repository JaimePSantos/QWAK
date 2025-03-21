import numpy as np
import networkx as nx
from qwak.qwak import QWAK
import hiperwalk as hpw
from tqdm import tqdm
import os
import matplotlib.pyplot as plt
# 

def run_qwak_walk(graph, time,gamma):
    vertex = len(graph) // 2
    qwak_instance = QWAK(graph, gamma=gamma)
    qwak_instance.runExpmWalk(time=time, initStateList=[vertex])
    final_state_qwak = qwak_instance.getProbVec()
    return final_state_qwak

def run_hiperwalk(graph, time_hiperwalk, gamma):
    numpy_graph = nx.to_numpy_array(graph)
    graph = hpw.Graph(numpy_graph)
    vertex = len(numpy_graph) // 2
    hiperwalk = hpw.ContinuousTime(graph=graph, gamma=gamma, time=time_hiperwalk)
    state = hiperwalk.ket(vertex)
    final_state = hiperwalk.simulate(range=2, state=state)
    prob_vec = hiperwalk.probability_distribution(final_state)
    return prob_vec[-1]

def compare_final_states(state1, state2):
    return np.allclose(state1, state2,atol=1e-03)

def create_results_folder(nlist, time):
    path = os.path.dirname(os.path.abspath(__file__))
    folder_name = f"AllCloseDatasets_QWAK-Hiperwalk_n{min(nlist)}-{max(nlist)}_t{time:.1f}"
    results_folder = os.path.join(path, folder_name)
    os.makedirs(results_folder, exist_ok=True)
    return results_folder

def plot_final_states(n, results_folder):
    n_folder = os.path.join(results_folder, f"n{n}")
    qwak_prob_vec_file = os.path.join(n_folder, f"qwak_prob_vec_n{n}.txt")
    hiperwalk_prob_vec_file = os.path.join(n_folder, f"hiperwalk_prob_vec_n{n}.txt")
    
    qwak_prob_vec = np.loadtxt(qwak_prob_vec_file)
    hiperwalk_prob_vec = np.loadtxt(hiperwalk_prob_vec_file)
    
    plt.figure(figsize=(10, 6))
    plt.plot(qwak_prob_vec, label=f'QWAK Prob Vec n{n}')
    plt.plot(hiperwalk_prob_vec, label=f'Hiperwalk Prob Vec n{n}')
    plt.xlabel('Node')
    plt.ylabel('Probability')
    plt.title(f'Probability Vectors for Graph Size {n}')
    plt.legend()
    plt.show()

def main(nlist, time,time_hiperwalk):
    results_folder = create_results_folder(nlist, time)
    allclose_list = []
    for n in tqdm(nlist, desc="Processing graph sizes"):
        n_folder = os.path.join(results_folder, f"n{n}")
        os.makedirs(n_folder, exist_ok=True)
        
        qwak_prob_vec_file = os.path.join(n_folder, f"qwak_prob_vec_n{n}.txt")
        hiperwalk_prob_vec_file = os.path.join(n_folder, f"hiperwalk_prob_vec_n{n}.txt")
        
        if not os.path.exists(qwak_prob_vec_file):
            graph = nx.cycle_graph(n)
            final_state_qwak = run_qwak_walk(graph, time, gamma=1/(2*np.sqrt(2)))
            np.savetxt(qwak_prob_vec_file, final_state_qwak)
        else:
            final_state_qwak = np.loadtxt(qwak_prob_vec_file)
        
        if not os.path.exists(hiperwalk_prob_vec_file):
            graph = nx.cycle_graph(n)
            final_state_hiperwalk = run_hiperwalk(graph, time_hiperwalk, gamma=1/(2*np.sqrt(2)))
            np.savetxt(hiperwalk_prob_vec_file, final_state_hiperwalk)
        else:
            final_state_hiperwalk = np.loadtxt(hiperwalk_prob_vec_file)
        
        comparison_result = compare_final_states(final_state_qwak, final_state_hiperwalk)
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
    nlist = range(3, 100)  # Graph sizes from 3 to 100
    time = 10  # Default time parameter
    time_hiperwalk = 100
    main(nlist, time, time_hiperwalk)
