import networkx as nx
import numpy as np
from numpy.linalg import eigh

class QuantumWalk:
    def __init__(self, graph = nx.Graph()):
        self.graph                          = graph
        self.adjacency                      = self.graph2matrix()
        self.eigenvalues, self.eigenvectors = self.matrix2spectrum() 

           
    def graph2matrix(self):
        return nx.adjacency_matrix(self.graph).todense()
    
    def matrix2spectrum(self):
        return eigh(self.adjacency)
        
    def evolution(self, t = 0, initial = None):
        D = -1j*t*self.eigenvalues
        D = np.diag(D)
        
        U = (self.eigenvectors @ D @ self.eigenvectors.H)
        
        return np.abs(np.array(U @ initial))**2
             