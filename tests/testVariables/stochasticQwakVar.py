import os as os
import sys

filePath = 'HardcodedValues'
fileName = 'stochasticQwakVarValues.txt'
base_path = os.path.abspath(os.path.dirname(__file__))
stochasticQwakVarValuesFile = os.path.join(base_path, filePath + os.sep + fileName)

with open(stochasticQwakVarValuesFile,'r') as f:
    stochasticQwakVarValues = f.readlines()

stochasticProbDistSingleNodeCycleNoNoise = eval(stochasticQwakVarValues[0])

stochasticProbDistSingleNodeCycleNoise = eval(stochasticQwakVarValues[1])