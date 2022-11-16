export class StaticQuantumwalk {
    constructor(_dim, _time, _initState, _graph,_probDist,_walkName) {
        this._dim = _dim;
        this._time = _time;
        this._initState = _initState;
        this._graph = _graph;
        this._probDist = _probDist;
        this._walkName = _walkName;
    }

    reset(){
        this._dim = 100;
        this.time = 10;
        this._initState = [50]
        this._graph = 'nx.cycle_graph'
        console.log("WALK RESET")
    }

    get dim() {
        return this._dim;
    }

    set dim(newDim) {
        this._dim = newDim;
    }

    get time() {
        return this._time;
    }

    set time(newTime) {
        this._time = newTime;
    }

    get initState() {
        return this._initState;
    }

    set initState(newInitState) {
        this._initState = newInitState;
    }

    get graph() {
        return this._graph;
    }

    set graph(newGraph) {
        this._graph = newGraph;
    }

    set probDist(newProbDist){
        this._probDist = newProbDist;
    }

    get probDist(){
        return this._probDist;
    }

    set walkName(newWalkName){
        this._walkName = newWalkName;
    }

    get walkName(){
        return this._walkName;
    }
}