import os
import cProfile
import pstats
from functools import wraps
from io import StringIO
from os.path import exists
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
):
    def noop_decorator(func):
        return func

    def inner(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            path = os.path.join(os.path.dirname(__file__), "TestOutput", "Profiling")
            os.makedirs(path, exist_ok=True)
            os.chdir(path)

            if output_file is not None:
                _output_file = os.path.join(output_path, output_file)
            else:
                _output_file = os.path.join(output_path, func.__name__ + ".prof")

            output_dir = os.path.dirname(_output_file)
            os.makedirs(output_dir, exist_ok=True)

            pr = cProfile.Profile()
            with tqdm(total=1, desc=f"Profiling {func.__name__}", unit="call") as pbar:
                pr.enable()
                retval = func(*args, **kwargs)
                pr.disable()
                pbar.update(1)

            with open(_output_file, "a+") as f:
                ps = pstats.Stats(pr, stream=f)
                if strip_dirs:
                    ps.strip_dirs()
                ps.sort_stats(sort_by)
                if csv:
                    csv_content = prof_to_csv(pr, sort_by, lines_to_print, strip_dirs)
                    f.write(csv_content)
                else:
                    pr.dump_stats(_output_file)
            return retval
        return wrapper

    return inner if benchmark else noop_decorator

def prof_to_csv(prof, sort_by="cumulative", lines_to_print=None, strip_dirs=False):
    out_stream = StringIO()
    ps = pstats.Stats(prof, stream=out_stream)
    if strip_dirs:
        ps.strip_dirs()
    ps.sort_stats(sort_by).print_stats(lines_to_print)
    result = out_stream.getvalue()
    result = "ncalls" + result.split("ncalls")[-1]
    lines = [",".join(line.rstrip().split(None, 5)) for line in result.split("\n")]
    lines.extend(["Next Entry", "\n"])
    return "\n".join(filter(None, lines))