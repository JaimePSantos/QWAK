class QuantumWalk {
    constructor(_dim,_time,_gamma,_initState,_graph) {
        this.dim = _dim;
        this.time = _time;
        this.gamma = _gamma;
        this.initState = _initState;
        this.graph = _graph;
    }

    get dim(){
        return this.dim;
    }

    set dim(newDim){
        this.dim = newDim;
    }

    get time(){
        return this.time;
    }

    set time(newTime){
        this.time = newTime;
    }

    get gamma(){
        return this.gamma;
    }

    set gamma(newGamma){
        this.gamma = newGamma;
    }

    get initState(){
        return this.initState;
    }

    set initState(newInitState){
        this.initState = newInitState;
    }

    get graph(){
        return this.graph;
    }

    set graph(newGraph){
        this.graph = newGraph;
    }
}