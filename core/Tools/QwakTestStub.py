import networkx as nx
import numpy as np

from Tools.Profiler import profile
from qwak.qwak import QWAK

import unittest


class QWAKTestStub(unittest.TestCase):

    def testProbDistUniformSuperposition(self):
       n = 100 
       t = 12 
       vec = [np.array([2.33566948e-23]), np.array([2.33555206e-23]), np.array([3.21405954e-22]), np.array([4.50789548e-21]), np.array([6.02254352e-20]), np.array([7.65703867e-19]), np.array([9.25021994e-18]), np.array([1.06018847e-16]), np.array([1.15088494e-15]), np.array([1.18120087e-14]), np.array([1.14399471e-13]), np.array([1.04335083e-12]), np.array([8.9405336e-12]), np.array([7.18051426e-11]), np.array([5.39059828e-10]), np.array([3.77154328e-09]), np.array([2.45117022e-08]), np.array([1.47436596e-07]), np.array([8.1737139e-07]), np.array([4.15696157e-06]), np.array([1.92899538e-05]), np.array([8.1162648e-05]), np.array([0.00030734]), np.array([0.00103811]), np.array([0.00309318]), np.array([0.00801674]), np.array([0.0177387]), np.array([0.03264987]), np.array([0.04807663]), np.array([0.05307457]), np.array([0.03873662]), np.array([0.01405194]), np.array([0.005279]), np.array([0.02110154]), np.array([0.03059605]), np.array([0.01457536]), np.array([0.00771127]), np.array([0.0225105]), np.array([0.01820895]), np.array([0.00800278]), np.array([0.01940289]), np.array([0.01472733]), np.array([0.0105186]), np.array([0.01830804]), np.array([0.01053605]), np.array([0.01525312]), np.array([0.01317469]), np.array([0.0130088]), np.array([0.01394557]), np.array([0.01280537]), np.array([0.01344478]), np.array([0.01344478]), np.array([0.01280537]), np.array([0.01394557]), np.array([0.0130088]), np.array([0.01317469]), np.array([0.01525312]), np.array([0.01053605]), np.array([0.01830804]), np.array([0.0105186]), np.array([0.01472733]), np.array([0.01940289]), np.array([0.00800278]), np.array([0.01820895]), np.array([0.0225105]), np.array([0.00771127]), np.array([0.01457536]), np.array([0.03059605]), np.array([0.02110154]), np.array([0.005279]), np.array([0.01405194]), np.array([0.03873662]), np.array([0.05307457]), np.array([0.04807663]), np.array([0.03264987]), np.array([0.0177387]), np.array([0.00801674]), np.array([0.00309318]), np.array([0.00103811]), np.array([0.00030734]), np.array([8.1162648e-05]), np.array([1.92899538e-05]), np.array([4.15696157e-06]), np.array([8.1737139e-07]), np.array([1.47436596e-07]), np.array([2.45117022e-08]), np.array([3.77154328e-09]), np.array([5.39059828e-10]), np.array([7.18051426e-11]), np.array([8.9405336e-12]), np.array([1.04335083e-12]), np.array([1.14399471e-13]), np.array([1.18120087e-14]), np.array([1.15088495e-15]), np.array([1.06018845e-16]), np.array([9.25021946e-18]), np.array([7.6570362e-19]), np.array([6.02252446e-20]), np.array([4.50786872e-21]), np.array([3.21394285e-22])] 
       graph = nx.cycle_graph(n)
       initStateList = [n // 2, n // 2 + 1]
       laplacian = False
       markedSearch = None
       self.qwak = QWAK(graph, laplacian, markedSearch)
       self.qwak.runWalk(t, initStateList)
       self.assertAlmostEqual(self.qwak.getProbDistVec(),vec)

#    def getMean(self):
#        return self.qwak.getMean()
#
#    def getSndMoment(self):
#        return self.qwak.getSndMoment()
#
#    def getStDev(self):
#        return self.qwak.getStDev()
#
#    def getSurvivalProb(self, k0, k1):
#        return self.qwak.getSurvivalProb(k0, k1)
#
#    def getInversePartRatio(self):
#        return self.qwak.getInversePartRatio()
