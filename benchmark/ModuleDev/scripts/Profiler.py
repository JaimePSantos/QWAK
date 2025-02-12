import os
import cProfile
import pstats
from functools import wraps
from io import StringIO
from tqdm import tqdm
import inspect

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
                except:
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

            # Path uses only first tracked attribute
            first_attr_part = ""
            if tracked_attributes and time_data:
                first_attr_name = tracked_attributes[0]
                first_attr_value = time_data.get(first_attr_name, "")
                if first_attr_value:
                    first_attr_part = f"{first_attr_name}_{first_attr_value}"

            final_output_path = os.path.join(base_path, output_path, first_attr_part)
            os.makedirs(final_output_path, exist_ok=True)

            # Filename uses all tracked attributes
            attr_parts = [f"{k}_{v}" for k, v in time_data.items()]
            combined_attrs = '_'.join(attr_parts) if attr_parts else ''
            
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