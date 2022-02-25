import { defaultDist, cy, data, data2, customCy } from "./tools.js";
import { StaticQuantumwalk } from "./staticQuantumwalk.js";
import { DynamicQuantumwalk } from "./dynamicQuantumwalk.js";


// #### INPUTS & DISPLAYS ####
let inputTime = document.getElementById("inputTime");
let inputDim = document.getElementById("inputDim");
let inputGraph = document.getElementById("inputGraph");
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

let inputTimeRange = document.getElementById("inputTimeRange");
let inputInitStateRange = document.getElementById("inputInitStateRange");


// #### JAVASCRIPT QUANTUM WALK OBJECTS ####
let defaultN = 100;
let defaultT = 10;
let defaultInitState = [Math.floor(defaultN / 2), Math.floor(defaultN / 2) + 1];
let defaultGraph = 'nx.cycle_graph';
let defaultTimeList = [0, 100];
let defaultInitStateList = [[Math.floor(defaultN / 2), Math.floor(defaultN / 2) + 1]];

let staticQuantumWalk = new StaticQuantumwalk(defaultN, defaultT, defaultInitState, defaultGraph);
let dynamicQuantumWalk = new DynamicQuantumwalk(defaultGraph, defaultTimeList, defaultInitStateList);

let inputInit = () => {
    inputTime.value = defaultT;
    inputDim.value = defaultN;
    inputGraph.value = defaultGraph;
    inputInitState.value = defaultInitState
}

let inputRangeInit = () => {
    inputTimeRange.value = defaultTimeList;
    inputInitStateRange.value = defaultInitStateList;
}

inputInit();
inputRangeInit();


// #### CHARTS FOR DISTRIBUTIONS ####
let staticCtx = document.getElementById("staticProbDistChart").getContext("2d");
let dynamicCtx = document.getElementById("dynamicProbDistChart").getContext("2d");

cy.layout({ name: "circle" }).run();

let myChart = new Chart(staticCtx, data);
let myAnimatedChart = new Chart(dynamicCtx, data2);


// #### BUTTONS ####
document.getElementById("setInitStateRangeButton").addEventListener('click', async function () {
    setInitStateRange();
});

document.getElementById("setTimeRangeButton").addEventListener('click', async function () {
    setTimeRange();
});

document.getElementById("setInitStateButton").addEventListener('click', async function () {
    setInitState();
});

document.getElementById("setTimeButton").addEventListener('click', async function () {
    setTime();
});

document.getElementById("setDimButton").addEventListener('click', async function () {
    setDimButton();
});

document.getElementById("setGraphButton").addEventListener('click', async function () {
    setGraph();
});

document.getElementById("dynamicProbDistButton").addEventListener('click', async function () {
    setdynamicProbDist();
});

document.getElementById("runGraphButton").addEventListener('click', async function () {
    setRunGraph();
});

document.getElementById("staticProbDistButton").addEventListener('click', async function () {
    setStaticProbDist();
});

document.getElementById("survProbNodesButton").addEventListener('click', async function () {
    setStaticSurvivalProb();
});

document.getElementById("PSTNodesButton").addEventListener('click', async function () {
    setPST();
});


// #### BUTTON FUNCTIONS ####
let setInitStateRange = async () => {
    dynamicQuantumWalk.initStateList = inputInitStateRange.value;
    eel.setInitStateList(dynamicQuantumWalk.initStateList);
}

let setTimeRange = async () => {
    dynamicQuantumWalk.timeList = inputTimeRange.value;
    eel.setTimeList(dynamicQuantumWalk.timeList);
}

let setInitState = async () => {
    staticQuantumWalk.initState = inputInitState.value;
    eel.setInitState(staticQuantumWalk.initState);
}

let setTime = async () => {
    staticQuantumWalk.time = parseFloat(inputTime.value);
    eel.setTime(staticQuantumWalk.time);
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

let setRunGraph = async () => {
    let myGraph = await getGraph();
    updateGraph(myGraph);
    setGraph();
    setDimButton();
}

let setStaticProbDist = async () => {
    let walk = await getWalk();
    let distList = walk.flat();
    data.data.datasets[0].data = distList;
    data.data.labels = [...Array(distList.length).keys()];
    myChart.destroy();
    myChart = new Chart(staticCtx, data);
    await setStaticMean();
    await setStaticSndMoment();
    await setStaticStDev();
    await setInversePartRatio();
}

let setdynamicProbDist = async () => {
    let multipleWalks = await getMultipleWalks();
    let i = 0;
    myAnimatedChart.clear();
    // data2.options.scales.y.ticks.min = 0.9
    // data2.options.scales.y.ticks.max = 1
    // data2.options.scales.y.ticks.stepSize = 0.001
    for (const walk of multipleWalks) {
        setTimeout(() => {
            data2.data.datasets[0].data = walk.flat();
            data2.data.labels = [...Array(walk.length).keys()];
            data2.options.scales.y.ticks.beginAtZero = false;
            myAnimatedChart.update();
        }, 80 * i);
        i++;
    }
}

let setStaticMean = async () => {
    let statMean = await getStaticMean();
    inputMean.value = statMean;
}

let setStaticSndMoment = async () => {
    let statSndMom = await getStaticSndMoment();
    inputSndMoment.value = statSndMom;
}

let setStaticStDev = async () => {
    let statStDev = await getStaticStDev();
    inputStDev.value = statStDev;
}

let setStaticSurvivalProb = async () => {
    let fromNode = inputSurvProbNodeA.value;
    let toNode = inputSurvProbNodeB.value;
    let survProb = await getStaticSurvivalProb(fromNode, toNode);
    inputSurvProbResult.value = survProb;
}

let setInversePartRatio = async () => {
    let invPartRatio = await getInversePartRatio();
    inputInvPartRat.value = invPartRatio;
}

let setPST = async () => {
    let fromNode = inputPSTNodeA.value;
    let toNode = inputPSTNodeB.value;
    let PST = await getPST(fromNode, toNode);
    inputPSTResult.value = PST;
}

let getWalk = () => {
    return eel
        .runWalk()()
        .then((a) => {
            return a ? a : Promise.reject(Error("Get Walk failed."));
        })
        .catch((e) => console.log(e));
};

let getMultipleWalks = () => {
    return eel
        .runMultipleWalks()()
        .then((a) => {
            return a ? a : Promise.reject(Error("Get Multiple Walks failed."));
        })
        .catch((e) => console.log(e));
};

let getGraph = () => {
    return eel
        .graphToJson()()
        .then((a) => {
            return a ? a : Promise.reject(Error("Get Graph failed."));
        })
        .catch((e) => console.log(e));
};

let getTime = () => {
    return eel
        .getTime()()
        .then((a) => {
            return a ? a : Promise.reject(Error("Get Time failed."));
        })
        .catch((e) => console.log(e));
}

let getStaticMean = () =>{
        return eel
        .getStaticMean()()
        .then((a) => {
            return a ? a : Promise.reject(Error("Get Static Mean failed."));
        })
        .catch((e) => console.log(e));
}

let getStaticSndMoment = () =>{
        return eel
        .getStaticSndMoment()()
        .then((a) => {
            return a ? a : Promise.reject(Error("Get Static Snd Moment failed."));
        })
        .catch((e) => console.log(e));
}

let getStaticStDev = () =>{
        return eel
        .getStaticStDev()()
        .then((a) => {
            if (isNaN(a)){
                Promise.reject(Error("Get Static Standard Deviation faile: StDev is NaN."));
            }else{
                return a;
            }
        })
        .catch((e) => console.log(e));
}

let getStaticSurvivalProb = (fromNode,toNode) =>{
        return eel
        .getStaticSurvivalProb(fromNode,toNode)()
        .then((a) => {
            if (isNaN(a)){
                Promise.reject(Error("Get Survival Probability failed: SP is NaN."));
            }else{
                return a;
            }
        })
        .catch((e) => console.log(e));
}

// #### ASYNC FUNCTIONS TO GET VALUES FROM PYTHON ####
let getInversePartRatio = () =>{
        return eel
        .getInversePartRatio()()
        .then((a) => {
            if (isNaN(a)){
                    Promise.reject(Error("Get Inv. Part. Ratio failed: IPR is NaN."));
                }else{
                    return a;
                }        })
        .catch((e) => console.log(e));
}

let getPST = (nodeA,nodeB) =>{
        return eel
        .checkPST(nodeA,nodeB)()
        .then((a) => {
            if (isNaN(parseFloat(a))){
                    Promise.reject(Error("Get Inv. Part. Ratio failed: IPR is NaN."));
                }else if(parseFloat(a)<0){
                    return "No PST.";
                }else{
                    return a;
            }
        })
        .catch((e) => console.log(e));
}


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