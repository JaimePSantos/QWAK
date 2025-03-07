import networkx as nx
import numpy as np
import matplotlib.pyplot as plt
from qwak.StochasticQwak import StochasticQWAK
from Maze import Maze
import numpy as np
import matplotlib.pyplot as plt
from random import randrange, shuffle

maze_graph = Maze(maze_size=(10,10))
maze_graph.plot_maze()
plt.show()

graph = nx.from_numpy_array(maze_graph.adjacency)
qwak = StochasticQWAK(graph,noiseParam=0.1,sinkNode=99,sinkRate=0.99)

exit_prob = []
exit_prob_opt = []
exit_prob_class = []

times = []

for i in range(10):
  t=100*i
  initState = [0]
  qwak.runWalk(t,initState)

  probVec = qwak.getProbVec()
  exit_prob_opt.append(probVec[-1])
  exit_prob.append(probVec[-1])
  exit_prob_class.append(probVec[-1])
  times.append(t)

plt.plot(times,exit_prob, label=r'$p=0$')
plt.plot(times,exit_prob_class, label=r'$p=1$')
plt.plot(times,exit_prob_opt, label=r'$p=0.1$')
plt.xlabel('time')
plt.ylabel('Exit probability')
plt.legend()
plt.show()