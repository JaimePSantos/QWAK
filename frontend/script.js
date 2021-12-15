let thing  = eel.runWalk();
goButton = document.getElementById("goButton");

function print_arr(n){
    console.log(`Got this from python: ${n}`)
}

let goButtonPress = goButton.onclick = () => {
    console.log(eel.runWalk()());
}