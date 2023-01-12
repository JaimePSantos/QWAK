import {staticChartData} from "./static-tools.js";

let inputTime = document.getElementById("inputTime");
let inputInitState = document.getElementById("inputInitState");

let myChart = new Chart(document.getElementById("staticProbDistChart").getContext("2d"), staticChartData);

export function plotStaticProbDistDB(walk) {
        let distList = walk.probDist.flat();
        staticChartData.data.datasets[0].data = distList;
        staticChartData.data.labels = [...Array(distList.length).keys()];
        myChart.destroy();
        myChart = new Chart(document.getElementById("staticProbDistChart").getContext("2d"), staticChartData);
}

export async function setStaticProbDistDB(newDim,newGraph,newTime,newInitCond) {
    await $.ajax({
        type: 'POST',
        url: `/setRunWalkDB`,
        data: {newDim:newDim,newGraph: newGraph, newTime:newTime,newInitCond:newInitCond},
        success: function () {
            console.log(`success - Runwalk`);
        },
        error: function (response) {
            console.log('Runwalk error');
        }
    });
}

export async function getStaticProbDistDB(newDim,newGraph,newTime,newInitCond) {
    let myWalk, walkId;
    await $.ajax({
        type: 'POST',
        url: `/getRunWalkDB`,
        data: {newDim:newDim,newGraph: newGraph, newTime:newTime,newInitCond:newInitCond},
        success: function (response) {
            console.log(`success - Runwalk ${response}`);
            myWalk = response;
        },
        error: function (response) {
            console.log('Runwalk error');
            myWalk = response;
        }
    });
    return myWalk;
}

export async function getStaticSurvivalProb(fromNode,toNode) {
    let survProb;
    await $.ajax({
        type: 'POST',
        url: `/getStaticSurvivalProb`,
        data:{fromNode:fromNode,toNode:toNode},
        success: function (response) {
            console.log(`success - Runwalk ${response}`);
            survProb = response;
        },
        error: function (response) {
            console.log('Runwalk error');
            survProb = response;
        }
    });
    return survProb;
}


export async function deleteWalkEntry(walkName) {
    await $.ajax({
        type: 'POST',
        url: `/deleteWalkEntry`,
        data:{walkName:walkName},
        success: function () {
            console.log(`success - Runwalk`);
        },
        error: function (response) {
            console.log('Runwalk error');
        }
    });
}

export async function deleteAllWalkEntries() {
    await $.ajax({
        type: 'POST',
        url: `/deleteAllWalkEntries`,
        success: function () {
            console.log(`success - Runwalk`);
        },
        error: function (response) {
            console.log('Runwalk error');
        }
    });
}

export async function setStaticPyInitState(initStateStr) {
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

export async function setStaticPyTime(newTime) {
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