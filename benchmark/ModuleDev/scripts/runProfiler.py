import networkx as nx

from OperatorBenchmark import OperatorBenchmark

from typing import List

def extract_top_cumtime(profiling_data: List[str]) -> List[float]:
    """
    Extracts the cumtime value from the top row of the profiling output for each file's data.
    
    Args:
        profiling_data (List[str]): List of profiling report strings.
        
    Returns:
        List[float]: A list of cumtime values extracted from the first profiling entry in each file.
        
    Raises:
        ValueError: If the expected header or data row cannot be found or parsed.
    """
    cumtime_values = []
    
    for data in profiling_data:
        lines = data.splitlines()
        header_index = None
        
        # Find the header line containing the columns (e.g., "ncalls ... cumtime")
        for i, line in enumerate(lines):
            if line.strip().startswith("ncalls") and "cumtime" in line:
                header_index = i
                break
        if header_index is None:
            raise ValueError("Profiling header with 'ncalls' and 'cumtime' not found in the data.")
        
        # The first non-empty line after the header is assumed to be the top row of data.
        for line in lines[header_index+1:]:
            if line.strip():
                tokens = line.split()
                try:
                    # Expected token order:
                    # tokens[0]: ncalls, tokens[1]: tottime, tokens[2]: percall, tokens[3]: cumtime, tokens[4]: percall, ...
                    cumtime = float(tokens[3])
                except (IndexError, ValueError) as e:
                    raise ValueError(f"Failed to extract cumtime from the profiling line: {line}") from e
                cumtime_values.append(cumtime)
                break  # Stop after processing the first valid data row.
    
    return cumtime_values


if __name__ == "__main__":
    n = 100
    t = 10
    graph = nx.cycle_graph(n)
    print(nx.cycle_graph.__name__)
    marked = [20]

    # Initialize benchmark
    graph = nx.cycle_graph(n)
    bench = OperatorBenchmark(tracked_attributes=['n','sample'])

    # Run profiling
    for sample in range(0,3):
        bench.init_operator2(graph=graph, sample=sample)

        # bench.build_operator(time=t,sample=sample)

    bench_init_file = bench.load_files2('init_operator')
    bench_operator_file = bench.load_files2('build_operator')

    # print(bench_init_file)

    cumtime = extract_top_cumtime(bench_init_file)

    print(cumtime)