from qwak.State import State
from qwak.Operator import Operator
from qwak.QuantumWalk import QuantumWalk
from qwak.ProbabilityDistribution import ProbabilityDistribution
from qwak.qwak import QWAK

import networkx as nx
import numpy as np
from matplotlib import pyplot as plt
import timeit
import sympy as sp
from sympy.abc import pi
from math import sqrt, ceil, pow

n = 2
N = 2**n
graph = nx.hypercube_graph(n)

initNodes = [0]
initState = State(N,initNodes)
initState.buildState()

operator = Operator(graph)
operator.buildDiagonalOperator(time=0.5)

quantumWalk = QuantumWalk(initState,operator)
quantumWalk.buildWalk()
finalState = quantumWalk.getFinalState()

probDist = ProbabilityDistribution(finalState)
probDist.buildProbDist()

# plt.plot(probDist.getProbVec())
# plt.show()
adjM = sp.Matrix(operator.getAdjacencyMatrix().real)
print(operator.getAdjacencyMatrix())
print(adjM.is_diagonalizable())
p , d = adjM.diagonalize()
print(p)

import numpy as np
from scipy.linalg import eigh

# Convert the SymPy matrix to a NumPy array
M = np.array(adjM.tolist()).astype(np.float64)

# Compute the eigenvalues and eigenvectors
# Using eigh instead of eig as our matrix is Hermitian (symmetric in this case)
eigenvalues, eigenvectors = eigh(M)

# Create a diagonal matrix from the eigenvalues
D = np.diag(eigenvalues)

# The matrix P of eigenvectors, in the same order as their corresponding eigenvalues, forms the basis
P = eigenvectors
print(P)

# Compute P^-1 * M * P and verify that it equals D
P_inv = np.linalg.inv(P)
result = np.matmul(P_inv, np.matmul(M, P))

# print("Matrix D:\n", D)
# print("\nP^-1 * M * P:\n", result)

# Check if D equals to P^-1 * M * P
if np.allclose(D, result):
    print("\nD equals P^-1 * M * P. The matrix is successfully diagonalized.")
else:
    print("\nD doesn't equal P^-1 * M * P. Something went wrong.")