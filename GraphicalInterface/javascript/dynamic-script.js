import { cy, customCy, dynamicChartData} from "./dynamic-tools.js";
import { DynamicQuantumwalk } from "./dynamicQuantumwalk.js";

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

// #### GRAPHS  ####

cy.layout({ name: "circle" }).run();

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
    cy.layout({ name: "circle" }).run();
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
    customCy.add({ group: 'nodes', data: { id: nodeNumber.toString(), name: nodeNumber.toString() },  position: { x: nodeXPos, y: nodeYPos }});
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
function sendAdjacencyMatrix(){
    return createAdjacencyMatrix(customCy);
}

function createAdjacencyMatrix(graph) {
    let adjacencyMatrix = math.zeros(graph.json().elements.nodes.length, graph.json().elements.nodes.length)

    for(let edg of graph.json().elements.edges){
        console.log(`Source: ${edg.data.source} -> Target: ${edg.data.target}`);
        adjacencyMatrix.subset(math.index(parseInt(edg.data.source), parseInt(edg.data.target)), 1);
        adjacencyMatrix.subset(math.index(parseInt(edg.data.target), parseInt(edg.data.source)), 1);
    }
    return adjacencyMatrix;
}

document.getElementById('clearGraphButton').addEventListener('click', function () {
    eh.disableDrawMode();
});