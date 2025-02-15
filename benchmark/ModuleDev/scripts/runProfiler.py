import networkx as nx

from OperatorBenchmark import OperatorBenchmark

if __name__ == "__main__":
    n = 1000
    t = 10
    graph = nx.cycle_graph(n)
    print(nx.cycle_graph.__name__)
    marked = [20]

    # Initialize benchmark
    graph = nx.cycle_graph(n)
    bench = OperatorBenchmark(graph,t, tracked_attributes=['n'])

    # Run profiling
    bench.init_operator()

    bench.build_operator(time=t)

    print(bench.load_files('init_operator'))
    print(bench.load_files('build_operator'))