import json

from flask import Flask, render_template, url_for, request, redirect, session
from flask_session import Session
from pymongo import MongoClient
import networkx as nx
import numpy as np
from qwak.GraphicalQWAK import GraphicalQWAK
from qwak.State import State
from qwak.qwak import QWAK
from qwak.Errors import StateOutOfBounds, UndefinedTimeList, EmptyProbDistList, MissingNodeInput
from bson import json_util
from dotenv import load_dotenv
import os
import random

load_dotenv()
QWAKCLUSTER_USERNAME = os.environ.get('QWAKCLUSTER_USERNAME')
QWAKCLUSTER_PASSWORD = os.environ.get('QWAKCLUSTER_PASSWORD')

connection_string = f"mongodb+srv://{QWAKCLUSTER_USERNAME}:{QWAKCLUSTER_PASSWORD}@qwakcluster.kkszzg0.mongodb.net/test"

client = MongoClient('localhost', 27017)
# client = MongoClient(connection_string)
db_string = 'qwak_flask'
database = client.get_database(db_string)
probDistEntry = database['probDistEntry']

app = Flask(__name__)
SESSION_TYPE = 'filesystem'
app.config.from_object(__name__)
Session(app)

staticN = 5
dynamicN = 5
t = 1
initState = [staticN // 2]
staticGraph = nx.cycle_graph(staticN)
dynamicGraph = nx.cycle_graph(dynamicN)
timeList = [0, 1]
initStateList = [[dynamicN // 2, (dynamicN // 2) + 1]]

resultRounding = 4

@app.route("/",methods=['GET', 'POST'])
@app.route("/home")
def home():
    if not session.get('sessionId'):
        sessionId = f'user{len(database.list_collection_names())+1}'
        session['sessionId'] = sessionId
        sessionCollection = database[sessionId]
        sessionCollection.insert_one({'init':sessionId})
        gQwak = GraphicalQWAK(
            staticN=staticN,
            dynamicN=dynamicN,
            staticGraph=staticGraph,
            dynamicGraph=dynamicGraph,
            staticStateList=initState,
            dynamicStateList=initStateList,
            staticTime=t,
            dynamicTimeList=timeList,
            qwakId=session['sessionId'])
        sessionCollection.insert_one(json.loads(gQwak.to_json()))

    return render_template('index.html')

@app.route("/staticQW")
def staticQW():
    if not session.get('staticQwakId'):
        staticQwakId = f"StaticQWAK_{session['sessionId']}"
        session['staticQwakId'] = staticQwakId
        sessionCollection = database[session['sessionId']]
        staticN = 5
        staticGraph = nx.cycle_graph(staticN)
        staticQWAK = QWAK(graph=staticGraph, qwakId=session['staticQwakId'])
        sessionCollection.insert_one(json.loads(staticQWAK.to_json()))
    return render_template('staticQW.html')

@app.route("/dynamicQW")
def dynamicQW():
    sessionCollection = database[session['sessionId']]
    sessionId = session['sessionId']
    return render_template('dynamicQW.html')

@app.route('/setStaticGraph',methods=['GET','POST'])
def setStaticGraph():
    sessionCollection = database[session['sessionId']]
    staticQWAK = QWAK.from_json(sessionCollection.find_one({'qwakId':session['staticQwakId']}))
    newDim = int(request.form.get("newDim"))
    newGraph = request.form.get("newGraph")
    staticQWAK.setDim(newDim,graphStr=newGraph)
    staticQWAK.setGraph(eval(f"{newGraph}({staticQWAK.getDim()})"))
    sessionCollection.replace_one({'qwakId': session['staticQwakId']},json.loads(staticQWAK.to_json()))
    return nx.cytoscape_data(staticQWAK.getGraph())

@app.route('/setDynamicGraph',methods=['GET','POST'])
def setDynamicGraph():
    sessionCollection = database[session['sessionId']]
    sessionId = session['sessionId']
    gQwak = GraphicalQWAK.from_json(sessionCollection.find_one({'qwakId': sessionId}))
    newGraph = request.form.get("newGraph")
    gQwak.setDynamicGraph(newGraph)
    sessionCollection.replace_one({'qwakId': sessionId},json.loads(gQwak.to_json()))
    return ("nothing")

@app.route('/getStaticGraphToJson',methods=['GET','POST'])
def getStaticGraphToJson():
    sessionCollection = database[session['sessionId']]
    staticQWAK = QWAK.from_json(sessionCollection.find_one({'qwakId':session['staticQwakId']}))
    return nx.cytoscape_data(staticQWAK.getGraph())

@app.route('/getDynamicGraphToJson',methods=['GET','POST'])
def getDynamicGraphToJson():
    sessionCollection = database[session['sessionId']]
    sessionId = session['sessionId']
    gQwak = GraphicalQWAK.from_json(sessionCollection.find_one({'qwakId': sessionId}))
    return gQwak.getDynamicGraphToJson()

@app.route('/setStaticDim',methods=['GET','POST'])
def setStaticDim():
    sessionCollection = database[session['sessionId']]
    staticQWAK = QWAK.from_json(sessionCollection.find_one({'qwakId':session['staticQwakId']}))
    newDim = request.form.get("newDim")
    graphStr = request.form.get("graphStr")
    staticQWAK.setDim(int(newDim), graphStr)
    sessionCollection.replace_one({'qwakId': session['staticQwakId']},json.loads(staticQWAK.to_json()))
    return ("nothing")

@app.route('/setDynamicDim',methods=['GET','POST'])
def setDynamicDim():
    sessionCollection = database[session['sessionId']]
    sessionId = session['sessionId']
    gQwak = GraphicalQWAK.from_json(sessionCollection.find_one({'qwakId': sessionId}))
    newDim = request.form.get("newDim")
    graphStr = request.form.get("graphStr")
    gQwak.setDynamicDim(int(newDim), graphStr)
    sessionCollection.replace_one({'qwakId': sessionId},json.loads(gQwak.to_json()))
    return ("nothing")

@app.route('/setStaticInitState',methods=['GET','POST'])
def setStaticInitState():
    sessionCollection = database[session['sessionId']]
    sessionId = session['sessionId']
    gQwak = GraphicalQWAK.from_json(sessionCollection.find_one({'qwakId':sessionId}))
    initStateStr = request.form.get("initStateStr")
    gQwak.setStaticInitState(initStateStr)
    sessionCollection.replace_one({'qwakId': sessionId},json.loads(gQwak.to_json()))
    return ("nothing")

@app.route('/setDynamicInitStateList',methods=['GET','POST'])
def setDynamicInitStateList():
    sessionCollection = database[session['sessionId']]
    sessionId = session['sessionId']
    gQwak = GraphicalQWAK.from_json(sessionCollection.find_one({'qwakId': sessionId}))
    initStateStr = request.form.get("initStateStr")
    gQwak.setDynamicInitStateList(initStateStr)
    sessionCollection.replace_one({'qwakId': sessionId},json.loads(gQwak.to_json()))
    return ("nothing")

@app.route('/setStaticTime',methods=['GET','POST'])
def setStaticTime():
    sessionCollection = database[session['sessionId']]
    sessionId = session['sessionId']
    gQwak = GraphicalQWAK.from_json(sessionCollection.find_one({'qwakId':sessionId}))
    newTime = request.form.get("newTime")
    gQwak.setStaticTime(newTime)
    sessionCollection.replace_one({'qwakId': sessionId},json.loads(gQwak.to_json()))
    return ("nothing")

@app.route('/setDynamicTime',methods=['GET','POST'])
def setDynamicTime():
    sessionCollection = database[session['sessionId']]
    sessionId = session['sessionId']
    gQwak = GraphicalQWAK.from_json(sessionCollection.find_one({'qwakId': sessionId}))
    newTime = request.form.get("newTime")
    gQwak.setDynamicTime(newTime)
    sessionCollection.replace_one({'qwakId': sessionId},json.loads(gQwak.to_json()))
    return ("nothing")

@app.route('/setRunWalkDB',methods=['POST'])
def setRunWalkDB():
    if request.method == 'POST':
        sessionCollection = database[session['sessionId']]

        newDim = int(request.form.get("newDim"))
        newGraphStr = request.form.get("newGraph")
        newGraph = eval(newGraphStr + f"({newDim})")

        newTime = eval(request.form.get("newTime"))
        newInitCond = request.form.get("newInitCond")
        initCondList = list(map(int, newInitCond.split(",")))

        staticQWAK = QWAK.from_json(sessionCollection.find_one({'qwakId': session['staticQwakId']}))
        staticQWAK.setDim(newDim, newGraphStr)
        staticQWAK.setGraph(newGraph)
        staticQWAK.setTime(newTime)
        newState = State(staticQWAK.getDim())
        newState.buildState(initCondList)
        staticQWAK.setInitState(newState)
        # TODO: SOME WAY TO CATCH THE ERROR HERE
        staticQWAK.runWalk()
        sessionCollection.replace_one({'qwakId': session['staticQwakId']}, json.loads(staticQWAK.to_json()))
    return ("nothing")

@app.route('/getRunWalkDB',methods=['POST'])
def getRunWalkDB():
    prob = 0
    print(request.method)
    if request.method == 'POST':
        sessionCollection = database[session['sessionId']]
        try:
            staticQWAK = QWAK.from_json(sessionCollection.find_one({'qwakId': session['staticQwakId']}))
            resultDict = {
                'prob': staticQWAK.getProbVec().tolist(),
                'mean': staticQWAK.getMean(),
                'sndMoment': staticQWAK.getSndMoment(),
                'stDev': staticQWAK.getStDev(),
                'invPartRatio': staticQWAK.getInversePartRatio()
            }
        except StateOutOfBounds as err:
            return [True, str(err)]
    return [False,resultDict]

@app.route('/setRunMultipleWalksDB',methods=['POST','GET'])
def setRunMultipleWalksDB():
    print(request.method)
    if request.method == 'POST':
        sessionCollection = database[session['sessionId']]
        sessionId = session['sessionId']
        gQwak = GraphicalQWAK.from_json(sessionCollection.find_one({'qwakId': sessionId}))
        name = str(request.form.get("walkName"))
        probDist = gQwak.runMultipleWalks()
        sessionCollection.replace_one({'qwakId': sessionId}, json.loads(gQwak.to_json()))
    return ("nothing")

@app.route('/getRunMultipleWalksDB',methods=['POST'])
def getRunMultipleWalksDB():
    prob = []
    print(request.method)
    if request.method == 'POST':
        sessionCollection = database[session['sessionId']]
        sessionId = session['sessionId']
        gQwak = GraphicalQWAK.from_json(sessionCollection.find_one({'qwakId': sessionId}))
        name = str(request.form.get("walkName"))
        prob = gQwak.getDynamicProbVecList().tolist()
    return prob

@app.route('/runMultipleWalks',methods=['GET','POST'])
def runMultipleWalks():
    sessionCollection = database[session['sessionId']]
    sessionId = session['sessionId']
    gQwak = GraphicalQWAK.from_json(sessionCollection.find_one({'qwakId': sessionId}))
    return gQwak.runMultipleWalks()

@app.route('/getStaticMean',methods=['GET','POST'])
def getStaticMean():
    sessionCollection = database[session['sessionId']]
    sessionId = session['sessionId']
    gQwak = GraphicalQWAK.from_json(sessionCollection.find_one({'qwakId': sessionId}))
    return [round(gQwak.getStaticMean(), resultRounding)]

@app.route('/getDynamicMean',methods=['GET','POST'])
def getDynamicMean():
    sessionCollection = database[session['sessionId']]
    sessionId = session['sessionId']
    gQwak = GraphicalQWAK.from_json(sessionCollection.find_one({'qwakId': sessionId}))
    return list(map(lambda x: round(x,resultRounding), gQwak.getDynamicMean()))

@app.route('/getStaticSndMoment',methods=['GET','POST'])
def getStaticSndMoment():
    sessionCollection = database[session['sessionId']]
    sessionId = session['sessionId']
    gQwak = GraphicalQWAK.from_json(sessionCollection.find_one({'qwakId': sessionId}))
    return [round(gQwak.getStaticSndMoment(), resultRounding)]

@app.route('/getStaticStDev',methods=['GET','POST'])
def getStaticStDev():
    sessionCollection = database[session['sessionId']]
    sessionId = session['sessionId']
    gQwak = GraphicalQWAK.from_json(sessionCollection.find_one({'qwakId': sessionId}))
    return [round(gQwak.getStaticStDev(), resultRounding)]

@app.route('/getDynamicStDev',methods=['GET','POST'])
def getDynamicStDev():
    sessionCollection = database[session['sessionId']]
    sessionId = session['sessionId']
    gQwak = GraphicalQWAK.from_json(sessionCollection.find_one({'qwakId': sessionId}))
    return list(map(lambda x: round(x,resultRounding), gQwak.getDynamicStDev()))

@app.route('/getStaticInversePartRatio',methods=['GET','POST'])
def getStaticInversePartRatio():
    sessionCollection = database[session['sessionId']]
    sessionId = session['sessionId']
    gQwak = GraphicalQWAK.from_json(sessionCollection.find_one({'qwakId': sessionId}))
    return [round(gQwak.getStaticInversePartRatio(), resultRounding)]

@app.route('/getDynamicInvPartRatio',methods=['GET','POST'])
def getDynamicInvPartRatio():
    sessionCollection = database[session['sessionId']]
    sessionId = session['sessionId']
    gQwak = GraphicalQWAK.from_json(sessionCollection.find_one({'qwakId': sessionId}))
    return list(map(lambda x: round(x,resultRounding), gQwak.getDynamicInvPartRatio()))

@app.route('/getStaticSurvivalProb',methods=['GET','POST'])
def getStaticSurvivalProb():
    sessionCollection = database[session['sessionId']]
    staticQWAK = QWAK.from_json(sessionCollection.find_one({'qwakId': session['staticQwakId']}))
    fromNode = str(request.form.get("fromNode"))
    toNode = str(request.form.get("toNode"))
    survProb = staticQWAK.getSurvivalProb(fromNode, toNode)
    # if not survProb[0]:
    #     survProb[1] = round(survProb[1], resultRounding)
    return str(survProb)

@app.route('/getDynamicSurvivalProb',methods=['GET','POST'])
def getDynamicSurvivalProb():
    sessionCollection = database[session['sessionId']]
    sessionId = session['sessionId']
    gQwak = GraphicalQWAK.from_json(sessionCollection.find_one({'qwakId': sessionId}))
    fromNode = str(request.form.get("fromNode"))
    toNode = str(request.form.get("toNode"))
    survProb = gQwak.getDynamicSurvivalProb(fromNode, toNode)
    if not survProb[0]:
        survProb[1] = list(map(lambda x: round(x,resultRounding),survProb[1]))
    return survProb

@app.route('/checkPST',methods=['GET','POST'])
def checkPST():
    sessionCollection = database[session['sessionId']]
    staticQWAK = QWAK.from_json(sessionCollection.find_one({'qwakId': session['staticQwakId']}))
    nodeA = str(request.form.get("nodeA"))
    nodeB = str(request.form.get("nodeB"))
    pst = staticQWAK.checkPST(nodeA, nodeB)
    return str(pst)

@app.route('/setStaticCustomGraph',methods=['GET','POST'])
def setStaticCustomGraph():
    sessionCollection = database[session['sessionId']]
    sessionId = session['sessionId']
    gQwak = GraphicalQWAK.from_json(sessionCollection.find_one({'qwakId': sessionId}))
    customAdjacency = np.matrix(eval(request.form.get("customAdjacency")))
    gQwak.setStaticCustomGraph(customAdjacency)
    return ("nothing")

@app.route('/setDynamicCustomGraph',methods=['GET','POST'])
def setDynamicCustomGraph():
    sessionCollection = database[session['sessionId']]
    sessionId = session['sessionId']
    gQwak = GraphicalQWAK.from_json(sessionCollection.find_one({'qwakId': sessionId}))
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

################## TEST ##################
@app.route("/test")
def test():
    return render_template('test.html')

@app.route("/reset",methods=['GET', 'POST'])
def reset():
    session.clear()
    for col in database.list_collection_names():
        database.drop_collection(col)

    # Locate the directory where the session files are stored
    session_dir = 'flask_session'
    # Iterate through all the files in the directory
    for file in os.listdir(session_dir):
        # Construct the full path to the file
        file_path = os.path.join(session_dir, file)
        try:
            # Attempt to delete the file
            os.unlink(file_path)
        except Exception as e:
            # An error occurred while trying to delete the file
            print(e)
    return render_template('reset.html')

@app.route("/load", methods=['GET', 'POST'])
def load():
    if not session.get('sessionId'):
        sessionId = f'user{len(database.list_collection_names())+1}'
        session['sessionId'] = sessionId
        print(session['sessionId'])
        sessionCollection = database[sessionId]
        sessionCollection.insert_one({'init':sessionId})
        # gQwak = GraphicalQWAK(
        #     staticN=staticN,
        #     dynamicN=dynamicN,
        #     staticGraph=staticGraph,
        #     dynamicGraph=dynamicGraph,
        #     staticStateList=initState,
        #     dynamicStateList=initStateList,
        #     staticTime=t,
        #     dynamicTimeList=timeList,
        #     qwakId=session['sessionId'])
        # sessionCollection.insert_one(json.loads(gQwak.to_json()))
        staticNTest = 5
        staticGraphTest = nx.cycle_graph(staticN)
        staticQWAK = QWAK(graph=staticGraphTest,qwakId=sessionId)
        sessionCollection.insert_one(json.loads(staticQWAK.to_json()))


    return("nothing")

@app.route('/setRunWalkDBTest',methods=['POST'])
def setRunWalkDBTest():
    if request.method == 'POST':
        sessionCollection = database[session['sessionId']]
        sessionId = session['sessionId']

        newDim = int(request.form.get("newDim"))
        newGraphStr = request.form.get("newGraph")
        newGraph = eval(newGraphStr + f"({newDim})")

        newTime = request.form.get("newTime")
        newInitCond = request.form.get("newInitCond")
        initCondList = list(map(int, newInitCond.split(",")))
        staticQWAK = QWAK.from_json(sessionCollection.find_one({'qwakId': sessionId}))
        staticQWAK.setDim(newDim,newGraphStr)
        staticQWAK.setGraph(newGraph)
        staticQWAK.setTime(newTime)
        newState = State(staticQWAK.getDim())
        newState.buildState(initCondList)
        staticQWAK.setInitState(newState)
        staticQWAK.runWalk()
        sessionCollection.replace_one({'qwakId': sessionId}, json.loads(staticQWAK.to_json()))
    return ("nothing")

@app.route('/getRunWalkDBTest',methods=['POST'])
def getRunWalkDBTest():
    if request.method == 'POST':
        sessionCollection = database[session['sessionId']]
        sessionId = session['sessionId']
        staticQWAK = QWAK.from_json(sessionCollection.find_one({'qwakId': sessionId}))
        staticQWAKJson = json.loads(staticQWAK.to_json())
        print(staticQWAK.getProbDist().getProbVec())

    return ("nothing")

################## TEST ##################

if __name__ == '__main__':
    app.run(debug=True)