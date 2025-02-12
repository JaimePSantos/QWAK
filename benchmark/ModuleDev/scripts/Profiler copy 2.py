import os
import cProfile
import pstats
from functools import wraps
from io import StringIO
from os.path import exists

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
    """
    A time profiler decorator. Inspired by and modified the profile decorator of Giampaolo Rodola: http://code.activestate.com/recipes/577817-profile-decorator/

    Args:
        :param output_file: Default is None Path of the output file. If only name of the file is given, it's saved in the current directory. If it's None, the name of the decorated function is used.
        :type output_file: str or None.
        :param sort_by: Sorting criteria for the Stats object. For a list of valid string and SortKey refer to: https://docs.python.org/3/library/profile.html#pstats.Stats.sort_stats
        :type sort_by: str or SortKey enum or tuple/list of str/SortKey enum.
        :param lines_to_print: Number of lines to print. Default (None) is for all the lines. This is useful in reducing the size of the printout, especially that sorting by 'cumulative', the time consuming operations are printed toward the top of the file.
        :type lines_to_print: int or None.
        :param strip_dirs: Whether to remove the leading path info from file names. This is also useful in reducing the size of the printout
        :type: strip_dirs: bool.

    Returns:
        Profile of the decorated function
    """

    def noop_decorator(func):
        return func  # pass through

    def inner(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            path = os.path.join(
                os.path.dirname(__file__),
                "TestOutput",
                "Profiling"
            )
            os.makedirs(path, exist_ok=True)  # Create TestOutput/Profiling
            os.chdir(path)

            # Construct the output file path
            if output_file is not None:
                _output_file = os.path.join(output_path, output_file)
            else:
                _output_file = os.path.join(output_path, func.__name__ + ".prof")

            # Ensure the directory for _output_file exists
            output_dir = os.path.dirname(_output_file)
            os.makedirs(output_dir, exist_ok=True)  # Key fix: create subdirectories

            pr = cProfile.Profile()
            pr.enable()
            retval = func(*args, **kwargs)
            pr.disable()

            # Save profiling results
            with open(_output_file, "a+") as f:
            # ... rest of the code ...
                ps = pstats.Stats(pr, stream=f)
                if strip_dirs:
                    ps.strip_dirs()
                if isinstance(sort_by, (tuple, list)):
                    ps.sort_stats(*sort_by)
                else:
                    ps.sort_stats(sort_by)
                if csv:
                    csvFile = prof_to_csv(
                        pr, sort_by, lines_to_print, strip_dirs)
                    if exists(_output_file):
                        with open(_output_file, "a+") as f:
                            f.write(csvFile)
                    else:
                        with open(_output_file, "w+") as f:
                            f.write(csvFile)
                elif not csv:
                    pr.dump_stats(_output_file)
            return retval

        return wrapper

    global benchmark
    return inner if benchmark else noop_decorator


def prof_to_csv(
        prof,
        sort_by="cumulative",
        lines_to_print=None,
        strip_dirs=False):
    out_stream = StringIO()
    ps = pstats.Stats(prof, stream=out_stream).print_stats()
    if strip_dirs:
        ps.strip_dirs()
    if isinstance(sort_by, (tuple, list)):
        ps.sort_stats(*sort_by)
    else:
        ps.sort_stats(sort_by)
    ps.print_stats(lines_to_print)
    result = out_stream.getvalue()
    # chop off header lines
    result = "ncalls" + result.split("ncalls")[-1]
    lines = [",".join(line.rstrip().split(None, 5))
             for line in result.split("\n")]
    lines.append("Next Entry")
    lines.append("\n")
    lines = list(filter(None, lines))
    return "\n".join(lines)
