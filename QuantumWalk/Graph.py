import networkx as nx
import matplotlib.pyplot as plt

class Graph2:
    def __init__(self):
        self._graph = nx.Graph()

    def addNode(self,node):
        self._graph.add_node(node)

    def addEdge(self,u_of_edge, v_of_edge, **attr):
        self._graph.add_edge(u_of_edge, v_of_edge, **attr)

    def completeGraph(self,n):
        self._graph = nx.complete_graph(n)

    def setGraph(self,newGraph):
        self._graph = newGraph

    def getGraph(self):
        return self._graph

    def drawGraph(self):
        nx.draw(self._graph)