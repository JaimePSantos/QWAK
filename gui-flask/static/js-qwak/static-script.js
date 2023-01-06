import {customCy, cy, staticChartData} from "./static-tools.js";
import {StaticQuantumwalk} from "./staticQuantumwalk.js";
import {setStaticDim,
    setStaticGraph,
    updateGraph,
    getStaticGraph,
    addNodeButtonPress,
    setCustomAdjacencyMatrix,
    createAdjacencyMatrix,
    adjacencyMatrixToString} from "./js-static/static-graph.js"
import { deleteAllWalkEntries,
    deleteWalkEntry,
    getStaticProbDistDB,
    setStaticProbDistDB,
    plotStaticProbDistDB,
    setStaticPyInitState,
    setStaticPyTime,
    getStaticSurvivalProb,
} from "./js-static/static-probDist.js"

// #### INPUTS & DISPLAYS ####

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
let defaultN = 5;
let defaultT = 1;
let defaultInitState = [Math.floor(defaultN / 2)];
let defaultGraph = 'nx.cycle_graph';
let defaultProbDist = [];
let defaultWalkName = "Placeholder";

let staticQuantumWalk = new StaticQuantumwalk(defaultN, defaultT, defaultInitState, defaultGraph,defaultProbDist,defaultWalkName);

let inputInit = () => {
    inputTime.value = defaultT;
    inputInitState.value = defaultInitState
    inputDim.value = defaultN;
    inputGraph.value = defaultGraph;
}

inputInit();
async function setStaticQuantity(quantity) {
    await $.ajax({
        type: 'POST',
        url: `/${quantity}`,
        data:{walkName:walkName},
        success: function () {
            console.log(`Success:\t ${quantity} -> ${quant}`);
        },
        error: function (response) {
            console.log(`Error:\t ${quantity}`);
        }
    });
}

// Graph generator buttons

$(async function () {
    $('#runGraphButton').on('click', async function (e) {
        e.preventDefault();
        staticQuantumWalk.reset();
        staticQuantumWalk.graph = inputGraph.value;
        staticQuantumWalk.dim = parseInt(inputDim.value);
        let myGraph = await setStaticGraph(staticQuantumWalk.dim,staticQuantumWalk.graph);
        updateGraph(myGraph);
    });
});

$(function () {
    $('#setDimButton').on('click', async function (e) {
        e.preventDefault();
        staticQuantumWalk.graph = inputGraph.value;
        staticQuantumWalk.dim = parseInt(inputDim.value);
        await setStaticDim(staticQuantumWalk.dim, staticQuantumWalk.graph)
    });
});

$(function () {
    $('#setGraphButton').on('click', async function (e) {
        e.preventDefault();
        staticQuantumWalk.graph = inputGraph.value;
        staticQuantumWalk.dim = parseInt(inputDim.value);
        await setStaticGraph(staticQuantumWalk.dim, staticQuantumWalk.graph)
    });
});

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
        staticQuantumWalk.reset();
        let customAdjacency = createAdjacencyMatrix(customCy);
        await setCustomAdjacencyMatrix(customAdjacency);
    });
});

// SETTING PROBDIST

async function setStaticJsInitState(){
    staticQuantumWalk.initState = inputInitState.value;
    await setStaticPyInitState(staticQuantumWalk.initState);
}

export async function setStaticJsTime(){
    staticQuantumWalk.time = (inputTime.value);
    await setStaticPyTime(staticQuantumWalk.time);
}

$(function () {
    $('#setInitStateButton').on('click', async function (e) {
        e.preventDefault();
        await setStaticJsInitState();
    });
});

$(function () {
    $('#setTimeButton').on('click', async function (e) {
        e.preventDefault();
        await setStaticJsTime();
    });
});

$(function () {
    $('#staticProbDistButton').on('click', async function (e) {
        var currentdate = new Date();
        staticQuantumWalk.walkName = `StaticQWAK-${currentdate.getDate() + "/"
                + (currentdate.getMonth()+1)  + "/" 
                + currentdate.getFullYear() + "-"  
                + currentdate.getHours() + ":"  
                + currentdate.getMinutes() + ":" 
                + currentdate.getSeconds()
        }`;
        e.preventDefault();
        staticQuantumWalk.reset();
        let walkResult = await getStaticProbDistDB(inputDim.value,inputGraph.value,inputTime.value,inputInitState.value);
        if(walkResult[0] == true){
            staticQuantumWalk.probDist = walkResult[1];
            alert(staticQuantumWalk.probDist)
        }else{
            staticQuantumWalk.hasError = false;
            staticQuantumWalk.probDist = walkResult[1]['prob'];
            staticQuantumWalk.mean = walkResult[1]['mean'];
            staticQuantumWalk.sndMoment = walkResult[1]['sndMoment'];
            staticQuantumWalk.stDev = walkResult[1]['stDev'];
            staticQuantumWalk.invPartRatio = walkResult[1]['invPartRatio'];
            plotStaticProbDistDB(staticQuantumWalk);
            await setStaticMean();
            await setStaticSndMoment();
            await setStaticStDev();
            await setStaticInversePartRatio();
        }

    });
});

$(function () {
    $('#setGammaButton').on('click', async function (e) {
        await deleteWalkEntry(staticQuantumWalk.walkName);
    });
});

$(function () {
    $('#setPlaceholderButton').on('click', async function (e) {
        await deleteAllWalkEntries();
    });
});

//SETTING STATISTICS
$(function () {
    $('#survProbNodesButton').on('click', async function (e) {
        e.preventDefault();
        let fromNode = inputSurvProbNodeA.value;
        let toNode = inputSurvProbNodeB.value;
        await setStaticSurvivalProb(fromNode, toNode);
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
    inputMean.value = staticQuantumWalk.mean;
}

async function setStaticSndMoment() {
    inputSndMoment.value = staticQuantumWalk.sndMoment;
}

async function setStaticStDev() {
    inputStDev.value = staticQuantumWalk.stDev;
}

async function setStaticInversePartRatio() {
    inputInvPartRat.value = staticQuantumWalk.invPartRatio;
}

async function setStaticSurvivalProb(fromNode, toNode) {
    staticQuantumWalk.survivalProb = await getStaticSurvivalProb(fromNode,toNode);
    inputSurvProbResult.value = staticQuantumWalk.survivalProb
}

async function setPst(nodeA, nodeB) {
    staticQuantumWalk.PST = await getPst(nodeA, nodeB);
    inputPSTResult.value = staticQuantumWalk.PST
    // if (PST[0] == true) {
    //     alert(PST[1]);
    //     return;
    // } else {
    //     if (PST[1] < 0) {
    //         inputPSTResult.value = 'No PST.';
    //     } else {
    //         inputPSTResult.value = PST[1];
    //     }
    // }
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

// async function getStaticSurvivalProb(fromNode, toNode) {
//     let staticSurvivalProb;
//     await $.ajax({
//         type: 'POST',
//         url: `/getStaticSurvivalProb`,
//         data: {fromNode: fromNode, toNode: toNode},
//         success: function (response) {
//             staticSurvivalProb = response;
//             console.log(`success - staticSurvivalProb ${staticSurvivalProb}`);
//             return staticSurvivalProb;
//         },
//         error: function (response) {
//             console.log('staticSurvivalProb error');
//             staticSurvivalProb = 'error'
//             return staticSurvivalProb;
//         }
//     });
//     return staticSurvivalProb;
// }

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

// #### DATABASE ####

