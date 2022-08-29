import numpy as np
import networkx as nx

n = 100
H = nx.cycle_graph(n, create_using=nx.DiGraph)
G = H.reverse()
alpha = np.pi / 2

for u, v, d in H.edges(data=True):
    d["weight"] = np.exp(1j * alpha)
    mat = np.matrix(d["weight"])

for u, v, d in G.edges(data=True):
    d["weight"] = np.exp(-1j * alpha)
    mat = np.matrix(d["weight"])

orientedGraph = nx.compose(H, G)
