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

     set mean(newMean){
        this._mean = newMean;
    }

    get mean(){
        return this._mean;
    }

    set sndMoment(newSndMoment){
        this._sndMoment = newSndMoment;
    }

    get sndMoment(){
        return this._sndMoment;
    }

    set stDev(newStDev){
        this._stDev = newStDev;
    }

    get stDev(){
        return this._stDev;
    }

    set invPartRatio(newInvPartRatio){
        this._invPartRatio = newInvPartRatio;
    }

    get invPartRatio(){
        return this._invPartRatio;
    }

    set survivalProb(newSurvivalProb){
        this._survivalProb = newSurvivalProb;
    }

    get survivalProb(){
        return this._survivalProb;
    }

    set PST(newPst){
        this._PST = newPst;
    }

    get PST(){
        return this._PST;
    }
}
