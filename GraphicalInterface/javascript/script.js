import {defaultDist, cy} from "./tools.js";

let goButton = document.getElementById("goButton");
let graphButton = document.getElementById("graphButton");
let ctx = document.getElementById("myChart").getContext("2d");
let myDist = new Array();

let data = {
  type: "line",
  data: {
    labels: [...Array(defaultDist.length).keys()],
    datasets: [
      {
        label: "# of Votes",
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

cy.on('mouseup', function (e) {
    let tg = e.target;
    if (tg.group != undefined && tg.group() == 'nodes') {
        let w = cy.width();
        let h = cy.height();
        if (tg.position().x > w) tg.position().x = w;
        if (tg.position().x < 0) tg.position().x = 0;
        if (tg.position().y > h) tg.position().y = h;
        if (tg.position().y < 0) tg.position().y = 0;
    }
})

let newData = { ...data };

let myChart = new Chart(ctx, data);

function print_arr(n) {
  console.log(`Got this from python: ${n}`);
}

let graphButtonPress = (graphButton.onclick = async () => {
  let myGraphString = await getGraph();
  let myGraph = JSON.parse(myGraphString)
  // console.log(cy.elements)
  // console.log(myGraph)
  cy.json({elements:myGraph})
})

let goButtonPress = (goButton.onclick = async () => {
  myDist = await getWalk();
  let distList = myDist.flat();
  newData.data.datasets[0].data = distList;
  newData.data.labels = [...Array(distList.length).keys()];
  myChart.destroy();
  myChart = new Chart(ctx, data);
});

let getWalk = () => {
  return eel
    .runWalk()()
    .then((a) => {
      return a ? a : Promise.reject(Error("Get Prob failed."));
    })
    .catch((e) => console.log(e));
};

let getGraph = () => {
  return eel
    .graphToJson()()
    .then((a) => {
      return a ? a : Promise.reject(Error("Get Prob failed."));
    })
    .catch((e) => console.log(e));
};

function getPromisedData(promise) {
  let myData = promise()
    .then((data) => {
      return data;
    })
    .catch((e) => console.log(e));
  return myData;
}
