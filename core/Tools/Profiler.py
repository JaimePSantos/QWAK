import cProfile, pstats
from functools import wraps
from io import StringIO

global benchmark
benchmark = True

import os
#retval = os.getcwd()
#os.chdir( retval + "../../TestOutput/Profiling/" )

def profile(output_path,output_file=None, sort_by='cumulative', lines_to_print=None, strip_dirs=False,csv=False):
    """A time profiler decorator.
    Inspired by and modified the profile decorator of Giampaolo Rodola:
    http://code.activestate.com/recipes/577817-profile-decorator/
    Args:
        output_file: str or None. Default is None
            Path of the output file. If only name of the file is given, it's
            saved in the current directory.
            If it's None, the name of the decorated function is used.
        sort_by: str or SortKey enum or tuple/list of str/SortKey enum
            Sorting criteria for the Stats object.
            For a list of valid string and SortKey refer to:
            https://docs.python.org/3/library/profile.html#pstats.Stats.sort_stats
        lines_to_print: int or None
            Number of lines to print. Default (None) is for all the lines.
            This is useful in reducing the size of the printout, especially
            that sorting by 'cumulative', the time consuming operations
            are printed toward the top of the file.
        strip_dirs: bool
            Whether to remove the leading path info from file names.
            This is also useful in reducing the size of the printout
    Returns:
        Profile of the decorated function
    """
    def noop_decorator(func):
        return func  # pass through

    def inner(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            if output_file is not None:
                _output_file = output_path + output_file
            else:
                _output_file = output_path + func.__name__ + '.prof'
            pr = cProfile.Profile()
            pr.enable()
            retval = func(*args, **kwargs)
            pr.disable()
            with open(_output_file, 'w') as f:
                ps = pstats.Stats(pr, stream=f)
                if strip_dirs:
                    ps.strip_dirs()
                if isinstance(sort_by, (tuple, list)):
                    ps.sort_stats(*sort_by)
                else:
                    ps.sort_stats(sort_by)
                if csv:
                    csvFile = prof_to_csv(pr,sort_by, lines_to_print, strip_dirs)
                    with open(_output_file, 'a+') as f:
                        f.write(csvFile)
                elif not csv:
                    pr.dump_stats(_output_file)
            return retval
        return wrapper
    global benchmark
    return inner if benchmark else noop_decorator

def prof_to_csv(prof,sort_by='cumulative', lines_to_print=None, strip_dirs=False):
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
    result = 'ncalls' + result.split('ncalls')[-1]
    lines = [','.join(line.rstrip().split(None, 5)) for line in result.split('\n')]
    return '\n'.join(lines)