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
    qwak_instance.runExpmWalk(time=time, initStateList=[vertex])
    final_state_qwak = qwak_instance.getProbVec()
    return final_state_qwak

def run_hiperwalk(graph, time, gamma):
    numpy_graph = nx.to_numpy_array(graph)
    graph = hpw.Graph(graph)
    vertex = len(numpy_graph) // 2
    hiperwalk = hpw.ContinuousTime(graph=graph, gamma=gamma, time=time)
    state = hiperwalk.ket(vertex)
    final_state = hiperwalk.simulate(range=2, state=state)
    prob_vec = hiperwalk.probability_distribution(final_state)
    return prob_vec

n = 100
time = 10
time_hiperwalk = 100
gamma = 1/(2*np.sqrt(2))
gamma_hiperwalk = 1/(2*np.sqrt(2))
# gamma = 1
# gamma_hiperwalk = 1

graph = nx.cycle_graph(n)

qwak_prob_vec = run_qwak_walk(graph, time, gamma)
hiperwalk_prob_vec = run_hiperwalk(graph, time, gamma)[-1]

plt.plot(hiperwalk_prob_vec, label='Hiperwalk Prob Vec')
plt.plot(qwak_prob_vec, label='QWAK Prob Vec')
plt.legend()
plt.show()

# print("QWAK Probability Vector:\n", qwak_prob_vec)
# print("\nHiperwalk Probability Vector:\n", hiperwalk_prob_vec)
# print("\nLast element of Hiperwalk Probability Vector:", hiperwalk_prob_vec[-1])

# tolerance = 1e-3
# if np.allclose(qwak_prob_vec, hiperwalk_prob_vec[-1], atol=tolerance):
#     print("\nThe last elements of both probability vectors are close within the given tolerance.")
# else:
#     print("\nThe last elements of both probability vectors are not close within the given tolerance.")
#     difference = np.abs(qwak_prob_vec - hiperwalk_prob_vec[-1])
#     percentage_difference = (difference / hiperwalk_prob_vec[-1]) * 100
#     print("Difference between the last elements of the probability vectors (as percentages):\n", percentage_difference)

# plt.plot(qwak_prob_vec, label='QWAK Prob Vec')
# plt.plot(hiperwalk_prob_vec, label='Hiperwalk Prob Vec')
# plt.legend()
# plt.show()