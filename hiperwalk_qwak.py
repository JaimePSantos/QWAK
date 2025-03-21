import numpy as np
import networkx as nx
from qwak.qwak import QWAK
import hiperwalk as hpw
from tqdm import tqdm
import os
import matplotlib.pyplot as plt


def run_qwak_walk(graph, time,gamma):
    vertex = len(graph) // 2
    qwak_instance = QWAK(graph, gamma=gamma)
    qwak_instance.runWalk(time=time, initStateList=[vertex])
    final_state_qwak = qwak_instance.getProbVec()
    print(final_state_qwak)
    return final_state_qwak

def run_hiperwalk(graph, time, gamma):
    numpy_graph = nx.to_numpy_array(graph)
    graph = hpw.Graph(numpy_graph)
    vertex = len(numpy_graph) // 2
    hiperwalk = hpw.ContinuousTime(graph=graph, gamma=gamma, time=time)
    state = hiperwalk.ket(vertex)
    final_state = hiperwalk.simulate(range=2, state=state)
    prob_vec = hiperwalk.probability_distribution(final_state)
    return prob_vec

def compare_walks(walk1, walk2, tolerance=1e-3):
    """
    Compare if two walks are the same within a given tolerance.

    Parameters:
    walk1 (np.ndarray): The first walk probability vector.
    walk2 (np.ndarray): The second walk probability vector.
    tolerance (float): The tolerance within which the walks are considered the same.

    Returns:
    bool: True if the walks are the same within the given tolerance, False otherwise.
    """
    return np.allclose(walk1, walk2, atol=tolerance)

def compare_walks_for_range(n_range, time_qwak, time_hiperwalk, gamma, tolerance=1e-3):
    """
    Compare QWAK and Hiperwalk for a range of n values, creating a cycle graph for each n,
    and print whether the probability vectors are close within the given tolerance.

    Parameters:
    n_range (range): The range of n values to iterate over.
    time_qwak (float): The time parameter for the QWAK walk.
    time_hiperwalk (float): The time parameter for the Hiperwalk walk.
    gamma (float): The gamma parameter for the walks.
    tolerance (float): The tolerance within which the walks are considered the same.
    """
    for n in n_range:
        graph = nx.cycle_graph(n)
        qwak_prob_vec = run_qwak_walk(graph, time_qwak, gamma)
        hiperwalk_prob_vec = run_hiperwalk(graph, time_hiperwalk, gamma)
        if compare_walks(qwak_prob_vec, hiperwalk_prob_vec, tolerance):
            print(f"For n={n}, the probability vectors are close within the given tolerance.")
        else:
            print(f"For n={n}, the probability vectors are not close within the given tolerance.")
            max_diff = np.max(np.abs(qwak_prob_vec - hiperwalk_prob_vec))
            print(f"Maximum difference: {max_diff}")


n = 100
time = 10
time_hiperwalk = time*10
gamma = 1/(2*np.sqrt(2))
gamma_hiperwalk = 1/(2*np.sqrt(2))
# gamma = 1
# gamma_hiperwalk = 1

graph = nx.cycle_graph(n)

qwak_prob_vec = run_qwak_walk(graph, time, gamma)
hiperwalk_prob_vec = run_hiperwalk(graph, time_hiperwalk, gamma)[-1]

plt.plot(hiperwalk_prob_vec, label='Hiperwalk Prob Vec')
plt.plot(qwak_prob_vec, label='QWAK Prob Vec')
plt.legend()
plt.show()

# Simple allclose test with tolerance
tolerance = 1e-3
if compare_walks(qwak_prob_vec, hiperwalk_prob_vec, tolerance):
    print("The probability vectors are close within the given tolerance.")
else:
    print("The probability vectors are not close within the given tolerance.")

# Use the compare_walks_for_range function
# time = 10
# time_hiperwalk = 100
# gamma = 1/(2*np.sqrt(2))
# n_range = range(3, 10, 1)
# tolerance = 1e-3

# compare_walks_for_range(n_range, time, time_hiperwalk, gamma, tolerance)