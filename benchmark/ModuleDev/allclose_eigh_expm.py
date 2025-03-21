import numpy as np
import networkx as nx
from qwak.qwak import QWAK
from tqdm import tqdm
import os
import matplotlib.pyplot as plt


def run_qwak_walk_normal_mode(graph_size, time):
    graph = nx.erdos_renyi_graph(graph_size, p=0.8, seed=10)
    qwak_instance = QWAK(graph)
    qwak_instance.runWalk(time=time, initStateList=[graph_size // 2])
    final_state_normal = qwak_instance.getProbVec()
    return final_state_normal


def run_qwak_walk_expm_mode(graph_size, time):
    graph = nx.erdos_renyi_graph(graph_size, p=0.8, seed=10)
    qwak_instance = QWAK(graph)
    qwak_instance.runExpmWalk(
        time=time, initStateList=[
            graph_size // 2])
    final_state_expm = qwak_instance.getProbVec()
    return final_state_expm


def compare_final_states(state1, state2):
    return np.allclose(state1, state2)


def create_results_folder(nlist, time):
    path = os.path.dirname(os.path.abspath(__file__))
    folder_name = f"AllCloseDatasets_Eigh-Expm_n{
        min(nlist)}-{max(nlist)}_t{time:.1f}"
    results_folder = os.path.join(path, folder_name)
    os.makedirs(results_folder, exist_ok=True)
    return results_folder


def plot_final_states(n, results_folder):
    n_folder = os.path.join(results_folder, f"n{n}")
    eigh_prob_vec_file = os.path.join(
        n_folder, f"eigh_prob_vec_n{n}.txt")
    expm_prob_vec_file = os.path.join(
        n_folder, f"expm_prob_vec_n{n}.txt")

    eigh_prob_vec = np.loadtxt(eigh_prob_vec_file)
    expm_prob_vec = np.loadtxt(expm_prob_vec_file)

    plt.figure(figsize=(10, 6))
    plt.plot(eigh_prob_vec, label=f'Eigh Prob Vec n{n}')
    plt.plot(expm_prob_vec, label=f'Expm Prob Vec n{n}')
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

        eigh_prob_vec_file = os.path.join(
            n_folder, f"eigh_prob_vec_n{n}.txt")
        expm_prob_vec_file = os.path.join(
            n_folder, f"expm_prob_vec_n{n}.txt")

        if not os.path.exists(eigh_prob_vec_file):
            final_state_normal = run_qwak_walk_normal_mode(n, time)
            np.savetxt(eigh_prob_vec_file, final_state_normal)
        else:
            final_state_normal = np.loadtxt(eigh_prob_vec_file)

        if not os.path.exists(expm_prob_vec_file):
            final_state_expm = run_qwak_walk_expm_mode(n, time)
            np.savetxt(expm_prob_vec_file, final_state_expm)
        else:
            final_state_expm = np.loadtxt(expm_prob_vec_file)

        comparison_result = compare_final_states(
            final_state_normal, final_state_expm)
        allclose_list.append(comparison_result)

    print("Allclose list:", allclose_list)

    while True:
        plot_prompt = input(
            "Do you want to plot any of the final states? (y/n): ").strip().lower()
        if plot_prompt == 'n':
            break
        graph_size = int(
            input("Enter the graph size to plot: ").strip())
        if graph_size in nlist:
            plot_final_states(graph_size, results_folder)
        else:
            print(
                f"Graph size {graph_size} is not in the provided range.")


if __name__ == "__main__":
    nlist = range(3, 1000)  # Graph sizes from 3 to 500
    time = 100  # Default time parameter
    main(nlist, time)
