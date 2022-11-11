import {customCy, cy, staticChartData} from "./static-tools.js";
import {StaticQuantumwalk} from "./staticQuantumwalk.js";


// #### INPUTS & DISPLAYS ####
let inputDim = document.getElementById("inputDim");
let inputGraph = document.getElementById("inputGraph");
let inputTime = document.getElementById("inputTime");
let inputInitState = document.getElementById("inputInitState");

let inputMean = document.getElementById("inputMean");
let inputSndMoment = document.getElementById("inputSndMoment");
let inputStDev = document.getElementById("inputStDev");
let inputSurvProbResult = document.getElementById("inputSurvProbResult");
let inputSurvProbNodeA = document.getElementById("inputSurvProbNodeA");
let inputSurvProbNodeB = document.getElementById("inputSurvProbNodeB");
let inputInvPartRat = document.getElementById("inputInvPartRat");
let inputPSTNodeA = document.getElementById("inputPSTNodeA");
let inputPSTNodeB = document.getElementById("inputPSTNodeB");
let inputPSTResult = document.getElementById("inputPSTResult");


// #### JAVASCRIPT QUANTUM WALK OBJECTS ####
let defaultN = 100;
let defaultT = 10;
let defaultInitState = [Math.floor(defaultN / 2)];
let defaultGraph = 'nx.cycle_graph';
let defaultTimeList = [0, 100];
let defaultInitStateList = [[Math.floor(defaultN / 2)]];

let staticQuantumWalk = new StaticQuantumwalk(defaultN, defaultT, defaultInitState, defaultGraph);

let inputInit = () => {
    inputTime.value = defaultT;
    inputInitState.value = defaultInitState
    inputDim.value = defaultN;
    inputGraph.value = defaultGraph;
}

inputInit();

// SETTING THE GRAPH
// - Graph Generator

let myChart = new Chart(document.getElementById("staticProbDistChart").getContext("2d"), staticChartData);

$(function () {
    $('#runGraphButton').on('click', async function (e) {
        e.preventDefault();
        staticQuantumWalk.graph = inputGraph.value;
        staticQuantumWalk.dim = parseInt(inputDim.value);
        setStaticDim(staticQuantumWalk.dim, staticQuantumWalk.graph);
        setStaticGraph(staticQuantumWalk.graph);
        let myGraph = await getStaticGraph();
        // console.log(myGraph)
        updateGraph(myGraph);
    });
});

$(function () {
    $('#setDimButton').on('click', function (e) {
        e.preventDefault();
        staticQuantumWalk.graph = inputGraph.value;
        staticQuantumWalk.dim = parseInt(inputDim.value);
        setStaticDim(staticQuantumWalk.dim, staticQuantumWalk.graph)
    });
});

function setStaticDim(newDim, graphStr) {
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

function setStaticGraph(newGraph) {
    $.ajax({
        type: 'POST',
        url: `/setStaticGraph`,
        data: {newGraph: newGraph},
        success: function (response) {
            console.log('success - graph set to ${newGraph}');
        },
        error: function (response) {
            console.log('setGraph error');
        }
    })
}

function updateGraph(graph) {
    cy.elements().remove()
    cy.add(graph.elements)
    cy.layout({name: "circle"}).run();
}

async function getStaticGraph() {
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

// - Custom Graph
// #### CUSTOM GRAPH ####


let nodeNumber = 2;
let nodeXPos = 200;
let nodeYPos = 0;

var eh = customCy.edgehandles();

document.getElementById('addEdgeButton').addEventListener('click', function () {
    eh.enableDrawMode();
});

document.getElementById("addNodeButton").addEventListener('click', function () {
    addNodeButtonPress();
});

document.getElementById('clearGraphButton').addEventListener('click', function () {
    eh.disableDrawMode();
});

$(function () {
    $('#graphCustomButton').on('click', async function (e) {
        e.preventDefault();
        let customAdjacency = createAdjacencyMatrix(customCy);
        setCustomAdjacencyMatrix(customAdjacency);
    });
});


async function addNodeButtonPress() {
    nodeNumber++;
    nodeYPos += 50;
    customCy.add({
        group: 'nodes',
        data: {id: nodeNumber.toString(), name: nodeNumber.toString()},
        position: {x: nodeXPos, y: nodeYPos}
    });
}

function setCustomAdjacencyMatrix(customAdjacency) {
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

function createAdjacencyMatrix(graph) {
    let adjacencyMatrix = math.zeros(graph.json().elements.nodes.length, graph.json().elements.nodes.length)

    for (let edg of graph.json().elements.edges) {
        // console.log(`Source: ${edg.data.source} -> Target: ${edg.data.target}`);
        adjacencyMatrix.subset(math.index(parseInt(edg.data.source), parseInt(edg.data.target)), 1);
        adjacencyMatrix.subset(math.index(parseInt(edg.data.target), parseInt(edg.data.source)), 1);
    }
    adjacencyMatrix = adjacencyMatrixToString(adjacencyMatrix);
    return adjacencyMatrix;
}

function adjacencyMatrixToString(adjacencyMatrix) {
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

// SETTING PROBDIST

$(function () {
    $('#setInitStateButton').on('click', function (e) {
        e.preventDefault();
        staticQuantumWalk.initState = inputInitState.value;
        setStaticInitState(staticQuantumWalk.initState)
    });
});

$(function () {
    $('#setTimeButton').on('click', function (e) {
        e.preventDefault();
        staticQuantumWalk.time = (inputTime.value);
        setStaticTime(staticQuantumWalk.time)
    });
});

$(function () {
    $('#staticProbDistButton').on('click', async function (e) {
        e.preventDefault();
        let staticProbDist = await getStaticProbDist();
        setStaticProbDist(staticProbDist);
        setStaticMean();
        setStaticSndMoment();
        setStaticStDev();
        setStaticInversePartRatio();
    });
});

function setStaticInitState(initStateStr) {
    $.ajax({
        type: 'POST',
        url: `/setStaticInitState`, // <- Add the queryparameter here
        data: {initStateStr: initStateStr},
        success: function (response) {
            console.log('success - InitState set to ${initStateStr}');
        },
        error: function (response) {
            console.log('InitState error');
        }
    });
}

function setStaticTime(newTime) {
    $.ajax({
        type: 'POST',
        url: `/setStaticTime`, // <- Add the queryparameter here
        data: {newTime: newTime},
        success: function (response) {
            console.log('success - Time set to ${newTime}');
        },
        error: function (response) {
            console.log('setTime error');
        }
    });
}

function setStaticProbDist(walk) {
    // console.log(walk)
    if (walk[0] == true) {
        alert(walk[1]);
        return;
    } else {
        let distList = walk[1].flat();
        staticChartData.data.datasets[0].data = distList;
        staticChartData.data.labels = [...Array(distList.length).keys()];
        myChart.destroy();
        myChart = new Chart(document.getElementById("staticProbDistChart").getContext("2d"), staticChartData);
        // await setStaticMean();
        // await setStaticSndMoment();
        // await setStaticStDev();
        // await setInversePartRatio();
    }
}

async function getStaticProbDist() {
    let myWalk;
    await $.ajax({
        type: 'POST',
        url: `/runWalk`, // <- Add the queryparameter here
        success: function (response) {
            myWalk = response;
            console.log(`success - Runwalk ${myWalk}`);
            return myWalk;
        },
        error: function (response) {
            console.log('Runwalk error');
            myWalk = 'error'
            return myWalk;
        }
    });
    return myWalk;
}

//SETTING STATISTICS
$(function () {
    $('#survProbNodesButton').on('click', async function (e) {
        e.preventDefault();
        let fromNode = inputSurvProbNodeA.value;
        let toNode = inputSurvProbNodeB.value;
        setStaticSurvivalProb(fromNode, toNode);
    });
});

$(function () {
    $('#PSTNodesButton').on('click', async function (e) {
        e.preventDefault();
        let nodeA = inputPSTNodeA.value;
        let nodeB = inputPSTNodeB.value;
        setPst(nodeA, nodeB);
    });
});

async function setStaticMean() {
    let statMean = await getStaticMean();
    inputMean.value = statMean;
}

async function setStaticSndMoment() {
    let statSndMom = await getStaticSndMoment();
    inputSndMoment.value = statSndMom;
}

async function setStaticStDev() {
    let statStDev = await getStaticStDev();
    inputStDev.value = statStDev;
}

async function setStaticInversePartRatio() {
    let invPartRatio = await getStaticInversePartRatio();
    inputInvPartRat.value = invPartRatio;
}

async function setStaticSurvivalProb(fromNode, toNode) {
    let survProb = await getStaticSurvivalProb(fromNode, toNode);
    if (survProb[0] == true) {
        alert(survProb[1]);
        return;
    } else {
        inputSurvProbResult.value = survProb[1];
    }
}

async function setPst(nodeA, nodeB) {
    let PST = await getPst(nodeA, nodeB);
    if (PST[0] == true) {
        alert(PST[1]);
        return;
    } else {
        if (PST[1] < 0) {
            inputPSTResult.value = 'No PST.';
        } else {
            inputPSTResult.value = PST[1];
        }
    }
}

async function getStaticMean() {
    let staticMean;
    await $.ajax({
        type: 'POST',
        url: `/getStaticMean`, // <- Add the queryparameter here
        success: function (response) {
            staticMean = response;
            console.log(`success - getStaticMean ${staticMean}`);
            return staticMean;
        },
        error: function (response) {
            console.log('getStaticMean error');
            staticMean = 'error'
            return staticMean;
        }
    });
    return staticMean;
}

async function getStaticSndMoment() {
    let staticSndMoment;
    await $.ajax({
        type: 'POST',
        url: `/getStaticSndMoment`,
        success: function (response) {
            staticSndMoment = response;
            console.log(`success - getStaticSndMoment ${staticSndMoment}`);
            return staticSndMoment;
        },
        error: function (response) {
            console.log('getStaticSndMoment error');
            staticSndMoment = 'error'
            return staticSndMoment;
        }
    });
    return staticSndMoment;
}

async function getStaticStDev() {
    let staticStDev;
    await $.ajax({
        type: 'POST',
        url: `/getStaticStDev`,
        success: function (response) {
            staticStDev = response;
            console.log(`success - getStaticStDev ${staticStDev}`);
            return staticStDev;
        },
        error: function (response) {
            console.log('getStaticStDev error');
            staticStDev = 'error'
            return staticStDev;
        }
    });
    return staticStDev;
}

async function getStaticInversePartRatio() {
    let staticInversePartRatio;
    await $.ajax({
        type: 'POST',
        url: `/getStaticInversePartRatio`,
        success: function (response) {
            staticInversePartRatio = response;
            console.log(`success - staticInversePartRatio ${staticInversePartRatio}`);
            return staticInversePartRatio;
        },
        error: function (response) {
            console.log('staticInversePartRatio error');
            staticInversePartRatio = 'error'
            return staticInversePartRatio;
        }
    });
    return staticInversePartRatio;
}

async function getStaticSurvivalProb(fromNode, toNode) {
    let staticSurvivalProb;
    await $.ajax({
        type: 'POST',
        url: `/getStaticSurvivalProb`,
        data: {fromNode: fromNode, toNode: toNode},
        success: function (response) {
            staticSurvivalProb = response;
            console.log(`success - staticSurvivalProb ${staticSurvivalProb}`);
            return staticSurvivalProb;
        },
        error: function (response) {
            console.log('staticSurvivalProb error');
            staticSurvivalProb = 'error'
            return staticSurvivalProb;
        }
    });
    return staticSurvivalProb;
}

async function getPst(nodeA, nodeB) {
    let pst;
    await $.ajax({
        type: 'POST',
        url: `/checkPST`,
        data: {nodeA: nodeA, nodeB: nodeB},
        success: function (response) {
            pst = response;
            console.log(`success - pst ${pst}`);
            return pst;
        },
        error: function (response) {
            console.log('pst error');
            pst = 'error'
            return pst;
        }
    });
    return pst;
}

// #### GRAPHS  ####

cy.layout({name: "circle"}).run();