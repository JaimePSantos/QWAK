
let inputDim = document.getElementById("inputDim");
let inputGraph = document.getElementById("inputGraph");
let inputTime = document.getElementById("inputTime");
let inputInitState = document.getElementById("inputInitState");

let inputDimDyn = document.getElementById("inputDimDyn");
let inputGraphDyn = document.getElementById("inputGraphDyn");
let inputTimeDyn = document.getElementById("inputTimeDyn");
let inputInitStateDyn = document.getElementById("inputInitStateDyn");


let defaultN = 5;
let defaultT = 1;
let defaultInitState = [Math.floor(defaultN / 2)];
let defaultGraph = 'nx.cycle_graph';

let inputInit = () => {
    inputTime.value = defaultT;
    inputInitState.value = defaultInitState
    inputDim.value = defaultN;
    inputGraph.value = defaultGraph;

    inputTimeDyn.value = [defaultT-1,defaultT];
    inputInitStateDyn.value = [defaultInitState]
    inputDimDyn.value = defaultN;
    inputGraphDyn.value = defaultGraph;
}

inputInit();


$(function () {
    $('#testRunWalkBut').on('click', async function (e) {
        e.preventDefault();
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