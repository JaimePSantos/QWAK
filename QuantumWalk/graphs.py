import numpy as np
from matplotlib.pyplot import *
from natsort import natsorted, ns #pip install natsort

class Graph(object):
    def __init__(self,graph_dict=None):
        if graph_dict == None: #inicializa um grafo caso nenhum seja dado
            graph_dict = {}
        self.__graph_dict = graph_dict
    
    def vertices(self):
        return list(self.__graph_dict.keys()) #devolve vertices
   
    def edges(self):
        return self.__generate_edges()

    def add_vertex(self,vertex):
        if vertex not in self.__graph_dict: #se o vertice nao esta no dicionario, chave vertice com lista vazia ]e adicionada???
            self.__graph_dict[vertex] = []
        
    def add_edge(self,edge):
        edge = set(edge)
        (vertex1,vertex2) = tuple(edge)
        if vertex1 in self.__graph_dict:
            self.__graph_dict[vertex1].append(vertex2)
            self.__graph_dict[vertex2].append(vertex1)
        else:
            self.__graph_dict[vertex1] = [vertex2]

    def __generate_edges(self):
        edges=[]
        for vertex in self.__graph_dict:
            for neighbour in self.__graph_dict[vertex]:
                if {neighbour,vertex} not in edges:
                    edges.append({vertex,neighbour})
        return edges
    
    def linegraph(self,N):
        for i in range(N):
            self.add_vertex(str(i))
        i = 0
        self.add_edge({str(i), str(i+1)})
        for i in range(1,(N-1)):
            v1 = str(i)
            v2 = str(i+1)
            self.add_edge({v1,v2})
        i = N-1
        self.add_edge({str(i), str(0)})
        return self

    def bipartite_linegraph(self,N):
        k=0
        for i in range(0,2*N):
            self.add_vertex(str(i))
        for i in range(0,N-1):
            z = str(k)
            k = (k+N+1)%(2*N)
            y = str(k)
            self.add_edge({z,y})
        self.add_edge({str(0),str(2*(N)-1)})
        self.add_edge({str(N),str(N-1)})
        k=N
        for i in range(N,(2*N)-1):
            z = str(k)
            k=(k+N+1)%(2*N)
            y=str(k)
            self.add_edge({z,y})
        return self

    def __str__(self):
        res = "vertices: "
        for k in self.__graph_dict:
            res += str(k) + " "
        res += "\nedges: "
        for edge in self.__generate_edges():
            res += str(edge) + " "
        return res

    def find_path(self,start_vertex,end_vertex,path=None):
        if path == None:
            path = []
        graph = self.__graph_dict
        path = path + [start_vertex]
        if start_vertex == end_vertex:
            return path
        if start_vertex not in graph:
            return None
        for vertex in graph[start_vertex]:
            if vertex not in path:
                extended_path = self.find_path(vertex,end_vertex,path)
                if extended_path:
                    return extended_path
        return None

    def find_all_paths(self,start_vertex,end_vertex,path=[]):
        graph = self.__graph_dict
        path = path + [start_vertex]
        if start_vertex == end_vertex:
            return [path]
        if start_vertex not in graph:
            return []
        paths = []
        for vertex in graph[start_vertex]:
            if vertex not in path:
                extended_paths = self.find_all_paths(vertex,end_vertex,path)
                for p in extended_paths:
                    paths.append(p)
        return paths
        
    def adjacency_list(self):
        k = len(self.__graph_dict)
        if k >=1:
            return[str(key) + ":" +str(self.__graph_dict[key]) for key in self.__graph_dict.keys()]
        else:
            return dict()

    def adjacency_matrix(self):
         k = len(self.__graph_dict)
         if  k>=1:
            self.vertex_names = natsorted(self.__graph_dict.keys()) #substituir natsorted para remover dependencia
            self.vertex_indices = dict(zip(self.vertex_names,range(len(self.vertex_names)))) #faz tuplo (a,0),(b,1) e mete num dicionario
            self.adjacencymatrix = np.zeros(shape=(k,k))
            for i in range(k):
                for j in self.__graph_dict[self.vertex_names[i]]:
                    self.adjacencymatrix[i][self.vertex_indices[j]] = 1
            return self.adjacencymatrix
            
         else:
            return dict()
        
    def is_adjacent(self,vertex1,vertex2):
        if vertex2 in self.__graph_dict[vertex1]:
            return True
        else:
            return False

    def vertex_degree(self,vertex):
        adj_vertices = self.__graph_dict[vertex]
        degree = len(adj_vertices) + adj_vertices.count(vertex) #loop conta como 2
        return degree
    
    def vertex_degreeprob(self,vertex):
        adj_vertices = self.__graph_dict[vertex]
        degreeprob = 1/(len(adj_vertices) + adj_vertices.count(vertex)) #loop conta como 2
        return degreeprob
    
    def degree_matrix(self):
        k = len(self.__graph_dict)
        self.degmatrix = np.zeros(shape=(k,k))
        for i in range(0,k):
            for j in range(0,k):
                if(j==i):
                    str(self.vertex_names)
                    self.degmatrix[i][j] = self.vertex_degree(self.vertex_names[i])
        return self.degmatrix
    
    def laplacian(self):
        return self.degmatrix - self.adjacencymatrix









##################################TESTS##########################################################
# N=4
# g = Graph({})
# graph = g.bipartite_linegraph(N)
# i=0
# v= graph.vertex_degreeprob(str(i))
# print(v)
# adjl = graph.adjacency_list()
# adjm = graph.adjacency_matrix()
# print(adjm)
# print(adjl)
#print(graph)
