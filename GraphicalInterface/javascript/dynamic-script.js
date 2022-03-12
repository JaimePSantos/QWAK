import { cy, customCy} from "./dynamic-tools.js";
import { DynamicQuantumwalk } from "./dynamicQuantumwalk.js";

let inputDim = document.getElementById("inputDim");
let inputGraph = document.getElementById("inputGraph");

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
    staticQuantumWalk.dim = parseInt(inputDim.value);
    staticQuantumWalk.graph = inputGraph.value;
    eel.setDim(staticQuantumWalk.dim, staticQuantumWalk.graph);
}

let setGraph = async () => {
    staticQuantumWalk.graph = inputGraph.value;
    eel.setGraph(staticQuantumWalk.graph);
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