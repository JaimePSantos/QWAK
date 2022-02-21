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

let setTimeRangeButton = document.getElementById("setTimeRangeButton");
let setGammaRangeButton = document.getElementById("setGammaRangeButton");
let setInitStateRangeButton = document.getElementById("setInitStateRangeButton");

let inputTimeRange = document.getElementById("inputTimeRange");
let inputGammaRange = document.getElementById("inputGammaRange");
let inputInitStateRange = document.getElementById("inputInitStateRange");

let defaultN = 100;
let defaultT = 30;
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

inputInit()
inputRangeInit()

let ctx = document.getElementById("myChart").getContext("2d");
let ctx2 = document.getElementById("myAnimatedChart").getContext("2d");

cy.layout({ name: "circle" }).run();

let myChart = new Chart(ctx, data);
let myAnimatedChart = new Chart(ctx2, data2);



let setInitStateRangeButtonPress = setInitStateRangeButton.onclick = async () => {
    dynamicQuantumWalk.initStateList = inputInitStateRange.value;
    eel.setInitStateList(dynamicQuantumWalk.initStateList);
}


let setTimeRangeButtonPress = setTimeRangeButton.onclick = async () => {
    dynamicQuantumWalk.timeList = inputTimeRange.value;
    eel.setTimeList(dynamicQuantumWalk.timeList)
}

let setInitStateButtonPress = setInitStateButton.onclick = async () => {
    staticQuantumWalk.initState = inputInitState.value;
    eel.setInitState(staticQuantumWalk.initState)
}

let setTimeButtonPress = setTimeButton.onclick = async () => {
    staticQuantumWalk.time = parseFloat(inputTime.value);
    eel.setTime(staticQuantumWalk.time);
}

let setDimButtonPress = setDimButton.onclick = async () => {
    staticQuantumWalk.dim = parseInt(inputDim.value);
    staticQuantumWalk.graph = inputGraph.value;
    eel.setDim(staticQuantumWalk.dim, staticQuantumWalk.graph);
}

let setGraphButtonPress = setGraphButton.onclick = async () => {
    staticQuantumWalk.graph = inputGraph.value;
    eel.setGraph(staticQuantumWalk.graph);
}

let goMultipleButtonPress = goMultipleButton.onclick = async () => {
    let multipleWalks = await getMultipleWalks();
    let i = 0;
    myAnimatedChart.clear();
    for (const walk of multipleWalks) {
        setTimeout(() => {
            data2.data.datasets[0].data = walk.flat();
            data2.data.labels = [...Array(walk.length).keys()];
            myAnimatedChart.update();
            // console.log(walk)
        }, 80 * i);
        i++;
    }
};

let graphButtonPress = graphButton.onclick = async () => {
    let myGraph = await getGraph();
    updateGraph(myGraph)
};

let goButtonPress = goButton.onclick = async () => {
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

};

let survProbNodesButtonPress = survProbNodesButton.onclick = async () => {
    setStaticSurvivalProb();
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
            return a ? a : Promise.reject(Error("Get Inverse Participation Ratio failed."));
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
    customCy.add({ group: 'nodes', data: { id: nodeNumber.toString(),name: nodeNumber.toString() },  position: { x: nodeXPos, y: nodeYPos }});
    // customCy.layout();
}
document.getElementById('graphCustomButton').addEventListener('click', function () {
    graphCustomButtonPress();
});

let graphCustomButtonPress = async () => {
    let adjacencyMatrix = createAdjacencyMatrix(customCy);
    console.log(adjacencyMatrix.toArray())
    eel.printAdjacencyMatrix()
}

eel.expose(sendAdjacencyMatrix);
function sendAdjacencyMatrix(){
    return createAdjacencyMatrix(customCy);
}

function createAdjacencyMatrix(graph) {
    let adjacencyMatrix = math.zeros(graph.json().elements.nodes.length, graph.json().elements.nodes.length)

    for(let edg of graph.json().elements.edges){
        console.log(`Source: ${edg.data.source} -> Target: ${edg.data.target}`)
        adjacencyMatrix.subset(math.index(parseInt(edg.data.source),parseInt(edg.data.target)),1)
        adjacencyMatrix.subset(math.index(parseInt(edg.data.target),parseInt(edg.data.source)),1)
    }
    return adjacencyMatrix

}

document.getElementById('clearGraphButton').addEventListener('click', function () {
    eh.disableDrawMode();
});

// document.querySelector('#start').addEventListener('click', function () {
//     eh.start(customCy.$('node:selected'));
// });

// var popperEnabled = false;
//
// document.querySelector('#popper').addEventListener('click', function () {
//     if (popperEnabled) { return; }
//
//     popperEnabled = true;
//
//     // example code for making your own handles -- customise events and presentation where fitting
//     // var popper;
//     var popperNode;
//     var popper;
//     var popperDiv;
//     var started = false;
//
//     function start() {
//         eh.start(popperNode);
//     }
//
//     function stop() {
//         eh.stop();
//     }
//
//     function setHandleOn(node) {
//         if (started) { return; }
//
//         removeHandle(); // rm old handle
//
//         popperNode = node;
//
//         popperDiv = document.createElement('div');
//         popperDiv.classList.add('popper-handle');
//         popperDiv.addEventListener('mousedown', start);
//         document.body.appendChild(popperDiv);
//
//         popper = node.popper({
//             content: popperDiv,
//             popper: {
//                 placement: 'top',
//                 modifiers: [
//                     {
//                         name: 'offset',
//                         options: {
//                             offset: [0, -10],
//                         },
//                     },
//                 ]
//             }
//         });
//     }
//
//     function removeHandle() {
//         if (popper) {
//             popper.destroy();
//             popper = null;
//         }
//
//         if (popperDiv) {
//             document.body.removeChild(popperDiv);
//             popperDiv = null;
//         }
//
//         popperNode = null;
//     }
//
//     customCy.on('mouseover', 'node', function (e) {
//         setHandleOn(e.target);
//     });
//
//     customCy.on('grab', 'node', function () {
//         removeHandle();
//     });
//
//     customCy.on('tap', function (e) {
//         if (e.target === customCy) {
//             removeHandle();
//         }
//     });
//
//     customCy.on('zoom pan', function () {
//         removeHandle();
//     });
//
//     window.addEventListener('mouseup', function (e) {
//         stop();
//     });
//
//     customCy.on('ehstart', function () {
//         started = true;
//     });
//
//     customCy.on('ehstop', function () {
//         started = false;
//     });
// });
