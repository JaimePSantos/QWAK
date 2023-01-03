import {
    customCy,
    cy,
    staticChartData,
    dynamicChartData,
    dynamicInvPartRatioChartData,
    dynamicMeanChartData,
    dynamicStDevChartData,
    dynamicSurvivalProbChartData
} from "./dynamic-tools.js";

import {DynamicQuantumwalk} from "./dynamicQuantumwalk.js";
import {setDynamicDim,setDynamicGraph,getDynamicGraph,updateGraph,addNodeButtonPress,setCustomAdjacencyMatrix,createAdjacencyMatrix,adjacencyMatrixToString} from "./js-dynamic/dynamic-graph.js"

import {plotDynamicProbDist, setDynamicProbDistDB,getDynamicProbDistDB} from "./js-dynamic/dynamic-probDist.js"

// #### INPUTS & DISPLAYS ####
let inputDim = document.getElementById("inputDim");
let inputGraph = document.getElementById("inputGraph");
let inputTimeRange = document.getElementById("inputTimeRange");
let inputInitStateRange = document.getElementById("inputInitStateRange");

// #### JAVASCRIPT QUANTUM WALK OBJECTS ####
let defaultN = 5;
let defaultGraph = 'nx.cycle_graph';
let defaultTimeList = [0, 5];
let defaultInitStateList = [[Math.floor(defaultN / 2)]];
let defaultProbDist = [];
let defaultWalkName = "Placeholder";

let dynamicQuantumWalk = new DynamicQuantumwalk(defaultGraph, defaultTimeList, defaultInitStateList,defaultWalkName,defaultProbDist);

let inputRangeInit = () => {
    inputDim.value = defaultN;
    inputGraph.value = defaultGraph;
    inputTimeRange.value = defaultTimeList;
    inputInitStateRange.value = defaultInitStateList;
}

inputRangeInit();

async function getDynamicQuantity(quantity) {
    let quant;
    await $.ajax({
        type: 'POST',
        url: `/${quantity}`, // <- Add the queryparameter here
        success: function (response) {
            quant = response;
            console.log(`Success:\t ${quantity} -> ${quant}`);
            return quant;
        },
        error: function (response) {
            console.log(`Error:\t ${quantity}`);
            quant = 'error'
            return quant;
        }
    });
    return quant;
}

// Graph Generator
cy.layout({name: "circle"}).run();

$(function () {
    $('#runGraphButton').on('click', async function (e) {
        e.preventDefault();
        dynamicQuantumWalk.reset();
        dynamicQuantumWalk.graph = inputGraph.value;
        dynamicQuantumWalk.dim = parseInt(inputDim.value);
        let myGraph =  await setDynamicGraph(dynamicQuantumWalk.dim,dynamicQuantumWalk.graph);
        updateGraph(myGraph);
    });
});

$(function () {
    $('#setDimButton').on('click', function (e) {
        e.preventDefault();
        dynamicQuantumWalk.graph = inputGraph.value;
        dynamicQuantumWalk.dim = parseInt(inputDim.value);
        setDynamicDim(dynamicQuantumWalk.dim, dynamicQuantumWalk.graph)
    });
});


// #### CUSTOM GRAPH ####

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
        dynamicQuantumWalk.reset();
        let customAdjacency = createAdjacencyMatrix(customCy);
        await setCustomAdjacencyMatrix(customAdjacency);
    });
});

// #### #### PROB DIST ANIMATION #### ####

$(function () {
    $('#setInitStateRangeButton').on('click', function (e) {
        e.preventDefault();
        setDynamicJsInitStateList();
    });
});

$(function () {
    $('#setTimeRangeButton').on('click', function (e) {
        e.preventDefault();
        setDynamicJsTime();
    });
});

function setDynamicPyInitStateList(initStateStr) {
    $.ajax({
        type: 'POST',
        url: `/setDynamicInitStateList`, // <- Add the queryparameter here
        data: {initStateStr: initStateStr},
        success: function (response) {
            console.log('success - InitState set to ${initStateStr}');
        },
        error: function (response) {
            console.log('InitState error');
        }
    });
}

$(function () {
    $('#dynamicProbDistButton').on('click', async function (e) {
        var currentdate = new Date();
        dynamicQuantumWalk.walkName = `DynamicQWAK-${currentdate.getDate() + "/"
                + (currentdate.getMonth()+1)  + "/" 
                + currentdate.getFullYear() + "-"  
                + currentdate.getHours() + ":"  
                + currentdate.getMinutes() + ":" 
                + currentdate.getSeconds()
        }`;
        e.preventDefault();
        dynamicQuantumWalk.reset();
        await setDynamicProbDistDB(inputDim.value,inputGraph.value,inputTimeRange.value,inputInitStateRange.value);
        let walkResult = await getDynamicProbDistDB(dynamicQuantumWalk.walkName);
         if(walkResult[0] == "True"){
            dynamicQuantumWalk.hasError = true;
            dynamicQuantumWalk.probDist = walkResult[1];
        }else{
            dynamicQuantumWalk.hasError = false;
            dynamicQuantumWalk.probDist = walkResult[1]['prob'];
        }
        plotDynamicProbDist(dynamicQuantumWalk.probDist);
    });
});

function setDynamicJsTime(){
    dynamicQuantumWalk.time = (inputTimeRange.value);
    setDynamicPyTime(dynamicQuantumWalk.time);
}

function setDynamicJsInitStateList(){
    dynamicQuantumWalk.initState = inputInitStateRange.value;
    setDynamicPyInitStateList(dynamicQuantumWalk.initState);
}

function setDynamicPyTime(newTime) {
    $.ajax({
        type: 'POST',
        url: `/setDynamicTime`, // <- Add the queryparameter here
        data: {newTime: newTime},
        success: function (response) {
            console.log('success - Time set to ${newTime}');
        },
        error: function (response) {
            console.log('setTime error');
        }
    });
}
// #### #### MEAN PLOT #### ####

let myDynamicMeanChart = new Chart(document.getElementById("dynamicMeanChart").getContext("2d"), dynamicMeanChartData)

$(function () {
    $('#dynamicMeanButton').on('click', async function (e) {
        setDynMean();
    });
});

let setDynMean = async () => {
    let dynMean = [];
    dynMean = await getDynamicQuantity('getDynamicMean');
    dynamicMeanChartData.data.datasets[0].data = dynMean.flat();
    dynamicMeanChartData.data.labels = [...Array(dynMean.length).keys()];
    myDynamicMeanChart.clear();
    myDynamicMeanChart.update();
}

// #### #### STDEV PLOT #### ####
//
let dynStdevChartData = JSON.parse(JSON.stringify(dynamicStDevChartData))
let myDynamicStDevChart = new Chart(document.getElementById("dynamicStDevChart").getContext("2d"), dynStdevChartData);

$(function () {
    $('#dynamicStDevButton').on('click', async function (e) {
        setDynStDev();
    });
});

let setDynStDev = async () => {
    let dynStDev = [];
    dynStDev = await getDynamicQuantity('getDynamicStDev');
    myDynamicStDevChart.data.datasets[0].data = dynStDev.flat()
    myDynamicStDevChart.data.labels = [...Array(dynStDev.length).keys()];
    myDynamicStDevChart.clear();
    myDynamicStDevChart.update();
}

// #### #### INV PART RATIO PLOT #### ####

let myDynamicInvPartRatioChart = new Chart(document.getElementById("dynamicInvPartRatioChart").getContext("2d"), dynamicInvPartRatioChartData)

$(function () {
    $('#dynamicInvPartRatioButton').on('click', async function (e) {
        setDynInvPartRatio();
    });
});

let setDynInvPartRatio = async () => {
    let dynInvPartRatio = await getDynamicQuantity('getDynamicInvPartRatio');
    dynamicInvPartRatioChartData.data.datasets[0].data = dynInvPartRatio.flat();
    dynamicInvPartRatioChartData.data.labels = [...Array(dynInvPartRatio.length).keys()];
    myDynamicInvPartRatioChart.clear();
    myDynamicInvPartRatioChart.update();
}

// #### #### SURVIVAL PROB PLOT #### ####

let myDynamicSurvivalProbChart = new Chart(document.getElementById("dynamicSurvivalProbChart").getContext("2d"), dynamicSurvivalProbChartData)

$(function () {
    $('#dynamicSurvivalProbButton').on('click', async function (e) {
        setDynSurvProb();
    });
});

let setDynSurvProb = async () => {
    let k0 = document.getElementById("dynInputSurvProbNodeA").value
    let k1 = document.getElementById("dynInputSurvProbNodeB").value
    let dynSurvProb = await getDynamicSurvivalProb(k0, k1);
    if(dynSurvProb[0]==true){
        alert(dynSurvProb[1]);
        return;
    }else{
        dynamicSurvivalProbChartData.data.datasets[0].data = dynSurvProb[1].flat();
        dynamicSurvivalProbChartData.data.labels = [...Array(dynSurvProb[1].length).keys()];
        myDynamicSurvivalProbChart.clear();
        myDynamicSurvivalProbChart.update();
    }
}
async function getDynamicSurvivalProb(fromNode, toNode) {
    // TODO: Should add an error for when the nodes in the interval are larger than the graph.
    let dynamicSurvivalProb;
    await $.ajax({
        type: 'POST',
        url: `/getDynamicSurvivalProb`,
        data: {fromNode: fromNode, toNode: toNode},
        success: function (response) {
            dynamicSurvivalProb = response;
            console.log(`success - dynamicSurvivalProb ${dynamicSurvivalProb}`);
            return dynamicSurvivalProb;
        },
        error: function (response) {
            console.log('dynamicSurvivalProb error');
            dynamicSurvivalProb = 'error'
            return dynamicSurvivalProb;
        }
    });
    return dynamicSurvivalProb;
}

function openTab(evt, graph, tabcontent, tablinks) {
    // Declare all variables
    var i, tabcontent, tablinks;

    // Get all elements with class="tabcontent" and hide them
    tabcontent = document.getElementsByClassName(tabcontent);
    for (i = 0; i < tabcontent.length; i++) {
        tabcontent[i].style.display = "none";
    }

    // Get all elements with class="tablinks" and remove the class "active"
    tablinks = document.getElementsByClassName(tablinks);
    for (i = 0; i < tablinks.length; i++) {
        tablinks[i].className = tablinks[i].className.replace(" active", "");
    }

    // Show the current tab, and add an "active" class to the button that opened the tab
    document.getElementById(graph).style.display = "block";
    evt.currentTarget.className += " active";
}
