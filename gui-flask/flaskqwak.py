import json

from flask import Flask, render_template, url_for, request, redirect, session
from flask_session import Session
from pymongo import MongoClient
import networkx as nx
import numpy as np
from numpy import pi
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

# connection_string = f"mongodb+srv://{QWAKCLUSTER_USERNAME}:{QWAKCLUSTER_PASSWORD}@qwakcluster.kkszzg0.mongodb.net/test"

client = MongoClient('localhost', 27017)
# client = MongoClient(connection_string)
db_string = 'qwak_flask'
database = client.get_database(db_string)
probDistEntry = database['probDistEntry']

app = Flask(__name__)
SESSION_TYPE = 'filesystem'
app.config.from_object(__name__)
Session(app)

resultRounding = 3


@app.route("/", methods=['GET', 'POST'])
@app.route("/home")
def home():
    if not session.get('sessionId'):
        sessionId = f'user{len(database.list_collection_names())+1}'
        session['sessionId'] = sessionId
        probDistSessionCollection = database[sessionId]
        probDistSessionCollection.insert_one({'init': sessionId})

    return render_template('index.html')


@app.route("/staticQW")
def staticQW():
    if not session.get('sessionId'):
        sessionId = f'user{len(database.list_collection_names())+1}'
        session['sessionId'] = sessionId
        probDistSessionCollection = database[sessionId]
        probDistSessionCollection.insert_one({'init': sessionId})
    if not session.get('staticQwakId'):
        staticQwakId = f"StaticQWAK_{session['sessionId']}"
        session['staticQwakId'] = staticQwakId
        probDistSessionCollection = database[session['sessionId']]
        staticN = 5
        staticGraph = nx.cycle_graph(staticN)
        staticQWAK = QWAK(
            graph=staticGraph,
            qwakId=session['staticQwakId'])
        probDistSessionCollection.insert_one(
            json.loads(staticQWAK.to_json()))
    return render_template('staticQW.html')


@app.route("/dynamicQW")
def dynamicQW():
    if not session.get('sessionId'):
        sessionId = f'user{len(database.list_collection_names())+1}'
        session['sessionId'] = sessionId
        probDistSessionCollection = database[sessionId]
        probDistSessionCollection.insert_one({'init': sessionId})
    if not session.get('dynamicQwakId'):
        dynamicQwakId = f"DynamicQWAK_{session['sessionId']}"
        session['dynamicQwakId'] = dynamicQwakId
        probDistSessionCollection = database[session['sessionId']]
        dynamicN = 5
        dynamicGraph = nx.cycle_graph(dynamicN)
        dynamicQwak = QWAK(
            graph=dynamicGraph,
            qwakId=session['dynamicQwakId'])
        probDistSessionCollection.insert_one(
            json.loads(dynamicQwak.to_json(isDynamic=True)))
    return render_template('dynamicQW.html')


@app.route('/setStaticGraph', methods=['GET', 'POST'])
def setStaticGraph():
    probDistSessionCollection = database[session['sessionId']]
    staticQWAK = QWAK.from_json(probDistSessionCollection.find_one({
                                'qwakId': session['staticQwakId']}))
    newDim = int(request.form.get("newDim"))
    newGraph = request.form.get("newGraph")
    staticQWAK.setDim(newDim, graphStr=newGraph)
    staticQWAK.setGraph(eval(f"{newGraph}({staticQWAK.getDim()})"))
    probDistSessionCollection.replace_one(
        {'qwakId': session['staticQwakId']}, json.loads(staticQWAK.to_json()))
    return nx.cytoscape_data(staticQWAK.getGraph())


@app.route('/getStaticGraphToJson', methods=['GET', 'POST'])
def getStaticGraphToJson():
    probDistSessionCollection = database[session['sessionId']]
    staticQWAK = QWAK.from_json(probDistSessionCollection.find_one({
                                'qwakId': session['staticQwakId']}))
    return nx.cytoscape_data(staticQWAK.getGraph())


@app.route('/setStaticCustomGraph', methods=['GET', 'POST'])
def setStaticCustomGraph():
    probDistSessionCollection = database[session['sessionId']]
    staticQWAK = QWAK.from_json(probDistSessionCollection.find_one({
                                'qwakId': session['staticQwakId']}))
    customAdjacency = np.matrix(
        eval(request.form.get("customAdjacency")))
    staticQWAK.setCustomGraph(customAdjacency)
    probDistSessionCollection.replace_one(
        {'qwakId': session['staticQwakId']}, json.loads(staticQWAK.to_json()))
    return ("nothing")


@app.route('/getRunWalkDB', methods=['POST'])
def getRunWalkDB():
    print(request.method)
    if request.method == 'POST':
        probDistSessionCollection = database[session['sessionId']]
        try:
            newTime = eval(request.form.get("newTime"))
            newInitCond = request.form.get("newInitCond")
            initCondList = list(map(int, newInitCond.split(",")))
            staticQWAK = QWAK.from_json(probDistSessionCollection.find_one({
                                        'qwakId': session['staticQwakId']}))
            staticQWAK.setTime(newTime)
            newState = State(staticQWAK.getDim())
            newState.buildState(initCondList)
            staticQWAK.setInitState(newState)
            staticQWAK.runWalk()
            resultDict = {
                'prob': staticQWAK.getProbVec().tolist(),
                'mean': staticQWAK.getMean(resultRounding),
                'sndMoment': staticQWAK.getSndMoment(resultRounding),
                'stDev': staticQWAK.getStDev(resultRounding),
                'invPartRatio': staticQWAK.getInversePartRatio(resultRounding)}
            probDistSessionCollection.replace_one(
                {'qwakId': session['staticQwakId']}, json.loads(staticQWAK.to_json()))
            return [False, resultDict]
        except StateOutOfBounds as err:
            return [True, str(err)]


@app.route('/getStaticSurvivalProb', methods=['GET', 'POST'])
def getStaticSurvivalProb():
    try:
        probDistSessionCollection = database[session['sessionId']]
        staticQWAK = QWAK.from_json(probDistSessionCollection.find_one({
                                    'qwakId': session['staticQwakId']}))
        fromNode = str(request.form.get("fromNode"))
        toNode = str(request.form.get("toNode"))
        survProb = staticQWAK.getSurvivalProb(fromNode, toNode,resultRounding)
        return [False, str(survProb)]
    except MissingNodeInput as err:
        return [True, str(err)]


@app.route('/checkPST', methods=['GET', 'POST'])
def checkPST():
    probDistSessionCollection = database[session['sessionId']]
    staticQWAK = QWAK.from_json(probDistSessionCollection.find_one({
                                'qwakId': session['staticQwakId']}))
    nodeA = request.form.get("nodeA")
    nodeB = request.form.get("nodeB")
    try:
        pst = staticQWAK.checkPST(nodeA, nodeB)
        return [False,str(pst)]
    except MissingNodeInput as err:
        return [True,str(err)]

@app.route('/setDynamicGraph', methods=['GET', 'POST'])
def setDynamicGraph():
    probDistSessionCollection = database[session['sessionId']]
    dynamicQWAK = QWAK.from_json(probDistSessionCollection.find_one(
        {'qwakId': session['dynamicQwakId']}), isDynamic=True)
    newDim = int(request.form.get("newDim"))
    newGraph = request.form.get("newGraph")
    dynamicQWAK.setDim(newDim, graphStr=newGraph)
    dynamicQWAK.setGraph(eval(f"{newGraph}({dynamicQWAK.getDim()})"))
    probDistSessionCollection.replace_one(
        {'qwakId': session['dynamicQwakId']}, json.loads(dynamicQWAK.to_json(isDynamic=True)))
    return nx.cytoscape_data(dynamicQWAK.getGraph())


@app.route('/getDynamicGraphToJson', methods=['GET', 'POST'])
def getDynamicGraphToJson():
    probDistSessionCollection = database[session['sessionId']]
    dynamicQWAK = QWAK.from_json(probDistSessionCollection.find_one(
        {'qwakId': session['dynamicQwakId']}), isDynamic=True)
    return nx.cytoscape_data(dynamicQWAK.getGraph())


@app.route('/getRunMultipleWalksDB', methods=['POST', 'GET'])
def getRunMultipleWalksDB():
    if request.method == 'POST':
        try:
            probDistSessionCollection = database[session['sessionId']]
            newTimeList = eval(request.form.get("newTimeList"))
            newInitCond = request.form.get("newInitCond")
            initCondList = list(map(int, newInitCond.split(",")))
            dynamicQWAK = QWAK.from_json(probDistSessionCollection.find_one(
                {'qwakId': session['dynamicQwakId']}), isDynamic=True)
            dynamicQWAK.setTimeList(newTimeList)
            newState = State(dynamicQWAK.getDim())
            newState.buildState(initCondList)
            dynamicQWAK.setInitState(newState)
            dynamicQWAK.runMultipleWalks()
            probDistList = [probDist.getProbVec().tolist()
                            for probDist in dynamicQWAK.getProbDistList()]
            resultDict = {
                'prob': probDistList,
            }
            probDistSessionCollection.replace_one({'qwakId': session['dynamicQwakId']},
                                                  json.loads(dynamicQWAK.to_json(isDynamic=True)))
        except StateOutOfBounds as err:
            return [True, str(err)]
        return [False, resultDict]


@app.route('/setRunMultipleWalksDB', methods=['POST'])
def setRunMultipleWalksDB():
    print(request.method)
    if request.method == 'POST':
        try:
            probDistSessionCollection = database[session['sessionId']]
            dynamicQWAK = QWAK.from_json(probDistSessionCollection.find_one(
                {'qwakId': session['dynamicQwakId']}), isDynamic=True)
            probDistList = []
            for probDist in dynamicQWAK.getProbDistList():
                probDistList.append(probDist.getProbVec().tolist())
            resultDict = {
                'prob': probDistList
            }
        except StateOutOfBounds as err:
            return [True, str(err)]
    return [False, resultDict]


@app.route('/runMultipleWalks', methods=['GET', 'POST'])
def runMultipleWalks():
    probDistSessionCollection = database[session['sessionId']]
    sessionId = session['sessionId']
    gQwak = GraphicalQWAK.from_json(
        probDistSessionCollection.find_one({'qwakId': sessionId}))
    return gQwak.runMultipleWalks()


@app.route('/getDynamicMean', methods=['GET', 'POST'])
def getDynamicMean():
    probDistSessionCollection = database[session['sessionId']]
    dynamicQWAK = QWAK.from_json(probDistSessionCollection.find_one(
        {'qwakId': session['dynamicQwakId']}), isDynamic=True)
    meanList = dynamicQWAK.getMeanList(resultRounding)
    return meanList


@app.route('/getDynamicStDev', methods=['GET', 'POST'])
def getDynamicStDev():
    probDistSessionCollection = database[session['sessionId']]
    dynamicQWAK = QWAK.from_json(probDistSessionCollection.find_one(
        {'qwakId': session['dynamicQwakId']}), isDynamic=True)
    stDevList = dynamicQWAK.getStDevList(resultRounding)
    return stDevList


@app.route('/getDynamicInvPartRatio', methods=['GET', 'POST'])
def getDynamicInvPartRatio():
    probDistSessionCollection = database[session['sessionId']]
    dynamicQWAK = QWAK.from_json(probDistSessionCollection.find_one(
        {'qwakId': session['dynamicQwakId']}), isDynamic=True)
    stDevList = dynamicQWAK.getInversePartRatioList(resultRounding)
    return stDevList


@app.route('/getDynamicSurvivalProb', methods=['GET', 'POST'])
def getDynamicSurvivalProb():
    probDistSessionCollection = database[session['sessionId']]
    dynamicQWAK = QWAK.from_json(probDistSessionCollection.find_one(
        {'qwakId': session['dynamicQwakId']}), isDynamic=True)
    fromNode = str(request.form.get("fromNode"))
    toNode = str(request.form.get("toNode"))
    try:
        survProbList = dynamicQWAK.getSurvivalProbList(
            fromNode, toNode, resultRounding)
        return [False, survProbList]
    except MissingNodeInput as err:
        return [True, str(err)]


@app.route('/setDynamicCustomGraph', methods=['GET', 'POST'])
def setDynamicCustomGraph():
    probDistSessionCollection = database[session['sessionId']]
    dynamicQWAK = QWAK.from_json(probDistSessionCollection.find_one(
        {'qwakId': session['dynamicQwakId']}), isDynamic=True)
    customAdjacency = np.matrix(
        eval(request.form.get("customAdjacency")))
    dynamicQWAK.setCustomGraph(customAdjacency)
    probDistSessionCollection.replace_one(
        {'qwakId': session['dynamicQwakId']}, json.loads(dynamicQWAK.to_json(isDynamic=True)))
    return ("nothing")


@app.route('/deleteWalkEntry', methods=['POST'])
def deleteWalkEntry():
    print(request.method)
    if request.method == 'POST':
        name = str(request.form.get("walkName"))
        probDistEntry.delete_one({
            'name': name,
        })
    return ("nothing")


@app.route('/deleteAllWalkEntries', methods=['POST'])
def deleteAllWalkEntries():
    print(request.method)
    if request.method == 'POST':
        probDistEntry.delete_many({})
    return ("nothing")

################## TEST ##################


@app.route("/test")
def test():
    return render_template('test.html')


@app.route("/reset", methods=['GET', 'POST'])
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
        probDistSessionCollection = database[sessionId]
        probDistSessionCollection.insert_one({'init': sessionId})

        staticQwakId = f"StaticQWAK_{session['sessionId']}"
        session['staticQwakId'] = staticQwakId
        staticNTest = 5
        staticGraphTest = nx.cycle_graph(staticNTest)
        staticQWAK = QWAK(graph=staticGraphTest, qwakId=staticQwakId)
        probDistSessionCollection.insert_one(
            json.loads(staticQWAK.to_json()))

        dynamicQwakId = f"DynamicQWAK_{session['sessionId']}"
        session['dynamicQwakId'] = dynamicQwakId
        probDistSessionCollection = database[session['sessionId']]
        dynamicNTest = 5
        dynamicGraphTest = nx.cycle_graph(dynamicNTest)
        dynamicQwak = QWAK(
            graph=dynamicGraphTest,
            qwakId=session['dynamicQwakId'])
        probDistSessionCollection.insert_one(
            json.loads(dynamicQwak.to_json(isDynamic=True)))

    return ("nothing")


@app.route('/setRunWalkDBTest', methods=['POST'])
def setRunWalkDBTest():
    if request.method == 'POST':
        probDistSessionCollection = database[session['sessionId']]
        sessionId = session['sessionId']

        newDim = int(request.form.get("newDim"))
        newGraphStr = request.form.get("newGraph")
        newGraph = eval(newGraphStr + f"({newDim})")

        newTime = float(request.form.get("newTime"))
        newInitCond = request.form.get("newInitCond")
        initCondList = list(map(int, newInitCond.split(",")))

        staticQWAK = QWAK.from_json(probDistSessionCollection.find_one({
                                    'qwakId': session['staticQwakId']}))
        staticQWAK.setDim(newDim, newGraphStr)
        staticQWAK.setGraph(newGraph)
        staticQWAK.setTime(newTime)
        newState = State(staticQWAK.getDim())
        newState.buildState(initCondList)
        staticQWAK.setInitState(newState)
        staticQWAK.runWalk()

        probDistSessionCollection.replace_one(
            {'qwakId': sessionId}, json.loads(staticQWAK.to_json()))
    return ("nothing")


@app.route('/getRunWalkDBTest', methods=['POST'])
def getRunWalkDBTest():
    if request.method == 'POST':
        probDistSessionCollection = database[session['sessionId']]
        sessionId = session['sessionId']
        staticQWAK = QWAK.from_json(
            probDistSessionCollection.find_one({'qwakId': sessionId}))
        staticQWAKJson = json.loads(staticQWAK.to_json())
        print(staticQWAK.getProbDist().getProbVec())

    return ("nothing")


@app.route('/setRunMultipleWalksDBTest', methods=['POST', 'GET'])
def setRunMultipleWalksDBTest():
    if request.method == 'POST':
        probDistSessionCollection = database[session['sessionId']]

        newDim = int(request.form.get("newDim"))
        newGraphStr = request.form.get("newGraph")
        newGraph = eval(newGraphStr + f"({newDim})")

        newTimeList = eval(request.form.get("newTimeList"))
        newInitCond = request.form.get("newInitCond")
        initCondList = list(map(int, newInitCond.split(",")))

        dynamicQWAK = QWAK.from_json(probDistSessionCollection.find_one(
            {'qwakId': session['dynamicQwakId']}), True)
        dynamicQWAK.setDim(newDim, newGraphStr)
        dynamicQWAK.setGraph(newGraph)
        dynamicQWAK.setTimeList(newTimeList)
        newState = State(dynamicQWAK.getDim())
        newState.buildState(initCondList)
        dynamicQWAK.setInitState(newState)
        dynamicQWAK.runMultipleWalks()

        for probDist in dynamicQWAK.getProbDistList():
            print(probDist.getProbVec())

        probDistSessionCollection.replace_one(
            {'qwakId': session['dynamicQwakId']}, json.loads(dynamicQWAK.to_json(isDynamic=True)))
    return ("nothing")


@app.route('/getRunMultipleWalksDBTest', methods=['POST'])
def getRunMultipleWalksDBTest():
    prob = []
    print(request.method)
    if request.method == 'POST':
        probDistSessionCollection = database[session['sessionId']]
        sessionId = session['sessionId']
        gQwak = GraphicalQWAK.from_json(
            probDistSessionCollection.find_one({'qwakId': sessionId}))
        name = str(request.form.get("walkName"))
        prob = gQwak.getDynamicProbVecList().tolist()
    return prob

################## TEST ##################


if __name__ == '__main__':
    app.run(debug=True)
