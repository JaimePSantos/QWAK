import { defaultDist, cy, data, data2, customCy } from "./tools.js";
import { StaticQuantumwalk } from "./staticQuantumwalk.js";
import { DynamicQuantumwalk } from "./dynamicQuantumwalk.js";


let goButton = document.getElementById("goButton");
let goMultipleButton = document.getElementById("goMultipleButton");
let graphButton = document.getElementById("graphButton");

let setTimeButton = document.getElementById("setTimeButton");
let setGammaButton = document.getElementById("setGammaButton");
let setDimButton = document.getElementById("setDimButton");
let setGraphButton = document.getElementById("setGraphButton");
let setInitStateButton = document.getElementById("setInitStateButton");

let inputTime = document.getElementById("inputTime");
let inputGamma = document.getElementById("inputGamma");
let inputDim = document.getElementById("inputDim");
let inputGraph = document.getElementById("inputGraph");
let inputInitState = document.getElementById("inputInitState");

let inputMean = document.getElementById("inputMean");
let inputSndMoment = document.getElementById("inputSndMoment");
let inputStDev = document.getElementById("inputStDev");
let inputSurvProbResult = document.getElementById("inputSurvProbResult");
let inputSurvProbNodeA = document.getElementById("inputSurvProbNodeA");
let inputSurvProbNodeB = document.getElementById("inputSurvProbNodeB");
let survProbNodesButton = document.getElementById("survProbNodesButton");
let inputInvPartRat = document.getElementById("inputInvPartRat");
let inputPSTNodeA = document.getElementById("inputPSTNodeA");
let inputPSTNodeB = document.getElementById("inputPSTNodeB");
let PSTNodesButton = document.getElementById("PSTNodesButton");
let inputPSTResult = document.getElementById("inputPSTResult");

let setTimeRangeButton = document.getElementById("setTimeRangeButton");
let setGammaRangeButton = document.getElementById("setGammaRangeButton");
let setInitStateRangeButton = document.getElementById("setInitStateRangeButton");

let inputTimeRange = document.getElementById("inputTimeRange");
let inputGammaRange = document.getElementById("inputGammaRange");
let inputInitStateRange = document.getElementById("inputInitStateRange");

let defaultN = 100;
let defaultT = 10;
let defaultInitState = [Math.floor(defaultN / 2), Math.floor(defaultN / 2) + 1];
let defaultGraph = 'nx.cycle_graph';
let defaultTimeList = [0, 100];
let defaultInitStateList = [[Math.floor(defaultN / 2), Math.floor(defaultN / 2) + 1]];
let staticQuantumWalk = new StaticQuantumwalk(defaultN, defaultT, defaultInitState, defaultGraph)
let dynamicQuantumWalk = new DynamicQuantumwalk(defaultGraph, defaultTimeList, defaultInitStateList)

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

let ctx = document.getElementById("myChart").getContext("2d");
let ctx2 = document.getElementById("myAnimatedChart").getContext("2d");

cy.layout({ name: "circle" }).run();

let myChart = new Chart(ctx, data);
let myAnimatedChart = new Chart(ctx2, data2);


setInitStateRangeButton.addEventListener('click', async function () {
    dynamicQuantumWalk.initStateList = inputInitStateRange.value;
    eel.setInitStateList(dynamicQuantumWalk.initStateList);
});

setTimeRangeButton.addEventListener('click', async function () {
    dynamicQuantumWalk.timeList = inputTimeRange.value;
    eel.setTimeList(dynamicQuantumWalk.timeList);
});

setInitStateButton.addEventListener('click', async function () {
    staticQuantumWalk.initState = inputInitState.value;
    eel.setInitState(staticQuantumWalk.initState);
});

setTimeButton.addEventListener('click', async function () {
    staticQuantumWalk.time = parseFloat(inputTime.value);
    eel.setTime(staticQuantumWalk.time);
});

setDimButton.addEventListener('click', async function () {
    staticQuantumWalk.dim = parseInt(inputDim.value);
    staticQuantumWalk.graph = inputGraph.value;
    eel.setDim(staticQuantumWalk.dim, staticQuantumWalk.graph);
});


setGraphButton.addEventListener('click', async function () {
    staticQuantumWalk.graph = inputGraph.value;
    eel.setGraph(staticQuantumWalk.graph);
});

goMultipleButton.addEventListener('click', async function () {
    let multipleWalks = await getMultipleWalks();
    let i = 0;
    myAnimatedChart.clear();
    data2.options.scales.y.ticks.min = 0.9
    data2.options.scales.y.ticks.max = 1
    data2.options.scales.y.ticks.stepSize = 0.001
    for (const walk of multipleWalks) {
        setTimeout(() => {
            data2.data.datasets[0].data = walk.flat();
            data2.data.labels = [...Array(walk.length).keys()];
            data2.options.scales.y.ticks.beginAtZero = false;
            myAnimatedChart.update();
        }, 80 * i);
        i++;
    }
});

graphButton.addEventListener('click', async function () {
    let myGraph = await getGraph();
    updateGraph(myGraph);
    setGraphButtonPress();
    setDimButtonPress();
});

goButton.addEventListener('click', async function () {
    let walk = await getWalk();
    let distList = walk.flat();
    data.data.datasets[0].data = distList;
    data.data.labels = [...Array(distList.length).keys()];
    myChart.destroy();
    myChart = new Chart(ctx, data);
    await setStaticMean();
    await setStaticSndMoment();
    await setStaticStDev();
    await setInversePartRatio();
});

survProbNodesButton.addEventListener('click', async function () {
    setStaticSurvivalProb();
});

PSTNodesButton.addEventListener('click', async function () {
    setPST();
});

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