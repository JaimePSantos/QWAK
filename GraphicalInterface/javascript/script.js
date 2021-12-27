import { defaultDist, cy } from "./tools.js";

let defaultN = 100;
let defaultT = 30;
let defaultGamma = (1/(2*Math.sqrt(2))).toFixed(2);
let defaultInitState = [Math.floor(defaultN/2)];
let defaultGraph = 'nx.cycle_graph';

let currentN = defaultN;
let currentT = defaultT;
let currentGamma = defaultGamma;
let curentInitState = defaultInitState;
let currentGraph = defaultGraph;

let goButton = document.getElementById("goButton");
let goMultipleButton = document.getElementById("goMultipleButton");
let graphButton = document.getElementById("graphButton");
let setTimeButton = document.getElementById("setTimeButton");
let setGammaButton = document.getElementById("setGammaButton");
let setDimButton = document.getElementById("setDimButton");
let setGraphButton = document.getElementById("setGraphButton");

let inputTime = document.getElementById("inputTime");
let inputGamma = document.getElementById("inputGamma");
let inputDim =  document.getElementById("inputDim");
let inputGraph =  document.getElementById("inputGraph");
let inputInit = () => {
  inputTime.value = defaultT;
  inputGamma.value = defaultGamma;
  inputDim.value = defaultN;
  inputGraph.value = defaultGraph;
}
inputInit()

let ctx = document.getElementById("myChart").getContext("2d");
let ctx2 = document.getElementById("myAnimatedChart").getContext("2d");
let myDist = new Array();

let data = {
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

let data2 = {
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
  type: "line",
  options: {
    scales: {
      y: {
        // defining min and max so hiding the dataset does not change scale range
        min: 0,
        max: 0.5,
      },
    },
  },
};

cy.on("mouseup", function (e) {
  let tg = e.target;
  if (tg.group != undefined && tg.group() == "nodes") {
    let w = cy.width();
    let h = cy.height();
    if (tg.position().x > w) tg.position().x = w;
    if (tg.position().x < 0) tg.position().x = 0;
    if (tg.position().y > h) tg.position().y = h;
    if (tg.position().y < 0) tg.position().y = 0;
  }
});

cy.layout({ name: "circle" }).run();

let newData = { ...data };
let newData2 = { ...data2 };

let myChart = new Chart(ctx, data);
let myAnimatedChart = new Chart(ctx2, data2);

let setTimeButtonPress = setTimeButton.onclick = async() => {
  currentT = parseInt(inputTime.value);
  eel.setTime(currentT);
}

let setGammaButtonPress =setGammaButton.onclick = async () => {
  currentGamma = parseInt(inputGamma.value);
  eel.setGamma(currentGamma);
}

let setDimButtonPress = setDimButton.onclick = async () => {
  currentN = parseInt(inputDim.value);
  currentGraph = inputGraph.value;
  eel.setDim(currentN,currentGraph);
}

let setGraphButtonPress = setGraphButton.onclick = async () => {
  currentGraph = inputGraph.value;
  eel.setGraph(currentGraph);
}

let goMultipleButtonPress = goMultipleButton.onclick = async () => {
  let walk = await getMultipleWalks();
  let distListList = walk;
  let i = 0;
  for (const distList of distListList) {
    setTimeout(() => {
      console.log(distList);
      data2.data.datasets[0].data = distList.flat();
      data2.data.labels = [...Array(distList.length).keys()];
      myAnimatedChart.update();
    }, 100 * i);
    i++;
  }
};

let graphButtonPress = graphButton.onclick = async () => {
  let myGraph = await getGraph();
  updateGraph(myGraph)
};

let goButtonPress = goButton.onclick = async () => {
  myDist = await getWalk();
  let distList = myDist.flat();
  newData.data.datasets[0].data = distList;
  newData.data.labels = [...Array(distList.length).keys()];
  myChart.destroy();
  myChart = new Chart(ctx, data);
};

let getWalk = () => {
  return eel
    .runWalk()()
    .then((a) => {
      return a ? a : Promise.reject(Error("Get Walk failed."));
    })
    .catch((e) => console.log(e));
};

let getMultipleWalks = () => {
  return eel
    .runMultipleWalks([...Array(100).keys()])()
    .then((a) => {
      return a ? a : Promise.reject(Error("Get Multiple Walks failed."));
    })
    .catch((e) => console.log(e));
};

let getGraph = () => {
  return eel
    .graphToJson()()
    .then((a) => {
      return a ? a : Promise.reject(Error("Get Graph failed."));
    })
    .catch((e) => console.log(e));
};

let getTime = () => {
  return eel
  .getTime()()
  .then((a) => {
    return a ? a : Promise.reject(Error("Get Time failed."));
  })
  .catch((e) => console.log(e));
}

let updateGraph = (graph) =>{
  cy.elements().remove()  
  cy.add(graph.elements)
  cy.layout({ name: "circle" }).run();
}