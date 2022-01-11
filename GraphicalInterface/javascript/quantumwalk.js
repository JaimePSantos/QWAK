export class QuantumWalk {
    constructor(_dim,_time,_gamma,_initState,_graph,_timeList,_gammaList,_initStateList) {
        this._dim = _dim;
        this._time = _time;
        this._gamma = _gamma;
        this._initState = _initState;
        this._graph = _graph;
        this._timeList = _timeList;
        this._gammaList = _gammaList;
        this._initStateList = _initStateList;
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