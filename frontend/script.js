let thing = eel.runWalk();
let goButton = document.getElementById("goButton");
let ctx = document.getElementById('myChart').getContext('2d');
let myDist = new Array()

let data = {
    type: 'line',
    data: {
        labels: ['Red', 'Blue', 'Yellow', 'Green', 'Purple', 'Orange'],
        datasets: [{
            label: '# of Votes',
            data: [12, 19, 3, 5, 2, 3],
            borderWidth: 1,
            fill:false,
            borderColor:'rgb(21, 52, 228)',
            tension: 0.1,
            pointRadius:0,
        }]
    },
    options: {
        scales: {
            y: {
                beginAtZero: true
            }
        }
    }
};

let newData = {...data}


let myChart = new Chart(ctx, data)

function print_arr(n) {
    console.log(`Got this from python: ${n}`)
}

let goButtonPress = goButton.onclick = () => {
    getPromisedData(eel.runWalk()).then((a) => myDist = a);
    let distList = myDist.flat();
    console.log(data.data.datasets)
    newData.data.datasets[0].data = distList
    newData.data.labels = [...Array(distList.length-1).keys()]
    myChart.destroy();
    myChart = new Chart(ctx,data)
}

function getPromisedData(promise) {
    let myData = promise().then(data => {
        return data
    }).catch(e => console.log(e))
    return myData
}