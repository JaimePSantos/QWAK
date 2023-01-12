export function setStaticDim(newDim, graphStr) {
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

export async function setDynamicDim(newDim, graphStr) {
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

export async function setStaticGraph(newDim,newGraph) {
    let myGraph;
    await $.ajax({
        type: 'POST',
        url: `/setStaticGraph`,
        data: {newDim:newDim,newGraph:newGraph},
        success: function (response) {
            console.log(`success - graph set to ${newGraph}:\n ${response}`)
            // console.log(response);
            myGraph = response;
            return myGraph;
        },
        error: function (response) {
            myGraph = response;
            return myGraph;
        }
    });
    return myGraph;
}

export async function setDynamicGraph(newDim,newGraph) {
    let myGraph;
    await $.ajax({
        type: 'POST',
        url: `/setDynamicGraph`,
        data: {newDim:newDim, newGraph: newGraph},
        success: function (response) {
            console.log(`success - graph set to ${newGraph}`);
            myGraph = response;
            return myGraph;
        },
        error: function (response) {
            console.log('setGraph error');
            myGraph = response;
            return myGraph;
        }
    })
    return myGraph;
}

export let updateGraph = (graph,cyObject) => {
    cyObject.elements().remove()
    cyObject.add(graph.elements)
    cyObject.layout({name: "circle"}).run();
}

// - Custom Graph

let nodeNumber = 2;
let nodeXPos = 200;
let nodeYPos = 0;

export async function addNodeButtonPress(cyObject) {
    nodeNumber++;
    nodeYPos += 50;
    cyObject.add({
        group: 'nodes',
        data: {id: nodeNumber.toString(), name: nodeNumber.toString()},
        position: {x: nodeXPos, y: nodeYPos}
    });
}

export function setCustomAdjacencyMatrix(customAdjacency) {
    $.ajax({
        type: 'POST',
        url: `/setDynamicCustomGraph`, // <- Add the queryparameter here
        data: {customAdjacency: customAdjacency},
        async: false,
        success: function (response) {
            console.log('success - customAdjacency set to ${customAdjacency}');
        },
        error: function (response) {
            console.log('customAdjacency error');
        }
    });
}

export function createAdjacencyMatrix(graph) {
    let adjacencyMatrix = math.zeros(graph.json().elements.nodes.length, graph.json().elements.nodes.length)

    for (let edg of graph.json().elements.edges) {
        // console.log(`Source: ${edg.data.source} -> Target: ${edg.data.target}`);
        adjacencyMatrix.subset(math.index(parseInt(edg.data.source), parseInt(edg.data.target)), 1);
        adjacencyMatrix.subset(math.index(parseInt(edg.data.target), parseInt(edg.data.source)), 1);
    }
    adjacencyMatrix = adjacencyMatrixToString(adjacencyMatrix);
    return adjacencyMatrix;
}

export function adjacencyMatrixToString(adjacencyMatrix) {
    let adjm = "[";
    let elemAux = "";
    for (let elem of adjacencyMatrix._data) {
        elemAux = "["
        for (let e of elem) {
            elemAux = elemAux.concat(",", e);
        }
        elemAux = elemAux.concat("", "]")
        elemAux = elemAux.slice(0, 1) + elemAux.slice(2)
        adjm = adjm.concat(",", elemAux)
        elemAux = "";
    }
    adjm = adjm.concat("", "]")
    adjm = adjm.slice(0, 1) + adjm.slice(2)
    return adjm
}