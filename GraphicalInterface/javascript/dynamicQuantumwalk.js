export class DynamicQuantumwalk {
        constructor(_graph,_timeList,_gammaList,_initStateList) {
        this._graph = _graph;
        this._timeList = _timeList;
        this._gammaList = _gammaList;
        this._initStateList = _initStateList;
    }

    get graph(){
        return this._graph;
    }

    set graph(newGraph){
        this._graph = newGraph;
    }

    get timeList(){
        return this._timeList;
    }

    set timeList(newTimeList){
        this._timeList = newTimeList;
    }

    get gammaList(){
        return this._gammaList;
    }

    set gammaList(newGammaList){
        this._gammaList = newGammaList;
    }

    get initStateList(){
        return this._initStateList;
    }

    set initStateList(newInitStateList){
        this._initStateList = newInitStateList;
    }
}
