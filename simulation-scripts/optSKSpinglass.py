import networkx as nx
from matplotlib import pyplot as plt
import numpy as np
import math
import scipy.special as sp
from scipy.linalg import expm

nQubits = 5
targetQubit = 3
n = 2**nQubits

zGate = np.array([[1,0],[0,-1]])

idGate = np.array([[1,0],[0,1]])

largeIdGate = idGate
largeIdGate2 = idGate

for i in range(0,targetQubit-1):
    largeIdGate = np.kron(idGate,largeIdGate)

for i in range(targetQubit+1,nQubits-1):
    largeIdGate2 = np.kron(idGate,largeIdGate2)

print()
print(largeIdGate2)
largeZGate = np.kron(np.kron(largeIdGate, zGate),largeIdGate2)

print(len(largeZGate))
print(largeZGate)

print(f'largeIdGate {largeIdGate}\n\n'
      f'largeIdGate2 {largeIdGate2}\n\n'
      f'largeZGate {largeZGate}\n\n'
      f'length largeIdGate -> \t{len(largeIdGate)}\n'
      f'length largeIdGate2 -> \t{len(largeIdGate2)}\n'
      f'length largeZGate -> \t{len(largeZGate)}')