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
let myChart = new Chart(document.getElementById("staticProbDistChart").getContext("2d"), staticChartData);

$(function () {
    $('#runGraphButton').on('click', async function (e) {
        e.preventDefault();
        staticQuantumWalk.graph = inputGraph.value;
        staticQuantumWalk.dim = parseInt(inputDim.value);
        setStaticDim(staticQuantumWalk.dim, staticQuantumWalk.graph);
        setStaticGraph(staticQuantumWalk.graph);
        let myGraph = await getStaticGraph();
        console.log(myGraph)
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
// SETTING THE GRAPH

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

function setStaticTime(newTime){
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

function setStaticProbDist(walk){
    console.log(walk)
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

async function getStaticProbDist(){
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

//#### #### STATIC STATISTICS #### ####

document.getElementById("survProbNodesButton").addEventListener('click', async function () {
    setStaticSurvivalProb();
});

document.getElementById("PSTNodesButton").addEventListener('click', async function () {
    setPST();
});

let setStaticMean = async () => {
    // let statMean = await getStaticMean();
    inputMean.value = statMean;
}

let setStaticSndMoment = async () => {
    // let statSndMom = await getStaticSndMoment();
    inputSndMoment.value = statSndMom;
}

let setStaticStDev = async () => {
    // let statStDev = await getStaticStDev();
    inputStDev.value = statStDev;
}

let setStaticSurvivalProb = async () => {
    let fromNode = inputSurvProbNodeA.value;
    let toNode = inputSurvProbNodeB.value;
    // let survProb = await getStaticSurvivalProb(fromNode, toNode);
    console.log(survProb)
    if (survProb[0] == true) {
        alert(survProb[1]);
        return;
    } else {
        inputSurvProbResult.value = survProb[1];
    }
}

let setInversePartRatio = async () => {
    // let invPartRatio = await getInversePartRatio();
    inputInvPartRat.value = invPartRatio;
}

let setPST = async () => {
    let fromNode = inputPSTNodeA.value;
    let toNode = inputPSTNodeB.value;
    // let PST = await getPST(fromNode, toNode);
    // console.log(PST)
    // if(PST[0]==true){
    //     alert(PST[1]);
    //     return;
    // }else{
    //     if(PST[1]<0){
    //             inputPSTResult.value = 'No PST.';
    //     }else{
    //             inputPSTResult.value = PST[1];
    //     }
    // }
}

let getStaticMean = () => {
    return eel
        .getStaticMean()()
        .then((a) => {
            return a ? a : Promise.reject(Error("Get Static Mean failed."));
        })
        .catch((e) => console.log(e));
}

let getStaticSndMoment = () => {
    return eel
        .getStaticSndMoment()()
        .then((a) => {
            return a ? a : Promise.reject(Error("Get Static Snd Moment failed."));
        })
        .catch((e) => console.log(e));
}

let getStaticStDev = () => {
    return eel
        .getStaticStDev()()
        .then((a) => {
            if (isNaN(a)) {
                Promise.reject(Error("Get Static Standard Deviation faile: StDev is NaN."));
            } else {
                return a;
            }
        })
        .catch((e) => console.log(e));
}

let getStaticSurvivalProb = (fromNode, toNode) => {
    return eel
        .getStaticSurvivalProb(fromNode, toNode)()
        .then((a) => {
            return a;
        })
        .catch((e) => console.log(e));
}

let getInversePartRatio = () => {
    return eel
        .getInversePartRatio()()
        .then((a) => {
            if (isNaN(a)) {
                Promise.reject(Error("Get Inv. Part. Ratio failed: IPR is NaN."));
            } else {
                return a;
            }
        })
        .catch((e) => console.log(e));
}

let getPST = (nodeA, nodeB) => {
    return eel
        .checkPST(nodeA, nodeB)()
        .then((a) => {
            return a;
        })
        .catch((e) => console.log(e));
}

// #### GRAPHS  ####

cy.layout({name: "circle"}).run();

// #### #### GRAPH GENERATOR #### ####

// let setDimButton = async () => {
//     staticQuantumWalk.dim = parseInt(inputDim.value);
//     staticQuantumWalk.graph = inputGraph.value;
//     eel.setStaticDim(staticQuantumWalk.dim, staticQuantumWalk.graph);
// }

// let setStaticGraph = async () => {
//     staticQuantumWalk.graph = inputGraph.value;
//     eel.setStaticGraph(staticQuantumWalk.graph);
// }

// #### CUSTOM GRAPH ####
let updateGraph = (graph) => {
    cy.elements().remove()
    cy.add(graph.elements)
    cy.layout({name: "circle"}).run();
}

var eh = customCy.edgehandles();

document.getElementById('addEdgeButton').addEventListener('click', function () {
    eh.enableDrawMode();
});

document.getElementById("addNodeButton").addEventListener('click', function () {
    addNodeButtonPress();
});

let nodeNumber = 2;
let nodeXPos = 200;
let nodeYPos = 0;

let addNodeButtonPress = async () => {
    nodeNumber++;
    nodeYPos += 50;
    customCy.add({
        group: 'nodes',
        data: {id: nodeNumber.toString(), name: nodeNumber.toString()},
        position: {x: nodeXPos, y: nodeYPos}
    });
    // customCy.layout();
}

document.getElementById('graphCustomButton').addEventListener('click', function () {
    graphCustomButtonPress();
});

// let graphCustomButtonPress = async () => {
//     let adjacencyMatrix = createAdjacencyMatrix(customCy);
//     console.log(adjacencyMatrix.toArray());
//     eel.setStaticCustomGraph();
// }

// eel.expose(sendAdjacencyMatrix);

function sendAdjacencyMatrix() {
    return createAdjacencyMatrix(customCy);
}

function createAdjacencyMatrix(graph) {
    let adjacencyMatrix = math.zeros(graph.json().elements.nodes.length, graph.json().elements.nodes.length)

    for (let edg of graph.json().elements.edges) {
        console.log(`Source: ${edg.data.source} -> Target: ${edg.data.target}`);
        adjacencyMatrix.subset(math.index(parseInt(edg.data.source), parseInt(edg.data.target)), 1);
        adjacencyMatrix.subset(math.index(parseInt(edg.data.target), parseInt(edg.data.source)), 1);
    }
    return adjacencyMatrix;
}

document.getElementById('clearGraphButton').addEventListener('click', function () {
    eh.disableDrawMode();
});