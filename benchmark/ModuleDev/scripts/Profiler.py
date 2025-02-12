import os
import cProfile
import pstats
from functools import wraps
from io import StringIO
from tqdm import tqdm

global benchmark
benchmark = True

def profile(
    output_path,
    output_file=None,
    sort_by="cumulative",
    lines_to_print=None,
    strip_dirs=False,
    csv=False,
    time_attributes=None
):
    def noop_decorator(func):
        return func

    def inner(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            # Initial path setup
            base_path = os.path.join(os.path.dirname(__file__), "TestOutput", "Profiling")
            os.makedirs(base_path, exist_ok=True)
            
            pr = cProfile.Profile()
            with tqdm(total=1, desc=f"Profiling {func.__name__}", unit="call") as pbar:
                pr.enable()
                result = func(*args, **kwargs)
                pr.disable()
                pbar.update(1)

            # Get time attributes from instance
            instance = args[0] if args else None
            time_data = {}
            if time_attributes and instance:
                for attr in time_attributes:
                    time_data[attr] = getattr(instance, attr, 0)

            # Create dynamic output structure
            walk_time = f"walk_{time_data.get('walk_time', 0):.4f}".replace('.', '_')
            init_time = f"init_{time_data.get('init_time', 0):.4f}".replace('.', '_')
            n_dim = f"N_{time_data.get('n', 0)}".replace('.', '_')
            
            final_output_path = os.path.join(base_path, output_path,n_dim)
            os.makedirs(final_output_path, exist_ok=True)

            # Create filename
            if output_file:
                # filename = f"{init_time}_{output_file}"
                filename = f"{output_file}_{walk_time}"
            else:
                # filename = f"{init_time}_{func.__name__}.prof"
                filename = f"{func.__name__}_{walk_time}_.prof"

            full_path = os.path.join(final_output_path, filename)

            # Save results
            with open(full_path, "w") as f:
                ps = pstats.Stats(pr, stream=f)
                if strip_dirs:
                    ps.strip_dirs()
                ps.sort_stats(sort_by)
                
                if csv:
                    f.write(prof_to_csv(pr, sort_by, lines_to_print, strip_dirs))
                else:
                    ps.print_stats(lines_to_print)

            return result
        return wrapper

    return inner if benchmark else noop_decorator

def prof_to_csv(prof, sort_by, lines_to_print, strip_dirs):
    out_stream = StringIO()
    ps = pstats.Stats(prof, stream=out_stream)
    if strip_dirs:
        ps.strip_dirs()
    ps.sort_stats(sort_by).print_stats(lines_to_print)
    result = out_stream.getvalue()
    result = "ncalls" + result.split("ncalls")[-1]
    return "\n".join([",".join(line.rstrip().split(None,5)) for line in result.split("\n") if line])