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
  
    layout: {
      name: 'concentric',
      concentric: function (n) { return n.id() === '0' ? 200 : 0; },
      levelWidth: function (nodes) { return 100; },
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
        { data: { id: '0', name: '0' } },
        { data: { id: '1', name: '1' } },
        { data: { id: '2', name: '2' } }
      ],
      edges: [
        { data: { source: '0', target: '1' } },
        { data: { source: '1', target: '2' } }
      ]
    }
  });

  document.getElementById('defaultOpen').click()
