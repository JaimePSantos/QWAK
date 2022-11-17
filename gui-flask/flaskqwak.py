import json

from flask import Flask, render_template, url_for, request, redirect
from pymongo import MongoClient
import networkx as nx
import numpy as np
from qwak.GraphicalQWAK import GraphicalQWAK
from bson import json_util
from dotenv import load_dotenv
import os

load_dotenv()
QWAKCLUSTER_USERNAME = os.environ.get('QWAKCLUSTER_USERNAME')
QWAKCLUSTER_PASSWORD = os.environ.get('QWAKCLUSTER_PASSWORD')

connection_string = f"mongodb+srv://{QWAKCLUSTER_USERNAME}:{QWAKCLUSTER_PASSWORD}@qwakcluster.kkszzg0.mongodb.net/test"

client = MongoClient(connection_string)
database = client.flask_db
probDistEntry = database.probDistEntry

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

@app.route('/setRunWalkDB',methods=['POST'])
def setRunWalkDB():
    print(request.method)
    if request.method == 'POST':
        name = str(request.form.get("walkName"))
        probDist = gQwak.runWalk()
        probDistEntry.insert_one({
            'name' : name,
            'hasError': probDist[0],
            'walkDim': gQwak.getStaticDim(),
            'walkTime': gQwak.getStaticTime(),
            'walkInit': gQwak.getStaticInitState(),
            'walkAdjacency': list(map(lambda x: str(x), gQwak.getStaticAdjacencyMatrix())),
            'probDist': probDist[1],
            'mean': gQwak.getStaticMean(),
            'sndMoment': gQwak.getStaticSndMoment(),
            'stDev': gQwak.getStaticStDev(),
            'invPartRatio': gQwak.getStaticInversePartRatio(),
        })
    return ("nothing")

@app.route('/getRunWalkDB',methods=['POST'])
def getRunWalkDB():
    prob = 0
    print(request.method)
    if request.method == 'POST':
        name = str(request.form.get("walkName"))
        prob = json.loads(json_util.dumps(probDistEntry.find_one({"name":name})))
    return prob

@app.route('/setRunMultipleWalksDB',methods=['POST','GET'])
def setRunMultipleWalksDB():
    print(request.method)
    if request.method == 'POST':
        name = str(request.form.get("walkName"))
        probDist = gQwak.runMultipleWalks()
        probDistEntry.insert_one({
            'name' : name,
            'hasError': probDist[0],
            'walkDim': gQwak.getDynamicDim(),
            'walkTime': gQwak.getDynamicTime().tolist(),
            'walkInit': gQwak.getDynamicInitStateList(),
            'walkAdjacency': list(map(lambda x: str(x), gQwak.getDynamicAdjacencyMatrix())),
            'probDist': probDist[1],
            'mean': gQwak.getDynamicMean(),
            'stDev': gQwak.getDynamicStDev(),
            'invPartRatio': gQwak.getDynamicInvPartRatio(),
        })
    return ("nothing")

@app.route('/getRunMultipleWalksDB',methods=['POST'])
def getRunMultipleWalksDB():
    prob = 0
    print(request.method)
    if request.method == 'POST':
        name = str(request.form.get("walkName"))
        prob = json.loads(json_util.dumps(probDistEntry.find_one({"name":name})))
    return prob

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

@app.route('/getDynamicStDev',methods=['GET','POST'])
def getDynamicStDev():
    return list(map(lambda x: round(x,resultRounding), gQwak.getDynamicStDev()))

@app.route('/getStaticInversePartRatio',methods=['GET','POST'])
def getStaticInversePartRatio():
    return [round(gQwak.getStaticInversePartRatio(), resultRounding)]

@app.route('/getDynamicInvPartRatio',methods=['GET','POST'])
def getDynamicInvPartRatio():
    return list(map(lambda x: round(x,resultRounding), gQwak.getDynamicInvPartRatio()))

@app.route('/getStaticSurvivalProb',methods=['GET','POST'])
def getStaticSurvivalProb():
    fromNode = str(request.form.get("fromNode"))
    toNode = str(request.form.get("toNode"))
    survProb = gQwak.getStaticSurvivalProb(fromNode, toNode)
    if not survProb[0]:
        survProb[1] = round(survProb[1], resultRounding)
    return survProb

@app.route('/getDynamicSurvivalProb',methods=['GET','POST'])
def getDynamicSurvivalProb():
    fromNode = str(request.form.get("fromNode"))
    toNode = str(request.form.get("toNode"))
    survProb = gQwak.getDynamicSurvivalProb(fromNode, toNode)
    if not survProb[0]:
        survProb[1] = list(map(lambda x: round(x,resultRounding),survProb[1]))
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

@app.route('/setDynamicCustomGraph',methods=['GET','POST'])
def setDynamicCustomGraph():
    customAdjacency = np.matrix(eval(request.form.get("customAdjacency")))
    gQwak.setDynamicCustomGraph(customAdjacency)
    return ("nothing")

@app.route('/deleteWalkEntry',methods=['POST'])
def deleteWalkEntry():
    print(request.method)
    if request.method == 'POST':
        name = str(request.form.get("walkName"))
        probDistEntry.delete_one({
            'name' : name,
        })
    return ("nothing")

@app.route('/deleteAllWalkEntries',methods=['POST'])
def deleteAllWalkEntries():
    print(request.method)
    if request.method == 'POST':
        probDistEntry.delete_many({})
    return ("nothing")

if __name__ == '__main__':
    app.run(debug=True)