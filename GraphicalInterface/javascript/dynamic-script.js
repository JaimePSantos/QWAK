import {
    customCy,
    cy,
    dynamicChartData,
    dynamicInvPartRatioChartData,
    dynamicMeanChartData,
    dynamicStDevChartData,
    dynamicSurvivalProbChartData
} from "./dynamic-tools.js";
import {DynamicQuantumwalk} from "./dynamicQuantumwalk.js";

// #### INPUTS & DISPLAYS ####
let inputDim = document.getElementById("inputDim");
let inputGraph = document.getElementById("inputGraph");
let inputTimeRange = document.getElementById("inputTimeRange");
let inputInitStateRange = document.getElementById("inputInitStateRange");

// #### JAVASCRIPT QUANTUM WALK OBJECTS ####
let defaultN = 100;
let defaultGraph = 'nx.cycle_graph';
let defaultTimeList = [0, 100];
let defaultInitStateList = [[Math.floor(defaultN / 2)]];

let dynamicQuantumWalk = new DynamicQuantumwalk(defaultGraph, defaultTimeList, defaultInitStateList);

let inputRangeInit = () => {
    inputDim.value = defaultN;
    inputGraph.value = defaultGraph;
    inputTimeRange.value = defaultTimeList;
    inputInitStateRange.value = defaultInitStateList;
}

inputRangeInit();

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


// #### DYNAMIC QUANTUM WALK  ####

// #### #### PROB DIST ANIMATION #### ####

let myAnimatedChart = new Chart(document.getElementById("dynamicProbDistChart").getContext("2d"), dynamicChartData);

document.getElementById("setInitStateRangeButton").addEventListener('click', async function () {
    setInitStateRange();
});

document.getElementById("setTimeRangeButton").addEventListener('click', async function () {
    setTimeRange();
});

document.getElementById("dynamicProbDistButton").addEventListener('click', async function () {
    setdynamicProbDist();
});

let setInitStateRange = async () => {
    dynamicQuantumWalk.initStateList = inputInitStateRange.value;
    eel.setInitStateList(dynamicQuantumWalk.initStateList);
}

let setTimeRange = async () => {
    dynamicQuantumWalk.timeList = inputTimeRange.value;
    eel.setTimeList(dynamicQuantumWalk.timeList);
}

let setdynamicProbDist = async () => {
    let multipleWalks = await getMultipleWalks();
    let i = 0;
    let animationSteps = 100;
    myAnimatedChart.clear();
    for (const walk of multipleWalks) {
        setTimeout(() => {
            dynamicChartData.data.datasets[0].data = walk.flat();
            dynamicChartData.data.labels = [...Array(walk.length).keys()];
            dynamicChartData.options.scales.y.ticks.beginAtZero = false;
            myAnimatedChart.update();
        }, animationSteps * i);
        i++;
    }
}

let getMultipleWalks = () => {
    return eel
        .runMultipleWalks()()
        .then((a) => {
            return a ? a : Promise.reject(Error("Get Multiple Walks failed."));
        })
        .catch((e) => console.log(e));
};

// #### #### MEAN PLOT #### ####

let myDynamicMeanChart = new Chart(document.getElementById("dynamicMeanChart").getContext("2d"), dynamicMeanChartData)

document.getElementById("dynamicMeanButton").addEventListener('click', async function () {
    setDynMean();
});

let setDynMean = async () => {
    let dynMean = await getDynMean();
    dynamicMeanChartData.data.datasets[0].data = dynMean.flat();
    dynamicMeanChartData.data.labels = [...Array(dynMean.length).keys()];
    myDynamicMeanChart.clear();
    myDynamicMeanChart.update();
}

let getDynMean = () => {
    return eel
        .getDynMean()()
        .then((a) => {
            // if (Array.isArray(a)){
            //         Promise.reject(Error("Get Dynamic Mean failed: Mean is not an array."));
            //     }else{
            //         return a;
            // }
            return a;
        })
        .catch((e) => console.log(e));
}

// #### #### STDEV PLOT #### ####

let myDynamicStDevChart = new Chart(document.getElementById("dynamicStDevChart").getContext("2d"), dynamicStDevChartData)

document.getElementById("dynamicStDevButton").addEventListener('click', async function () {
    setDynStDev();
});

let setDynStDev = async () => {
    let dynStDev = await getDynStDev();
    dynamicStDevChartData.data.datasets[0].data = dynStDev.flat();
    dynamicStDevChartData.data.labels = [...Array(dynStDev.length).keys()];
    myDynamicStDevChart.clear();
    myDynamicStDevChart.update();
}

let getDynStDev = () => {
    return eel
        .getDynStDev()()
        .then((a) => {
            // if (Array.isArray(a)){
            //         Promise.reject(Error("Get Dynamic Mean failed: Mean is not an array."));
            //     }else{
            //         return a;
            // }
            return a;
        })
        .catch((e) => console.log(e));
}

// #### #### INV PART RATIO PLOT #### ####

let myDynamicInvPartRatioChart = new Chart(document.getElementById("dynamicInvPartRatioChart").getContext("2d"), dynamicInvPartRatioChartData)

document.getElementById("dynamicInvPartRatioButton").addEventListener('click', async function () {
    setDynInvPartRatio();
});

let setDynInvPartRatio = async () => {
    let dynInvPartRatio = await getDynInvPartRatio();
    dynamicInvPartRatioChartData.data.datasets[0].data = dynInvPartRatio.flat();
    dynamicInvPartRatioChartData.data.labels = [...Array(dynInvPartRatio.length).keys()];
    myDynamicInvPartRatioChart.clear();
    myDynamicInvPartRatioChart.update();
}

let getDynInvPartRatio = () => {
    return eel
        .getDynInvPartRatio()()
        .then((a) => {
            // if (Array.isArray(a)){
            //         Promise.reject(Error("Get Dynamic Mean failed: Mean is not an array."));
            //     }else{
            //         return a;
            // }
            return a;
        })
        .catch((e) => console.log(e));
}

// #### #### SURVIVAL PROB PLOT #### ####

let myDynamicSurvivalProbChart = new Chart(document.getElementById("dynamicSurvivalProbChart").getContext("2d"), dynamicSurvivalProbChartData)

document.getElementById("dynamicSurvivalProbButton").addEventListener('click', async function () {
    setDynSurvProb();
});

let setDynSurvProb = async () => {
    let k0 = document.getElementById("dynInputSurvProbNodeA").value
    let k1 = document.getElementById("dynInputSurvProbNodeB").value
    let dynSurvProb = await getDynSurvProb(k0, k1);
    dynamicSurvivalProbChartData.data.datasets[0].data = dynSurvProb.flat();
    dynamicSurvivalProbChartData.data.labels = [...Array(dynSurvProb.length).keys()];
    myDynamicSurvivalProbChart.clear();
    myDynamicSurvivalProbChart.update();
}

let getDynSurvProb = (k0, k1) => {
    return eel
        .getDynSurvivalProb(k0, k1)()
        .then((a) => {
            // if (Array.isArray(a)){
            //         Promise.reject(Error("Get Dynamic Mean failed: Mean is not an array."));
            //     }else{
            //         return a;
            // }
            return a;
        })
        .catch((e) => console.log(e));
}

// #### GRAPHS  ####

cy.layout({name: "circle"}).run();

// #### #### GRAPH GENERATOR #### ####

document.getElementById("runGraphButton").addEventListener('click', async function () {
    setRunGraph();
});

let setRunGraph = async () => {
    let myGraph = await getGraph();
    updateGraph(myGraph);
    setGraph();
    setDimButton();
}

let setDimButton = async () => {
    dynamicQuantumWalk.dim = parseInt(inputDim.value);
    dynamicQuantumWalk.graph = inputGraph.value;
    eel.setDim(dynamicQuantumWalk.dim, dynamicQuantumWalk.graph);
}

let setGraph = async () => {
    dynamicQuantumWalk.graph = inputGraph.value;
    eel.setGraph(dynamicQuantumWalk.graph);
}

let getGraph = () => {
    return eel
        .graphToJson()()
        .then((a) => {
            return a ? a : Promise.reject(Error("Get Graph failed."));
        })
        .catch((e) => console.log(e));
};

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

let graphCustomButtonPress = async () => {
    let adjacencyMatrix = createAdjacencyMatrix(customCy);
    console.log(adjacencyMatrix.toArray());
    eel.customGraphWalk();
}

eel.expose(sendAdjacencyMatrix);

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

  
