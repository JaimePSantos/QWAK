export class QuantumWalk {
    constructor(_dim,_time,_gamma,_initState,_graph) {
        this._dim = _dim;
        this._time = _time;
        this._gamma = _gamma;
        this._initState = _initState;
        this._graph = _graph;
    }

    get dim(){
        return this._dim;
    }

    set dim(newDim){
        this._dim = newDim;
    }

    get time(){
        return this._time;
    }

    set time(newTime){
        this._time = newTime;
    }

    get gamma(){
        return this._gamma;
    }

    set gamma(newGamma){
        this._gamma = newGamma;
    }

    get initState(){
        return this._initState;
    }

    set initState(newInitState){
        this._initState = newInitState;
    }

    get graph(){
        return this._graph;
    }

    set graph(newGraph){
        this._graph = newGraph;
    }
}