export class DynamicQuantumwalk {
    constructor(_graph, _timeList, _initStateList,_probDist,_walkName) {
        this._graph = _graph;
        this._timeList = _timeList;
        this._initStateList = _initStateList;
        this._probDist = _probDist;
        this._walkName = _walkName;
    }

    reset(){
        this._dim = 100;
        this.time = [0,10];
        this._initState = [[50]];
        this._graph = 'nx.cycle_graph'
        console.log("WALK RESET")
    }

    get graph() {
        return this._graph;
    }

    set graph(newGraph) {
        this._graph = newGraph;
    }

    get timeList() {
        return this._timeList;
    }

    set timeList(newTimeList) {
        this._timeList = newTimeList;
    }

    get initStateList() {
        return this._initStateList;
    }

    set initStateList(newInitStateList) {
        this._initStateList = newInitStateList;
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
