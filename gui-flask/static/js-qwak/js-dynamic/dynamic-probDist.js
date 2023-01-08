import {
    staticChartData,
    dynamicChartData,
} from "../dynamic-tools.js";

let myAnimatedChart = new Chart(document.getElementById("dynamicProbDistChart").getContext("2d"), dynamicChartData);

export function plotDynamicProbDist(multipleWalks) {
    // console.log(walk)
    if (multipleWalks.hasError == true) {
        alert(multipleWalks.probDist);
        return;
    } else {
        let i = 0;
        let animationSteps = 100;
        myAnimatedChart.clear();
        for (const walk of multipleWalks.probDist) {
            setTimeout(() => {
                dynamicChartData.data.datasets[0].data = walk.flat();
                dynamicChartData.data.labels = [...Array(walk.length).keys()];
                dynamicChartData.options.scales.y.ticks.beginAtZero = false;
                myAnimatedChart.update();
            }, animationSteps * i);
            i++;
        }
    }
}

export async function setDynamicProbDistDB(newDim,newGraph,newTimeList,newInitCond) {
    await $.ajax({
        type: 'POST',
        url: `/setRunMultipleWalksDB`,
        data: {newDim:newDim,newGraph: newGraph, newTimeList:newTimeList,newInitCond:newInitCond},
        success: function () {
            console.log(`success - Runwalk`);
        },
        error: function (response) {
            console.log('Runwalk error');
        }
    });
}

export async function getDynamicProbDistDB(newDim,newGraph,newTimeList,newInitCond) {
    let myWalk;
    await $.ajax({
        type: 'POST',
        url: `/getRunMultipleWalksDB`,
        data: {newDim:newDim,newGraph: newGraph, newTimeList:newTimeList,newInitCond:newInitCond},
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
