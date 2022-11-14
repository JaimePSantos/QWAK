import json

from flask import Flask, render_template, url_for, request
import networkx as nx
import numpy as np
from qwak.GraphicalQWAK import GraphicalQWAK
from django.http import JsonResponse
import requests


app = Flask(__name__)

staticN = 100
dynamicN = 100
t = 10
initState = [staticN // 2]
staticGraph = nx.cycle_graph(staticN)
dynamicGraph = nx.cycle_graph(dynamicN)
timeList = [0, 100]
initStateList = [[dynamicN // 2, (dynamicN // 2) + 1]]

gQwak = GraphicalQWAK(
    staticN,
    dynamicN,
    staticGraph,
    dynamicGraph,
    initState,
    initStateList,
    t,
    timeList)

resultRounding = 4

@app.route("/",methods=['GET', 'POST'])
@app.route("/home")
def home():
    return render_template('index.html')

@app.route("/staticQW")
def staticQW():
    return render_template('staticQW.html')

@app.route("/dynamicQW")
def dynamicQW():
    return render_template('dynamicQW.html')

@app.route('/setStaticGraph',methods=['GET','POST'])
def setStaticGraph():
    newGraph = request.form.get("newGraph")
    gQwak.setStaticGraph(newGraph)
    return ("nothing")

@app.route('/setDynamicGraph',methods=['GET','POST'])
def setDynamicGraph():
    newGraph = request.form.get("newGraph")
    gQwak.setDynamicGraph(newGraph)
    return ("nothing")

@app.route('/getStaticGraphToJson',methods=['GET','POST'])
def getStaticGraphToJson():
    return gQwak.getStaticGraphToJson()

@app.route('/getDynamicGraphToJson',methods=['GET','POST'])
def getDynamicGraphToJson():
    return gQwak.getDynamicGraphToJson()

@app.route('/setStaticDim',methods=['GET','POST'])
def setStaticDim():
    newDim = request.form.get("newDim")
    graphStr = request.form.get("graphStr")
    gQwak.setStaticDim(int(newDim), graphStr)
    return ("nothing")

@app.route('/setDynamicDim',methods=['GET','POST'])
def setDynamicDim():
    newDim = request.form.get("newDim")
    graphStr = request.form.get("graphStr")
    gQwak.setDynamicDim(int(newDim), graphStr)
    return ("nothing")

@app.route('/setStaticInitState',methods=['GET','POST'])
def setStaticInitState():
    initStateStr = request.form.get("initStateStr")
    gQwak.setStaticInitState(initStateStr)
    return ("nothing")

@app.route('/setDynamicInitStateList',methods=['GET','POST'])
def setDynamicInitStateList():
    initStateStr = request.form.get("initStateStr")
    gQwak.setDynamicInitStateList(initStateStr)
    return ("nothing")

@app.route('/setStaticTime',methods=['GET','POST'])
def setStaticTime():
    newTime = request.form.get("newTime")
    gQwak.setStaticTime(newTime)
    return ("nothing")

@app.route('/setDynamicTime',methods=['GET','POST'])
def setDynamicTime():
    newTime = request.form.get("newTime")
    gQwak.setDynamicTime(newTime)
    return ("nothing")

@app.route('/runWalk',methods=['GET','POST'])
def runWalk():
    return gQwak.runWalk()

@app.route('/runMultipleWalks',methods=['GET','POST'])
def runMultipleWalks():
    return gQwak.runMultipleWalks()

@app.route('/getStaticMean',methods=['GET','POST'])
def getStaticMean():
    return [round(gQwak.getStaticMean(), resultRounding)]

@app.route('/getDynamicMean',methods=['GET','POST'])
def getDynamicMean():
    return list(map(lambda x: round(x,resultRounding), gQwak.getDynamicMean()))

@app.route('/getStaticSndMoment',methods=['GET','POST'])
def getStaticSndMoment():
    return [round(gQwak.getStaticSndMoment(), resultRounding)]

@app.route('/getStaticStDev',methods=['GET','POST'])
def getStaticStDev():
    return [round(gQwak.getStaticStDev(), resultRounding)]

@app.route('/getStaticInversePartRatio',methods=['GET','POST'])
def getStaticInversePartRatio():
    return [round(gQwak.getStaticInversePartRatio(), resultRounding)]

@app.route('/getStaticSurvivalProb',methods=['GET','POST'])
def getStaticSurvivalProb():
    fromNode = str(request.form.get("fromNode"))
    toNode = str(request.form.get("toNode"))
    survProb = gQwak.getStaticSurvivalProb(fromNode, toNode)
    if not survProb[0]:
        survProb[1] = round(survProb[1], resultRounding)
    return survProb

@app.route('/checkPST',methods=['GET','POST'])
def checkPST():
    nodeA = str(request.form.get("nodeA"))
    nodeB = str(request.form.get("nodeB"))
    pst = gQwak.checkPST(nodeA, nodeB)
    return pst

@app.route('/setStaticCustomGraph',methods=['GET','POST'])
def setStaticCustomGraph():
    customAdjacency = np.matrix(eval(request.form.get("customAdjacency")))
    gQwak.setStaticCustomGraph(customAdjacency)
    return ("nothing")

if __name__ == '__main__':
    app.run(debug=True)