def runTimedQWAK2(n,pVal,t,seed):
    start_time = time.time()
    initNodes = [n//2]
    graph = nx.erdos_renyi_graph(n,pVal,seed=seed) 
    qw = QWAK(graph)
    qw.runWalk(t, initNodes)
    end_time = time.time()
    qwak_time = end_time - start_time
    final_state = qw.getProbVec()
    return final_state, qwak_time

def runTimedQWAK2_cupy(n,pVal,t,seed):
    start_time = time.time()
    initNodes = [n//2]
    graph = nx.erdos_renyi_graph(n,pVal,seed=seed) 
    qw = CQWAK(graph)
    qw.runWalk(t, initNodes)
    end_time = time.time()
    qwak_time = end_time - start_time
    final_state = qw.getProbVec()
    return final_state, qwak_time

def runMultipleSimpleQWAK3(nList, pVal, t, samples):#, seed_list_dict):
    qwList = []
    tList = []
    qwak_time = 0
    qwak_time_average = 0

    for n in tqdm(nList, desc=f"NPQWAK {len(nList)}:{nList[0]}->{nList[-1]}", leave=False):
        for sample in tqdm(range(1, samples + 1), desc=f"Samples for N = {n}"):
            qw, qwak_time = runTimedQWAK2(n, pVal, t, 10)
            qwak_time_average += qwak_time

        qwak_time_average = qwak_time_average / samples
        qwList.append(qw)
        tList.append(qwak_time_average)
        qwak_time_average = 0

    return tList, qwList

def runMultipleSimpleQWAK3_cupy(nList, pVal, t, samples):#, seed_list_dict):
    qwList = []
    tList = []
    qwak_time = 0
    qwak_time_average = 0

    for n in tqdm(nList, desc=f"CuPyQWAK {len(nList)}:{nList[0]}->{nList[-1]}", leave=False):
        # Access the corresponding seed list for the current `n`
        for sample in tqdm(range(1, samples + 1), desc=f"Samples for N = {n}"):
            qw, qwak_time = runTimedQWAK2_cupy(n, pVal, t, 10)
            qwak_time_average += qwak_time
        qwak_time_average = qwak_time_average / samples
        qwList.append(qw)
        tList.append(qwak_time_average)
        qwak_time_average = 0

    return tList, qwList