export let defaultDist = [
    (-34, 3.3333333333333335e-5),
    (-32, 6.666666666666667e-5),
    (-30, 0.00023333333333333333),
    (-28, 0.0004),
    (-26, 0.0010666666666666667),
    (-24, 0.0014333333333333333),
    (-22, 0.0038666666666666667),
    (-20, 0.006466666666666667),
    (-18, 0.009133333333333334),
    (-16, 0.01633333333333333),
    (-14, 0.024266666666666666),
    (-12, 0.0346),
    (-10, 0.046033333333333336),
    (-8, 0.05996666666666667),
    (-6, 0.0732),
    (-4, 0.08396666666666666),
    (-2, 0.08983333333333333),
    (0, 0.09083333333333334),
    (2, 0.0911),
    (4, 0.08453333333333334),
    (6, 0.07216666666666667),
    (8, 0.06343333333333333),
    (10, 0.0476),
    (12, 0.03496666666666667),
    (14, 0.025466666666666665),
    (16, 0.0159),
    (18, 0.010466666666666668),
    (20, 0.0064),
    (22, 0.003),
    (24, 0.0016333333333333334),
    (26, 0.0008666666666666666),
    (28, 0.0005333333333333334),
    (30, 0.00016666666666666666),
    (32, 3.3333333333333335e-5),
];

let initGraph = async () => {
    let graphStr = 'nx.cycle_graph'
    await setDynamicGraph(5,graphStr)
}

async function setDynamicDim(newDim, graphStr) {
    await $.ajax({
        type: 'POST',
        url: `/setDynamicDim`, // <- Add the queryparameter here
        data: {newDim: newDim, graphStr: graphStr},
        success: function (response) {
            console.log('success - Dim set to ${newDim}');
        },
        error: function (response) {
            console.log('setDim error');
        }
    });
}

async function setDynamicGraph(newDim,newGraph) {
    await $.ajax({
        type: 'POST',
        url: `/setDynamicGraph`,
        data: {newDim:newDim,newGraph: newGraph},
        success: function (response) {
            console.log('success - graph set to ${newGraph}');
        },
        error: function (response) {
            console.log('setGraph error');
        }
    })
}

async function getDynamicGraph() {
    let myGraph;
    await $.ajax({
        type: 'POST',
        url: `/getDynamicGraphToJson`, // <- Add the queryparameter here
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

initGraph();
let myGraph = await getDynamicGraph();

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


document.getElementById('defaultOpen').addEventListener('click', evt => {
    openTab(evt, 'GraphGenerator', "tabcontent", "tablinks");
})

document.getElementById('defaultOpen').click()

document.getElementById('customGraphDisplay').addEventListener('click', evt => {
    openTab(evt, 'CustomGraph', "tabcontent", "tablinks");

})


export let cy = cytoscape({
    container: document.getElementById("cy"), // container to render in
    boxSelectionEnabled: false,
    autounselectify: true,
    elements: myGraph.elements,
    directed: myGraph.directed,
    multigraph: myGraph.multigraph,
    wheelSensitivity: 0.1,
    layout: {
        name: 'circle',
    },
    style: [
        // the stylesheet for the graph
        {
            selector: "node",
            style: {
                "background-color": "#666",
                label: "data(id)",
            },
        },

        {
            selector: "edge",
            style: {
                width: 3,
                "line-color": "red",
                "curve-style": "bezier",
            },
        },
    ],
});

document.getElementById('customGraphDisplay').click()

export let customCy = cytoscape({
    container: document.getElementById('cyCustom'),
    directed: false,
    wheelSensitivity: 0.1,
    layout: {
        name: 'concentric',
        concentric: function (n) {
            return n.id() === '0' ? 200 : 0;
        },
        levelWidth: function (nodes) {
            return 100;
        },
        minNodeSpacing: 100
    },

    style: [
        {
            selector: 'node[name]',
            style: {
                'content': 'data(name)'
            }
        },

        {
            selector: 'edge',
            style: {
                'curve-style': 'bezier'
            }
        },

        // some style for the extension

        {
            selector: '.eh-handle',
            style: {
                'background-color': 'red',
                'width': 12,
                'height': 12,
                'shape': 'ellipse',
                'overlay-opacity': 0,
                'border-width': 12, // makes the handle easier to hit
                'border-opacity': 0
            }
        },

        {
            selector: '.eh-hover',
            style: {
                'background-color': 'red'
            }
        },

        {
            selector: '.eh-source',
            style: {
                'border-width': 2,
                'border-color': 'red'
            }
        },

        {
            selector: '.eh-target',
            style: {
                'border-width': 2,
                'border-color': 'red'
            }
        },

        {
            selector: '.eh-preview, .eh-ghost-edge',
            style: {
                'background-color': 'red',
                'line-color': 'red',
                'target-arrow-color': 'red',
                'source-arrow-color': 'red'
            }
        },

        {
            selector: '.eh-ghost-edge.eh-preview-active',
            style: {
                'opacity': 0
            }
        }
    ],

    elements: {
        nodes: [
            {data: {id: '0', name: '0'}},
            {data: {id: '1', name: '1'}},
            {data: {id: '2', name: '2'}}
        ],
        edges: [
            {data: {source: '0', target: '1'}},
            {data: {source: '1', target: '2'}}
        ]
    }
});

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
    },
};

export let dynamicMeanChartData = {
    type: "line",
    data: {
        labels: [...Array(100).keys()],
        datasets: [
            {
                label: "Node",
                data: [],
                fill: false,
                borderColor: "rgb(75, 192, 192)",
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
                borderColor: "rgb(75, 192, 192)",
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
                borderColor: "rgb(75, 192, 192)",
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
                borderColor: "rgb(75, 192, 192)",
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
    },
};

export let staticChartData = {
    type: "line",
    data: {
        labels: [...Array(defaultDist.length).keys()],
        datasets: [
            {
                label: "Probability",
                data: defaultDist,
                borderWidth: 1,
                fill: false,
                borderColor: "rgb(21, 52, 228)",
                tension: 0.1,
                pointRadius: 0,
            },
        ],
    },
    options: {
        responsive: true,
        maintainAspectRatio: false,
        scales: {
            y: {
                beginAtZero: true,
            },
        },

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

document.getElementById('defaultOpen').click()

cy.layout({name: "circle"}).run();
