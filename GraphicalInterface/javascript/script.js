import { defaultDist, cy } from "./tools.js";

let defaultN = 100;
let defaultT = 30;
let defaultGamma = (1/(2*Math.sqrt(2))).toFixed(2);
let defaultInitState = [Math.floor(defaultN/2),Math.floor(defaultN/2)+1];
let defaultGraph = 'nx.cycle_graph';

let currentN = defaultN;
let currentT = defaultT;
let currentGamma = defaultGamma;
let currentInitState = defaultInitState;
let currentGraph = defaultGraph;

let goButton = document.getElementById("goButton");
let goMultipleButton = document.getElementById("goMultipleButton");
let graphButton = document.getElementById("graphButton");

let setTimeButton = document.getElementById("setTimeButton");
let setGammaButton = document.getElementById("setGammaButton");
let setDimButton = document.getElementById("setDimButton");
let setGraphButton = document.getElementById("setGraphButton");
let setInitStateButton = document.getElementById("setInitStateButton");

let inputTime = document.getElementById("inputTime");
let inputGamma = document.getElementById("inputGamma");
let inputDim =  document.getElementById("inputDim");
let inputGraph =  document.getElementById("inputGraph");
let inputInitState = document.getElementById("inputInitState");
let inputInit = () => {
  inputTime.value = defaultT;
  inputGamma.value = defaultGamma;
  inputDim.value = defaultN;
  inputGraph.value = defaultGraph;
  inputInitState.value = defaultInitState
}
inputInit()

let defaultTimeList = [0,100];
let defaultGammaList = [(1/(2*Math.sqrt(2))).toFixed(2)];
let defaultInitStateList = [[Math.floor(defaultN/2),Math.floor(defaultN/2)+1]];

let currentTimeList = defaultTimeList;
let currentGammaList = defaultGammaList;
let currentInitStateList = defaultInitStateList;

let setTimeRangeButton = document.getElementById("setTimeRangeButton");
let setGammaRangeButton = document.getElementById("setGammaRangeButton");
let setInitStateRangeButton = document.getElementById("setInitStateRangeButton");

let inputTimeRange = document.getElementById("inputTimeRange");
let inputGammaRange = document.getElementById("inputGammaRange");
let inputInitStateRange = document.getElementById("inputInitStateRange");
let inputRangeInit = () => {
  inputTimeRange.value = defaultTimeList;
  inputGammaRange.value = defaultGammaList;
  inputInitStateRange.value = defaultInitStateList;
}
inputRangeInit()

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

cy.layout({ name: "circle" }).run();

let myChart = new Chart(ctx, data);
let myAnimatedChart = new Chart(ctx2, data2);

let setTimeRangeButtonPress = setTimeRangeButton.onclick = async () => {
  currentTimeList = inputTimeRange.value;
  eel.setTimeList(currentTimeList)
}

let setInitStateButtonPress = setInitStateButton.onclick = async () => {
  currentInitState = inputInitState.value;
  eel.setInitState(currentInitState)
}

let setTimeButtonPress = setTimeButton.onclick = async () => {
  currentT = parseInt(inputTime.value);
  eel.setTime(currentT);
}

let setGammaButtonPress = setGammaButton.onclick = async () => {
  currentGamma = parseFloat(inputGamma.value);
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
  let multipleWalks = await getMultipleWalks();
  let i = 0;
  myAnimatedChart.clear();
  for (const walk of multipleWalks) {
    setTimeout(() => {
      data2.data.datasets[0].data = walk.flat();
      data2.data.labels = [...Array(walk.length).keys()];
      myAnimatedChart.update();
    }, 80 * i);
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
  data.data.datasets[0].data = distList;
  data.data.labels = [...Array(distList.length).keys()];
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
    .runMultipleWalks()()
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