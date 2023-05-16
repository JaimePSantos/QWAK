export let dynamicChartData = {
    type: "line",
    data: {
        labels: [...Array(100).keys()],
        datasets: [
            {
                label: "Probability",
                data: [],
                fill: false,
                borderColor: "rgb(14,84,246)",
                pointRadius: 0,
            },
        ],
    },
    options: {
        scales: {
            x: {
                grid: {
                    display: false
                }
            },
            y:{
                suggestedMax:0.1,
                suggestedMin:0,
            },
        },
        maintainAspectRatio: false,
    },
};

function openTab(evt, graph, tabcontent, tablinks) {
    // Declare all variables
    var i, tabcontent, tablinks;

    // Get all elements with class="tabcontent" and hide them
    tabcontent = document.getElementsByClassName(tabcontent);
    for (i = 0; i < tabcontent.length; i++) {
        tabcontent[i].style.display = "none";
    }

    // Get all elements with class="tablinks" and remove the class "active"
    tablinks = document.getElementsByClassName(tablinks);
    for (i = 0; i < tablinks.length; i++) {
        tablinks[i].className = tablinks[i].className.replace(" active", "");
    }

    // Show the current tab, and add an "active" class to the button that opened the tab
    document.getElementById(graph).style.display = "block";
    evt.currentTarget.className += " active";
}

export let dynamicMeanChartData = {
    type: "line",
    data: {
        labels: [...Array(100).keys()],
        datasets: [
            {
                label: "Node",
                data: [],
                fill: false,
                borderColor: "rgb(246,14,14)",
                pointRadius: 0,
            },
        ],
    },
    options: {
        scales: {
            x: {
                grid: {
                    display: false
                }
            },
        },
        maintainAspectRatio: false,
    },
};

export let dynamicStDevChartData = {
    type: "line",
    data: {
        labels: [...Array(100).keys()],
        datasets: [
            {
                label: "Node",
                data: [],
                fill: false,
                borderColor: "rgb(246,14,14)",
                pointRadius: 0,
            },
        ],
    },
    options: {
        scales: {
            x: {
                grid: {
                    display: false
                }
            },
        },
        maintainAspectRatio: false,
    },
};

export let dynamicInvPartRatioChartData = {
    type: "line",
    data: {
        labels: [...Array(100).keys()],
        datasets: [
            {
                label: "Node",
                data: [],
                fill: false,
                borderColor: "rgb(246,14,14)",
                pointRadius: 0,
            },
        ],
    },
    options: {
        scales: {
            x: {
                grid: {
                    display: false
                }
            },
        },
        maintainAspectRatio: false,
    },
};

export let dynamicSurvivalProbChartData = {
    type: "line",
    data: {
        labels: [...Array(100).keys()],
        datasets: [
            {
                label: "Node",
                data: [],
                fill: false,
                borderColor: "rgb(246,14,14)",
                pointRadius: 0,
            },
        ],
    },
    options: {
        scales: {
            x: {
                grid: {
                    display: false
                }
            },
        },
        maintainAspectRatio: false,
    },
};

document.getElementById('defaultDynStat').addEventListener('click', evt => {
    openTab(evt, 'Mean', "stattabcontent", "stattablinks");
});

document.getElementById('stDevDynStat').addEventListener('click', evt => {
    openTab(evt, 'StDev', "stattabcontent", "stattablinks");
});

document.getElementById('invPartRatioDynStat').addEventListener('click', evt => {
    openTab(evt, 'InvPartRatio', "stattabcontent", "stattablinks");
});

document.getElementById('survProbDynStat').addEventListener('click', evt => {
    openTab(evt, 'SurvivalProb', "stattabcontent", "stattablinks");
});

document.getElementById('invPartRatioDynStat').click()

document.getElementById('invPartRatioDynStat').click()

document.getElementById('stDevDynStat').click()

document.getElementById('defaultDynStat').click()