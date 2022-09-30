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

// #### STATIC QUANTUM WALK  ####

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
            console.log('success 1');
            console.log(response)
        },
        error: function (response) {
            console.log('error');
        }
    });
}

function setStaticGraph(newGraph) {
    $.ajax({
        type: 'POST',
        url: `/setStaticGraph`,
        data: {newGraph: newGraph},
        success: function (response) {
            console.log('success 2');
            console.log(response)
        },
        error: function (response) {
            console.log('error');
        }
    })
}

async function getStaticGraph() {
    let myGraph;
    await $.ajax({
        type: 'POST',
        url: `/getStaticGraphToJson`, // <- Add the queryparameter here
        success: function (response) {
            console.log('success 3');
            myGraph = response;
            console.log(myGraph);
            return myGraph;
        },
        error: function (response) {
            console.log('error');
            myGraph = 'error'
            return myGraph;
        }
    });
    return myGraph;
}

document.getElementById("setInitStateButton").addEventListener('click', async function () {
    setInitState();
});

document.getElementById("setTimeButton").addEventListener('click', async function () {
    setTime();
});

document.getElementById("staticProbDistButton").addEventListener('click', async function () {
    setStaticProbDist();
});

// let setInitState = async () => {
//     staticQuantumWalk.initState = inputInitState.value;
//     eel.setInitState(staticQuantumWalk.initState);
// }

// let setTime = async () => {
//     staticQuantumWalk.time = (inputTime.value);
//     eel.setTime(staticQuantumWalk.time);
// }

let setStaticProbDist = async () => {
    // let walk = await getWalk();
    let walk = [false, 5]
    if (walk[0] == true) {
        alert(walk[1]);
        return;
    } else {
        console.log(walk[1]);
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

let getWalk = () => {
    return eel
        .runWalk()()
        .then((a) => {
            return a;
        })
        .catch((e) => console.log(e));
};

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