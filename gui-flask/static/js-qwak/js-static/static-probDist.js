import {staticChartData} from "../static-tools.js";

let inputTime = document.getElementById("inputTime");
let inputInitState = document.getElementById("inputInitState");

let myChart = new Chart(document.getElementById("staticProbDistChart").getContext("2d"), staticChartData);

export function plotStaticProbDistDB(walk) {
    // console.log(walk)
    if (walk.hasError == true) {
        alert(walk.probDist);
        return;
    } else {
        let distList = walk.probDist.flat();
        staticChartData.data.datasets[0].data = distList;
        staticChartData.data.labels = [...Array(distList.length).keys()];
        myChart.destroy();
        myChart = new Chart(document.getElementById("staticProbDistChart").getContext("2d"), staticChartData);
    }
}

export async function setStaticProbDistDB(walkName) {
    await $.ajax({
        type: 'POST',
        url: `/setRunWalkDB`,
        data:{walkName:walkName},
        success: function () {
            console.log(`success - Runwalk`);
        },
        error: function (response) {
            console.log('Runwalk error');
        }
    });
}

export async function getStaticProbDistDB(walkName) {
    let myWalk, walkId;
    await $.ajax({
        type: 'POST',
        url: `/getRunWalkDB`,
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