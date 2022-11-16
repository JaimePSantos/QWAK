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
// #### INPUTS & DISPLAYS ####
let inputDim = document.getElementById("inputDim");
let inputGraph = document.getElementById("inputGraph");
let inputTimeRange = document.getElementById("inputTimeRange");
let inputInitStateRange = document.getElementById("inputInitStateRange");

// #### JAVASCRIPT QUANTUM WALK OBJECTS ####
let defaultN = 100;
let defaultGraph = 'nx.cycle_graph';
let defaultTimeList = [0, 10];
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

// SETTING THE GRAPH
// - Graph Generator
cy.layout({name: "circle"}).run();

$(function () {
    $('#runGraphButton').on('click', async function (e) {
        e.preventDefault();
        dynamicQuantumWalk.reset();
        dynamicQuantumWalk.graph = inputGraph.value;
        dynamicQuantumWalk.dim = parseInt(inputDim.value);
        setDynamicDim(dynamicQuantumWalk.dim, dynamicQuantumWalk.graph);
        setDynamicGraph(dynamicQuantumWalk.graph);
        let myGraph = await getDynamicGraph();
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


// - Custom Graph
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

// #### DYNAMIC QUANTUM WALK  ####

// #### #### PROB DIST ANIMATION #### ####

let myAnimatedChart = new Chart(document.getElementById("dynamicProbDistChart").getContext("2d"), dynamicChartData);

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

function setDynamicJsInitStateList(){
    dynamicQuantumWalk.initState = inputInitStateRange.value;
    setDynamicPyInitStateList(dynamicQuantumWalk.initState);
}

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

function setDynamicJsTime(){
    dynamicQuantumWalk.time = (inputTimeRange.value);
    setDynamicPyTime(dynamicQuantumWalk.time);
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

// $(function () {
//     $('#dynamicProbDistButton').on('click', async function (e) {
//         e.preventDefault();
//         dynamicQuantumWalk.reset();
//         setDynamicJsTime();
//         setDynamicJsInitStateList();
//         let dynamicProbDist = await getDynamicQuantity('runMultipleWalks');
//         await setDynamicProbDist(dynamicProbDist);
//     });
// });

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
        setDynamicJsTime();
        setDynamicJsInitStateList();
        await setDynamicProbDistDB(dynamicQuantumWalk.walkName);
        dynamicQuantumWalk.probDist = await getDynamicProbDistDB(dynamicQuantumWalk.walkName);
        plotDynamicProbDist(dynamicQuantumWalk.probDist);
    });
});

function plotDynamicProbDist(multipleWalks) {
    // console.log(walk)
    if (multipleWalks.hasError == true) {
        alert(multipleWalks.probDist);
        return;
    } else {
        let i = 0;
        let animationSteps = 100;
        myAnimatedChart.clear();
        for (const walk of multipleWalks.probDist) {
            setTimeout(() => {
                dynamicChartData.data.datasets[0].data = walk.flat();
                dynamicChartData.data.labels = [...Array(walk.length).keys()];
                dynamicChartData.options.scales.y.ticks.beginAtZero = false;
                myAnimatedChart.update();
            }, animationSteps * i);
            i++;
        }
    }
}

async function setDynamicProbDistDB(walkName) {
    await $.ajax({
        type: 'POST',
        url: `/setRunMultipleWalksDB`,
        data:{walkName:walkName},
        success: function () {
            console.log(`success - Runwalk`);
        },
        error: function (response) {
            console.log('Runwalk error');
        }
    });
}

async function getDynamicProbDistDB(walkName) {
    let myWalk;
    await $.ajax({
        type: 'POST',
        url: `/getRunMultipleWalksDB`,
        data:{walkName:walkName},
        success: function (response) {
            console.log(`success - Runwalk ${response}`);
            myWalk = response;
        },
        error: function (response) {
            console.log('Runwalk error');
            myWalk = 0;
        }
    });
    return myWalk;
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

// #### #### GRAPH GENERATOR #### ####

// document.getElementById("runGraphButton").addEventListener('click', async function () {
//     setRunGraph();
// });

// document.getElementById("setDimButton").addEventListener('click', async function () {
//     setDimButton();
// });


// let setRunGraph = async () => {
//     setDynamicGraph();
//     let myGraph = await getDynamicGraph();
//     updateGraph(myGraph);
// }

// let setDimButton = async () => {
//     dynamicQuantumWalk.dim = parseInt(inputDim.value);
//     dynamicQuantumWalk.graph = inputGraph.value;
//     eel.setDynamicDim(dynamicQuantumWalk.dim, dynamicQuantumWalk.graph);
// }

// let setDynamicGraph = async () => {
//     dynamicQuantumWalk.graph = inputGraph.value;
//     eel.setDynamicGraph(dynamicQuantumWalk.graph);
// }

// let getDynamicGraph = () => {
//     return eel
//         .getDynamicGraphToJson()()
//         .then((a) => {
//             return a ? a : Promise.reject(Error("Get Graph failed."));
//         })
//         .catch((e) => console.log(e));
// };

// #### CUSTOM GRAPH ####
// var eh = customCy.edgehandles();
//
// document.getElementById('addEdgeButton').addEventListener('click', function () {
//     eh.enableDrawMode();
// });
//
// document.getElementById("addNodeButton").addEventListener('click', function () {
//     addNodeButtonPress();
// });
//
// let nodeNumber = 2;
// let nodeXPos = 200;
// let nodeYPos = 0;
//
// let addNodeButtonPress = async () => {
//     nodeNumber++;
//     nodeYPos += 50;
//     customCy.add({
//         group: 'nodes',
//         data: {id: nodeNumber.toString(), name: nodeNumber.toString()},
//         position: {x: nodeXPos, y: nodeYPos}
//     });
//     // customCy.layout();
// }
//
// document.getElementById('graphCustomButton').addEventListener('click', function () {
//     graphCustomButtonPress();
// });
//
// let graphCustomButtonPress = async () => {
//     let adjacencyMatrix = createAdjacencyMatrix(customCy);
//     console.log(adjacencyMatrix.toArray());
//     eel.setDynamicCustomGraph();
// }
//
// // eel.expose(sendAdjacencyMatrix);
// function sendAdjacencyMatrix() {
//     return createAdjacencyMatrix(customCy);
// }
//
// function createAdjacencyMatrix(graph) {
//     let adjacencyMatrix = math.zeros(graph.json().elements.nodes.length, graph.json().elements.nodes.length)
//
//     for (let edg of graph.json().elements.edges) {
//         console.log(`Source: ${edg.data.source} -> Target: ${edg.data.target}`);
//         adjacencyMatrix.subset(math.index(parseInt(edg.data.source), parseInt(edg.data.target)), 1);
//         adjacencyMatrix.subset(math.index(parseInt(edg.data.target), parseInt(edg.data.source)), 1);
//     }
//     return adjacencyMatrix;
// }
//
// document.getElementById('clearGraphButton').addEventListener('click', function () {
//     eh.disableDrawMode();
// });

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