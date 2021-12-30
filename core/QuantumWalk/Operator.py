import networkx as nx
import numpy as np

class Operator:
    """
    Class that represents the operators that will be used in a quantum walk.
    States are represented by matrices in quantum mechanics,
    therefore Numpy is used to generate ndarrays which contain these matrices.
    """

    def __init__(self, graph: nx.Graph) -> ():
        """
        Object is initialized with a user inputted graph, which is then used to
        generate the dimension of the operator and the adjacency matrix, which is
        the central structure required to perform walks on regular graphs. Note that this
        version of the software only supports regular undirected graphs, which will change
        in the future.
        The eigenvalues and eigenvectors of the adjacency matrix are also calculated at
        initialization, which are then used to calculate the diagonal operator for the walk.
        This is known as a spectral decomposition, and it was the chosen method since it is
        computationally cheaper than calculating the matrix exponent directly.

        Args:
            :param graph: Graph where the walk will be performed.
            :type graph: NetworkX.Graph
        """
        self._graph = graph
        self._adjacencyMatrix = nx.adjacency_matrix(graph).todense()
        self._n = len(graph)
        self._operator = np.zeros((self._n, self._n))
        self._eigenvalues, self._eigenvectors = np.linalg.eigh(
            self._adjacencyMatrix)
        self._time = 0
        self._gamma = 1

    def __mul__(self, other):
        """[summary]

        Args:
            other ([type]): [description]

        Returns:
            [type]: [description]
        """
        return self._operator * other

    def __rmul__(self, other):
        """[summary]

        Args:
            other ([type]): [description]

        Returns:
            [type]: [description]
        """
        return other * self._operator

    def __str__(self):
        """[summary]

        Returns:
            [type]: [description]
        """
        return '%s' % self._operator

    def buildDiagonalOperator(self, time=0, gamma=1):
        """[summary]

        Args:
            time (int, optional): [description]. Defaults to 0.
            gamma (int, optional): [description]. Defaults to 1.
        """
        self._time = time
        self._gamma = gamma
        D = np.diag(np.exp(-1j * self._time * self._gamma *
                           self._eigenvalues)).diagonal()
        self._operator = np.multiply(self._eigenvectors, D)
        self._operator = self._operator @ self._eigenvectors.H

    def setTime(self, newTime):
        """[summary]

        Args:
            newTime ([type]): [description]
        """
        self._time = newTime

    def getTime(self):
        """[summary]

        Returns:
            [type]: [description]
        """
        return self._time

    def setGamma(self, newGamma):
        """[summary]

        Args:
            newGamma ([type]): [description]
        """
        self._gamma = newGamma

    def getGamma(self):
        """[summary]

        Returns:
            [type]: [description]
        """
        return self._gamma

    def setDim(self, newDim):
        """[summary]

        Args:
            newDim ([type]): [description]
        """
        self._n = newDim

    def getDim(self):
        """[summary]

        Returns:
            [type]: [description]
        """
        return self._n

    def getAdjacencyMatrix(self):
        """[summary]

        Returns:
            [type]: [description]
        """
        return self._adjacencyMatrix

    def setAdjacencyMatrix(self, adjacencyMatrix):
        """[summary]

        Args:
            adjacencyMatrix ([type]): [description]
        """
        self._adjacencyMatrix = adjacencyMatrix

    def setOperator(self, newOperator):
        """[summary]

        Args:
            newOperator ([type]): [description]
        """
        self._n = newOperator.getDim()
        self._gamma = newOperator.getGamma()
        self._time = newOperator.getTime()
        self._operator = newOperator.getOperator()

    def getOperator(self):
        """[summary]

        Returns:
            [type]: [description]
        """
        return self._operator
