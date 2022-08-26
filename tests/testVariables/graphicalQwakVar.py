import os as os
import sys

filePath = 'HardcodedValues'
fileName = 'graphicalQwakVarValues.txt'
base_path = os.path.abspath(os.path.dirname(__file__))
graphicalQwakVarValuesFile = os.path.join(base_path, filePath + os.sep + fileName)

with open(graphicalQwakVarValuesFile,'r') as f:
    graphicalQwakVarValues = f.readlines()

graphicalStaticProbDistCycle = eval(graphicalQwakVarValues[0])
graphicalDynamicProbDistCycle = eval(graphicalQwakVarValues[1])

graphicalStaticProbDistCycleNewInitState = eval(graphicalQwakVarValues[2])
graphicalDynamicProbDistCycleNewInitState = eval(graphicalQwakVarValues[3])

graphicalStaticProbDistCycleNewDim = eval(graphicalQwakVarValues[4])
graphicalDynamicProbDistCycleNewDim = eval(graphicalQwakVarValues[5])

graphicalStaticSetGraphCycleComplete = eval(graphicalQwakVarValues[6])
graphicalDynamicSetGraphCycleComplete = eval(graphicalQwakVarValues[7])

graphicalStaticSetTimeCycle = eval(graphicalQwakVarValues[8])
graphicalDynamicSetTimeCycle = eval(graphicalQwakVarValues[9])

graphicalDynamicGetMeanCycle = eval(graphicalQwakVarValues[10])

graphicalDynamicGetStDevCycle = eval(graphicalQwakVarValues[11])

graphicalDynamicGetSurvivalProbCycle = eval(graphicalQwakVarValues[12])