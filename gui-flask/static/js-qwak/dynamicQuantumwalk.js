export class DynamicQuantumwalk {
    constructor(_graph, _timeList, _initStateList) {
        this._graph = _graph;
        this._timeList = _timeList;
        this._initStateList = _initStateList;
    }

    reset(){
        this._dim = [100];
        this.time = [10];
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
}
