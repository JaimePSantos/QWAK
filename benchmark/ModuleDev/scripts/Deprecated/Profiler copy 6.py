import os
import cProfile
import pstats
import re
import inspect
from functools import wraps
from io import StringIO
from tqdm import tqdm
from typing import Callable, List

global benchmark
benchmark = True

def profile(
    output_path,
    output_file=None,
    sort_by="cumulative",
    lines_to_print=None,
    strip_dirs=False,
    csv=False,
    tracked_attributes=None
):
    
    def noop_decorator(func):
        return func

    def inner(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            base_path = os.path.join(os.path.dirname(__file__), "TestOutput", "Profiling")
            os.makedirs(base_path, exist_ok=True)
            
            pr = cProfile.Profile()
            with tqdm(total=1, desc=f"Profiling {func.__name__}", unit="call") as pbar:
                pr.enable()
                result = func(*args, **kwargs)
                pr.disable()
                pbar.update(1)

            time_data = {}
            if tracked_attributes:
                sig = inspect.signature(func)
                try:
                    bound_args = sig.bind(*args, **kwargs)
                    bound_args.apply_defaults()
                    arguments = bound_args.arguments
                except Exception:
                    arguments = {}
                
                # Check if function is a method
                instance = None
                params = list(sig.parameters.values())
                if params and params[0].name == 'self' and args:
                    instance = args[0]
                
                for attr in tracked_attributes:
                    value = None
                    if attr in arguments:
                        value = arguments[attr]
                    elif instance and hasattr(instance, attr):
                        value = getattr(instance, attr, None)
                    if value is not None:
                        if isinstance(value, float):
                            formatted_value = f"{value:.4f}".replace('.', '_')
                        else:
                            formatted_value = str(value).replace('.', '_')
                        time_data[attr] = formatted_value

            # Folder structure: base_path / output_path / first_tracked_attr_value
            first_attr_part = ""
            if tracked_attributes and time_data:
                first_attr_name = tracked_attributes[0]
                first_attr_value = time_data.get(first_attr_name, "")
                if first_attr_value:
                    first_attr_part = f"{first_attr_name}_{first_attr_value}"

            final_output_path = os.path.join(base_path, output_path, first_attr_part)
            os.makedirs(final_output_path, exist_ok=True)

            # Filename uses all tracked attributes.
            attr_parts = [f"{k}_{v}" for k, v in time_data.items()]
            combined_attrs = '_'.join(attr_parts) if attr_parts else ''
            
            # If output_file is provided use it; otherwise use the function's name.
            # (Note the trailing underscore when output_file is None.)
            if output_file:
                filename = f"{output_file}-{combined_attrs}.prof"
            else:
                filename = f"{func.__name__}-{combined_attrs}_.prof"

            full_path = os.path.join(final_output_path, filename)

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
        
        # Store configuration for later lookup.
        wrapper._profile_config = {
            'output_path': output_path,
            'output_file': output_file,
            'tracked_attributes': tracked_attributes,
        }
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
    return "\n".join([",".join(line.rstrip().split(None, 5)) for line in result.split("\n") if line])

def get_profiling_path(instance, method: Callable) -> str:
    """
    (Legacy) Reconstructs the expected profiling file path.
    """
    # Get original decorated function.
    if inspect.ismethod(method):
        func = method.__func__
    else:
        func = method

    # Verify profiling was configured.
    if not hasattr(func, '_profile_config'):
        raise ValueError(f"Method {func.__name__} was not decorated with @profile")

    config = func._profile_config

    # Determine tracked attributes.
    tracked_attrs = config.get('tracked_attributes')
    if tracked_attrs is None:
        tracked_attrs = getattr(instance, 'tracked_attributes', None)
        if tracked_attrs is None:
            raise ValueError("No tracked_attributes defined in decorator or instance")

    # Collect and format values from the instance.
    formatted_values = {}
    for attr in tracked_attrs:
        value = getattr(instance, attr, None)
        if value is None:
            raise ValueError(f"Missing required attribute: {attr}")
        if isinstance(value, float):
            formatted = f"{value:.4f}".replace('.', '_')
        else:
            formatted = str(value).replace('.', '_')
        formatted_values[attr] = formatted

    # Build directory structure.
    first_attr = tracked_attrs[0]
    dir_structure = os.path.join(
        os.path.dirname(__file__),
        "TestOutput",
        "Profiling",
        config['output_path'],
        f"{first_attr}_{formatted_values[first_attr]}"
    )

    # Build filename.
    filename_base = config['output_file'] or func.__name__
    attr_str = '_'.join([f"{k}_{v}" for k, v in formatted_values.items()])
    # Match the profiler's filename logic: if no output_file, add a trailing underscore.
    if config['output_file']:
        filename = f"{filename_base}-{attr_str}.prof"
    else:
        filename = f"{filename_base}-{attr_str}_.prof"

    full_path = os.path.join(dir_structure, filename)

    if not os.path.exists(full_path):
        raise FileNotFoundError(
            f"Profiling data missing for {func.__name__} with parameters:\n"
            f"Tracked attributes: {tracked_attrs}\n"
            f"Current values: {formatted_values}\n\n"
            "Run profiling first with:\n"
            f"{instance.__class__.__name__}.{func.__name__}()"
        )

    return full_path

def find_exact_profiling_file(instance, method: Callable) -> str:
    """
    Reconstructs the exact profiling file path based on how the profiler creates
    its folder structure and filename (using tracked attributes) and returns it if found.

    Usage:
        try:
            exact_path = find_exact_profiling_file(benchmark_instance, benchmark_instance.init_operator)
        except FileNotFoundError as e:
            print(e)
    """
    # Get the original function from the method.
    if inspect.ismethod(method):
        func = method.__func__
    else:
        func = method

    # Ensure the function was decorated.
    if not hasattr(func, '_profile_config'):
        raise ValueError(f"Method {func.__name__} was not decorated with @profile")
    config = func._profile_config

    # Determine which tracked attributes to use.
    tracked_attrs = config.get('tracked_attributes')
    if tracked_attrs is None:
        tracked_attrs = getattr(instance, 'tracked_attributes', None)
        if tracked_attrs is None:
            raise ValueError("No tracked_attributes defined in decorator or instance")

    # Gather and format values from the instance.
    formatted_values = {}
    for attr in tracked_attrs:
        value = getattr(instance, attr, None)
        if value is None:
            raise ValueError(f"Missing required attribute: {attr}")
        if isinstance(value, float):
            formatted = f"{value:.4f}".replace('.', '_')
        else:
            formatted = str(value).replace('.', '_')
        formatted_values[attr] = formatted

    # Rebuild the directory path (which uses the first tracked attribute).
    first_attr = tracked_attrs[0]
    dir_structure = os.path.join(
        os.path.dirname(__file__),
        "TestOutput",
        "Profiling",
        config['output_path'],
        f"{first_attr}_{formatted_values[first_attr]}"
    )

    # Rebuild the filename exactly as the profiler does.
    filename_base = config['output_file'] or func.__name__
    attr_str = '_'.join([f"{k}_{v}" for k, v in formatted_values.items()])
    if config['output_file']:
        filename = f"{filename_base}-{attr_str}.prof"
    else:
        filename = f"{filename_base}-{attr_str}_.prof"

    full_path = os.path.join(dir_structure, filename)

    if not os.path.exists(full_path):
        raise FileNotFoundError(
            f"Profiling file not found at:\n{full_path}\n"
            f"Expected tracked attributes: {tracked_attrs}\n"
            f"Current attribute values: {formatted_values}\n"
            "Make sure to run profiling before searching for the file."
        )

    return full_path
