import {customCy, cy} from "./js-static/static-tools.js";
import {staticChartData} from "./js-static/static-charts.js";
import {StaticQuantumwalk} from "./js-static/staticQuantumwalk.js";
import {
    setStaticGraph,
    updateGraph,
    addNodeButtonPress,
    setCustomAdjacencyMatrix,
    createAdjacencyMatrix,
    } from "./graphs.js"
import {deleteWalkEntry,
    getStaticProbDistDB,
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
        updateGraph(myGraph,cy);
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
    addNodeButtonPress(customCy);
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
    console.log(staticQuantumWalk.time)
    await setStaticPyTime(staticQuantumWalk.time);
}

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
        console.log(inputTime.value)
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
    let survProb = await getStaticSurvivalProb(fromNode,toNode);
    if(survProb[0]==true){
        alert(survProb[1]);
    }else{
        staticQuantumWalk.survivalProb = survProb[1];
        inputSurvProbResult.value = staticQuantumWalk.survivalProb;
    }
}

async function setPst(nodeA, nodeB) {
    staticQuantumWalk.PST = await getPst(nodeA, nodeB);
    if (staticQuantumWalk.PST[0] == true) {
        alert(staticQuantumWalk.PST[1]);
        return;
    } else {
        if (staticQuantumWalk.PST[1] < 0) {
            inputPSTResult.value = 'No PST.';
        } else {
            inputPSTResult.value = staticQuantumWalk.PST[1];
        }
    }
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

window.addEventListener("resize", function(){
    cy.resize();
    customCy.resize();
    cy.fit();
    customCy.fit();
});