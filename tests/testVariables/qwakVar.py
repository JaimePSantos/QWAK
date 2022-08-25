import numpy as np
import networkx as nx
import os as os
import sys

filePath = 'HardcodedValues'
fileName = 'qwakVarValues.txt'
base_path = os.path.abspath(os.path.dirname(__file__))
qwakVarValuesFile = os.path.join(base_path, filePath + os.sep + fileName)

with open(qwakVarValuesFile,'r') as f:
    qwakVarValues = f.readlines()

probDistUniformSuperpositionCycle = eval(qwakVarValues[0])

probDistUniformSuperpositionComplete = eval(qwakVarValues[1])

probDistUniformSuperpositionCycleOriented = eval(qwakVarValues[2])

probDistUniformSuperpositionPath = eval(qwakVarValues[3])

probDistCustomStateCycle = eval(qwakVarValues[4])

probDistCycleNewDim = eval(qwakVarValues[5])
