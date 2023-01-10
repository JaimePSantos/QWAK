import {customCy, cy} from "../static-tools.js";

let inputDim = document.getElementById("inputDim");
let inputGraph = document.getElementById("inputGraph");

// - Graph Generator

export function setStaticDim(newDim, graphStr) {
    $.ajax({
        type: 'POST',
        url: `/setStaticDim`, // <- Add the queryparameter here
        data: {newDim: newDim, graphStr: graphStr},
        success: function (response) {
            console.log('success - Dim set to ${newDim}');
        },
        error: function (response) {
            console.log('setDim error');
        }
    });
}

export async function setStaticGraph(newDim,newGraph) {
    let myGraph;
    await $.ajax({
        type: 'POST',
        url: `/setStaticGraph`,
        data: {newDim:newDim,newGraph:newGraph},
        success: function (response) {
            console.log(`success - graph set to ${newGraph}:\n ${response}`)
            // console.log(response);
            myGraph = response;
            return myGraph;
        },
        error: function (response) {
            myGraph = response;
            return myGraph;
        }
    });
    return myGraph;
}

export function updateGraph(graph) {
    cy.elements().remove()
    cy.add(graph.elements)
    cy.layout({name: "circle"}).run();
}

export async function getStaticGraph() {
    let myGraph;
    await $.ajax({
        type: 'POST',
        url: `/getStaticGraphToJson`, // <- Add the queryparameter here
        success: function (response) {
            myGraph = response;
            console.log('success - got graph ${myGraph}');
            return myGraph;
        },
        error: function (response) {
            console.log('getStaticGraph error');
            myGraph = 'error'
            return myGraph;
        }
    });
    return myGraph;
}

// Custom Graph

let nodeNumber = 2;
let nodeXPos = 200;
let nodeYPos = 0;

var eh = customCy.edgehandles();

export async function addNodeButtonPress() {
    nodeNumber++;
    nodeYPos += 50;
    customCy.add({
        group: 'nodes',
        data: {id: nodeNumber.toString(), name: nodeNumber.toString()},
        position: {x: nodeXPos, y: nodeYPos}
    });
}

export function setCustomAdjacencyMatrix(customAdjacency) {
    // console.log(customAdjacency)
    $.ajax({
        type: 'POST',
        url: `/setStaticCustomGraph`, // <- Add the queryparameter here
        data: {customAdjacency: customAdjacency},
        async: false,
        success: function (response) {
            console.log('success - customAdjacency set to ${customAdjacency}');
        },
        error: function (response) {
            console.log('customAdjacency error');
        }
    });
}

export function createAdjacencyMatrix(graph) {
    let adjacencyMatrix = math.zeros(graph.json().elements.nodes.length, graph.json().elements.nodes.length)

    for (let edg of graph.json().elements.edges) {
        // console.log(`Source: ${edg.data.source} -> Target: ${edg.data.target}`);
        adjacencyMatrix.subset(math.index(parseInt(edg.data.source), parseInt(edg.data.target)), 1);
        adjacencyMatrix.subset(math.index(parseInt(edg.data.target), parseInt(edg.data.source)), 1);
    }
    adjacencyMatrix = adjacencyMatrixToString(adjacencyMatrix);
    return adjacencyMatrix;
}

export function adjacencyMatrixToString(adjacencyMatrix) {
    let adjm = "[";
    let elemAux = "";
    for (let elem of adjacencyMatrix._data) {
        elemAux = "["
        for (let e of elem) {
            elemAux = elemAux.concat(",", e);
        }
        elemAux = elemAux.concat("", "]")
        elemAux = elemAux.slice(0, 1) + elemAux.slice(2)
        adjm = adjm.concat(",", elemAux)
        elemAux = "";
    }
    adjm = adjm.concat("", "]")
    adjm = adjm.slice(0, 1) + adjm.slice(2)
    return adjm
}