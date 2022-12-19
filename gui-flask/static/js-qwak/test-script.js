
let inputDim = document.getElementById("inputDim");
let inputGraph = document.getElementById("inputGraph");
let inputTime = document.getElementById("inputTime");
let inputInitState = document.getElementById("inputInitState");

let defaultN = 5;
let defaultT = 1;
let defaultInitState = [Math.floor(defaultN / 2)];
let defaultGraph = 'nx.cycle_graph';

let inputInit = () => {
    inputTime.value = defaultT;
    inputInitState.value = defaultInitState
    inputDim.value = defaultN;
    inputGraph.value = defaultGraph;
}

inputInit();


$(function () {
    $('#testRunWalkBut').on('click', async function (e) {
        e.preventDefault();
        // await setStaticDim(inputDim.value, inputGraph.value);
        // await setStaticGraph(inputGraph.value);
        // await setStaticJsTime();
        // await setStaticJsInitState();
        // // let myGraph = await getStaticGraph();
        await setStaticProbDistDBTest(inputDim.value,inputGraph.value,inputTime.value,inputInitState.value);
    });
});

$(function () {
    $('#testGetRunWalkBut').on('click', async function (e) {
        e.preventDefault();
        await getStaticProbDistDBTest();
    });
});

$(function () {
    $('#resetBut').on('click', async function (e) {
        e.preventDefault();
        await reset();
    });
});

$(function () {
    $('#loadBut').on('click', async function (e) {
        e.preventDefault();
        await load();
    });
});

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

async function setStaticJsInitState(){
    await setStaticPyInitState(inputInitState.value);
}

export async function setStaticJsTime(){
    await setStaticPyTime(inputTime.value);
}

async function setStaticPyInitState(initStateStr) {
    $.ajax({
        type: 'POST',
        url: `/setStaticInitState`, // <- Add the queryparameter here
        data: {initStateStr: initStateStr},
        success: function (response) {
            console.log('success - InitState set to ${initStateStr}');
        },
        error: function (response) {
            console.log('InitState error');
        }
    });
}

async function setStaticPyTime(newTime) {
    $.ajax({
        type: 'POST',
        url: `/setStaticTime`, // <- Add the queryparameter here
        data: {newTime: newTime},
        success: function (response) {
            console.log('success - Time set to ${newTime}');
        },
        error: function (response) {
            console.log('setTime error');
        }
    });
}

async function getStaticGraph() {
    let myGraph;
    await $.ajax({
        type: 'POST',
        url: `/getStaticGraphToJson`, // <- Add the queryparameter here
        success: function (response) {
            myGraph = response;
            console.log('success - got graph ${myGraph}');
            return myGraph;
        },
        error: function (response) {
            console.log('getStaticGraph error');
            myGraph = 'error'
            return myGraph;
        }
    });
    return myGraph;
}

async function setStaticGraph(newGraph) {
    $.ajax({
        type: 'POST',
        url: `/setStaticGraph`,
        data: {newGraph: newGraph},
        success: function (response) {
            console.log('success - graph set to ${newGraph}');
        },
        error: function (response) {
            console.log('setGraph error');
        }
    })
}

async function setStaticDim(newDim, graphStr) {
    $.ajax({
        type: 'POST',
        url: `/setStaticDim`, // <- Add the queryparameter here
        data: {newDim: newDim, graphStr: graphStr},
        success: function (response) {
            console.log('success - Dim set to ${newDim}');
        },
        error: function (response) {
            console.log('setDim error');
        }
    });
}



async function setStaticProbDistDBTest(newDim,newGraph,newTime,newInitCond) {
    await $.ajax({
        type: 'POST',
        data: {newDim:newDim,newGraph: newGraph, newTime:newTime,newInitCond:newInitCond},
        url: `/setRunWalkDBTest`,
        success: function () {
            console.log(`success - Runwalk`);
        },
        error: function (response) {
            console.log('Runwalk error');
        }
    });
}

async function getStaticProbDistDBTest() {
    await $.ajax({
        type: 'POST',
        url: `/getRunWalkDBTest`,
        success: function () {
            console.log(`success - Runwalk`);
        },
        error: function (response) {
            console.log('Runwalk error');
        }
    });
}

async function reset() {
    await $.ajax({
        type: 'POST',
        url: `/reset`,
        success: function () {
            console.log(`success - reset`);
        },
        error: function (response) {
            console.log('Runwalk error');
        }
    });
}

async function load() {
    await $.ajax({
        type: 'POST',
        url: `/load`,
        success: function () {
            console.log(`success - Walk loaded`);
        },
        error: function (response) {
            console.log('Runwalk error');
        }
    });
}