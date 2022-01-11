let getGraph = () => {
    return eel
        .graphToJson()()
        .then((a) => {
            return a ? a : Promise.reject(Error("Get Prob failed."));
        })
        .catch((e) => console.log(e));
};

let initGraph = async () => {
    let graphStr = 'nx.cycle_graph'
    eel.setDim(100, graphStr)
    eel.setGraph(graphStr)
}

initGraph()
let myGraph = await getGraph();

export let cy = cytoscape({
    container: document.getElementById("cy"), // container to render in
    boxSelectionEnabled: false,
    autounselectify: true,
    elements: myGraph.elements,
    directed: myGraph.directed,
    multigraph: myGraph.multigraph,
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

export let data = {
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
        scales: {
            y: {
                beginAtZero: true,
            },
        },
    },
};

export let data2 = {
    type: "line",
    data: {
        labels: [...Array(100).keys()],
        datasets: [
            {
                label: "Probability",
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
            y: {
                grid: {
                    display: false
                }
            }
        },
    },
};