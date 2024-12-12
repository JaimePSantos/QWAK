def runTimedQWAK(n,t):
    start_time = time.time()
    initNodes = [n//2]
    qw = QWAK(nx.cycle_graph(n))
    qw.runWalk(t, initNodes)
    end_time = time.time()
    qwak_time = end_time - start_time
    return qw, qwak_time

def runTimedQWAK_cupy(n,t):
    start_time = time.time()
    initNodes = [n//2]
    qw = CQWAK(nx.cycle_graph(n))
    qw.runWalk(t, initNodes)
    end_time = time.time()
    qwak_time = end_time - start_time
    return qw, qwak_time

def runMultipleSimpleQWAK(nList,t,samples):
    qwList = []
    tList = []
    qwak_time = 0
    qwak_time_average = 0
    print(f"Running NP QWAK {len(nList)} walks up to n = {nList[-1]}")
    for n in nList:
        for sample in range(1,samples+1):
            print(f"----> Calculating NP QWAK for n = {n} \t Sample #{sample}",end='\r')
            qw, qwak_time = runTimedQWAK(n,t)
            qwak_time_average += qwak_time 
        qwak_time_average = qwak_time_average / samples
        qwList.append(qw)
        tList.append(qwak_time_average)
        qwak_time_average = 0
    return tList, qwList

def runMultipleSimpleQWAK_cupy(nList,t,samples):
    qwList = []
    tList = []
    qwak_time = 0
    qwak_time_average = 0
    print(f"Running CuPy QWAK {len(nList)} walks up to n = {nList[-1]}")
    for n in nList:
        # print(f"----> Calculating NP QWAK for n = {n}",end='\r')
        for sample in range(1,samples+1):
            print(f"----> Calculating CuPy QWAK for n = {n} \t Sample #{sample}",end='\r')
            qw, qwak_time = runTimedQWAK_cupy(n,t)
            qwak_time_average += qwak_time 
        qwak_time_average = qwak_time_average / samples
        qwList.append(qw)
        tList.append(qwak_time_average)
        qwak_time_average = 0
    return tList, qwList

def load_list_from_file(file_path):
    with open(file_path, 'r') as file:
        data_str = file.read()
    data = [json.loads(line) for line in data_str.splitlines()]
    return data

def write_list_to_file(file_path, data):
    data_str = [str(item) for item in data]  # Convert float values to strings
    with open(file_path, 'w') as file:
        file.write('\n'.join(data_str))
t = 50
nMax = 500
nList = list(range(3,nMax,5))
samples = 1

qwak_times_file = f'Datasets/Benchmark-SimpleQWAK_Cycle/simpleQWAKTime_N{nList[0]}-{nList[-1]}_T{t}_S{samples}.txt'
qwak_times_file_cupy = f'Datasets/Benchmark-SimpleQWAK_Cycle/simpleQWAKTime_CuPy_N{nList[0]}-{nList[-1]}_T{t}_S{samples}.txt'

if os.path.exists(qwak_times_file):
    qwak_times = load_list_from_file(qwak_times_file)
    print('File Exists!')
else:
    qwak_times,qw = runMultipleSimpleQWAK(nList,t,samples)
    write_list_to_file(qwak_times_file,qwak_times)

if os.path.exists(qwak_times_file_cupy):
    qwak_times_cupy = load_list_from_file(qwak_times_file)
    print('File Exists!')
else:
    qwak_times_cupy ,qw = runMultipleSimpleQWAK_cupy(nList,t,samples)
    write_list_to_file(qwak_times_file_cupy,qwak_times)