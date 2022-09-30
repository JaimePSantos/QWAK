import json

from flask import Flask, render_template, url_for
import networkx as nx
import numpy as np
from qwak.GraphicalQWAK import GraphicalQWAK
from django.http import JsonResponse

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

@app.route("/")
@app.route("/home")
def home():
    return render_template('index.html')

@app.route("/staticQW")
def staticQW():
    return render_template('staticQW.html')

@app.route("/dynamicQW")
def dynamicQW():
    return render_template('dynamicQW.html')

@app.route('/setStaticGraph/<newGraph>',methods=['POST'])
def setStaticGraph(newGraph,):
    # variable = newGraph.GET.get('newGraph', 'default')
    print('Variable:', newGraph)
    gQwak.setStaticGraph(newGraph)
    print(gQwak.getStaticGraph())
    return ("nothing")

@app.route('/getStaticGraphToJson',methods=['POST'])
def getStaticGraphToJson():
    return gQwak.getStaticGraphToJson()

if __name__ == '__main__':
    app.run(debug=True)