import os
import numpy as np
from matplotlib import pyplot as plt
from tqdm import tqdm
import shutil
from matplotlib.colors import LinearSegmentedColormap
from matplotlib.colors import Normalize


def process_profiling_data(
        path,
        method_name,
        nrange,
        sample_range,
        seed=None):
    for n in tqdm(nrange, desc="Processing n-values"):
        cumtimes = []
        for sample in sample_range:
            filename = f"{
                method_name}-n_{n}_sample_{sample}_pVal_0_8000_seed_{seed}.prof"
            filepath = os.path.join(path, f"n_{n}", filename)
            with open(filepath, 'r') as f:
                next(f)  # Skip the header line
                for line in f:
                    line = line.strip()
                    if not line:
                        continue
                    parts = line.split()
                    if len(parts) < 6:
                        continue
                    try:
                        cumtime = float(parts[3])
                    except (IndexError, ValueError):
                        continue
                    func_part = ' '.join(parts[5:])
                    if '(' in func_part and ')' in func_part:
                        func_name = func_part.split(
                            '(')[-1].split(')')[0]
                        if func_name == method_name:
                            cumtimes.append(cumtime)
                            break

        if cumtimes:
            average_cumtime = sum(cumtimes) / len(cumtimes)
            avg_folder = os.path.join(path, f"n_{n}_avg")
            os.makedirs(avg_folder, exist_ok=True)
            avg_filename = f"AVG-{method_name}-n_{n}_seed_{seed}.prof"
            avg_filepath = os.path.join(avg_folder, avg_filename)
            with open(avg_filepath, 'w') as avg_file:
                avg_file.write(f"{average_cumtime}\n")


def load_profiling_averages(path, method_name, nrange, seed=None):
    results = {}
    for n in tqdm(nrange, desc="Loading average times"):
        avg_folder = os.path.join(path, f"n_{n}_avg")
        avg_filename = f"AVG-{method_name}-n_{n}_seed_{seed}.prof"
        avg_filepath = os.path.join(avg_folder, avg_filename)
        try:
            with open(avg_filepath, 'r') as avg_file:
                results[n] = float(avg_file.readline().strip())
        except (FileNotFoundError, ValueError):
            raise ValueError(
                f"Average file not found or invalid format: {avg_filepath}")
    return results


def merge_by_sum(dict_a, dict_b):
    merged = {}
    for key in dict_a:
        merged[key] = dict_a[key] + dict_b[key]
    return merged


def plot_qwak2(
        x_value_matrix,
        y_value_matrix,
        x_label=None,
        y_label=None,
        plot_title=None,
        legend_labels=None,
        legend_title=None,
        legend_ncol=3,
        legend_loc='best',
        save_path=None,
        font_size=16,
        figsize=(12, 8),
        color_list=None,
        line_style_list=None,
        use_loglog=False,
        use_cbar=False,
        cbar_label=None,
        cbar_ticks_generator=None,
        cbar_num_ticks=3,
        cbar_tick_labels=['a', 'b', 'c'],
        x_num_ticks=None,
        y_num_ticks=None,
        x_round_val=3,
        y_round_val=3,
        v_line_values=None,
        v_line_style='--',
        v_line_list_index=None,
        v_line_colors=None,
        x_lim=None,
        use_grid=False,
        marker_list=None,  # Add marker_list parameter
        marker_interval=50,  # Add marker_interval parameter
        **kwargs):

    x_label = kwargs.get('x_label', x_label)
    y_label = kwargs.get('y_label', y_label)
    plot_title = kwargs.get('plot_title', plot_title)
    legend_labels = kwargs.get('legend_labels', legend_labels)
    legend_title = kwargs.get('legend_title', legend_title)
    legend_ncol = kwargs.get('legend_ncol', legend_ncol)
    legend_loc = kwargs.get('legend_loc', legend_loc)
    save_path = kwargs.get('save_path', save_path)
    font_size = kwargs.get('font_size', font_size)
    figsize = kwargs.get('figsize', figsize)
    color_list = kwargs.get('color_list', color_list)
    line_style_list = kwargs.get('line_style_list', line_style_list)
    use_loglog = kwargs.get('use_loglog', use_loglog)
    use_cbar = kwargs.get('use_cbar', use_cbar)
    cbar_label = kwargs.get('cbar_label', cbar_label)
    cbar_ticks_generator = kwargs.get(
        'cbar_ticks', cbar_ticks_generator)
    cbar_num_ticks = kwargs.get('cbar_num_ticks', cbar_num_ticks)
    cbar_tick_labels = kwargs.get('cbar_tick_labels', cbar_tick_labels)
    x_num_ticks = kwargs.get('x_num_ticks', x_num_ticks)
    y_num_ticks = kwargs.get('y_num_ticks', y_num_ticks)
    x_round_val = kwargs.get('x_round_val', x_round_val)
    y_round_val = kwargs.get('y_round_val', y_round_val)
    v_line_values = kwargs.get('v_line_values', v_line_values)
    v_line_style = kwargs.get('v_line_style', v_line_style)
    x_lim = kwargs.get('x_lim', x_lim)
    v_line_list_index = kwargs.get(
        'v_line_list_index', v_line_list_index)
    use_grid = kwargs.get('use_grid', use_grid)
    marker_list = kwargs.get('marker_list', marker_list)
    marker_interval = kwargs.get('marker_interval', marker_interval)

    if not isinstance(
            x_value_matrix[0],
            list) and not isinstance(
            x_value_matrix[0],
            np.ndarray):
        x_value_matrix = [x_value_matrix]
    if not isinstance(
            y_value_matrix[0],
            list) and not isinstance(
            y_value_matrix[0],
            np.ndarray):
        y_value_matrix = [y_value_matrix]

    if v_line_list_index is not None and v_line_values is None:
        raise ValueError(
            "v_line_list_index is provided, but v_line_values is None.")

    fig, ax = plt.subplots(figsize=figsize)
    if use_loglog:
        ax.loglog()
    if use_grid:
        ax.grid(True)
    axis_matrix_counter = 0
    color_matrix_counter = 0
    for xvalues, yvalues in zip(x_value_matrix, y_value_matrix):
        color = None
        line_style = None
        label = None
        marker = None  # Initialize marker variable
        if color_list is not None:
            color = color_list[axis_matrix_counter]
        if line_style_list is not None:
            line_style = line_style_list[axis_matrix_counter]
        if legend_labels is not None:
            label = legend_labels[axis_matrix_counter]
        if marker_list is not None:
            # Assign marker from list
            marker = marker_list[axis_matrix_counter]
        ax.plot(
            xvalues,
            yvalues,
            label=label,
            color=color,
            linestyle=line_style,
            marker=marker,
            markevery=marker_interval)  # Add marker to plot with interval
        if v_line_values is not None and axis_matrix_counter == v_line_list_index:
            if v_line_colors is None:
                v_line_colors = ['k'] * len(v_line_values)
            ax.axvline(
                x=v_line_values[color_matrix_counter][0],
                ymin=0,
                ymax=v_line_values[color_matrix_counter][1] /
                ax.get_ylim()[1],
                color=v_line_colors[color_matrix_counter],
                linestyle=v_line_style,
                linewidth=1.5)
            color_matrix_counter += 1
        elif v_line_values is not None and v_line_list_index is None:
            ax.axvline(
                x=v_line_values[axis_matrix_counter][0],
                ymin=0,
                ymax=v_line_values[axis_matrix_counter][1] /
                ax.get_ylim()[1],
                color=color,
                linestyle=v_line_style,
                linewidth=1.5)
        axis_matrix_counter += 1

    if x_label is not None:
        ax.set_xlabel(x_label, fontsize=font_size + 4)
    if y_label is not None:
        ax.set_ylabel(y_label, fontsize=font_size + 4)

    if plot_title is not None:
        ax.set_title(plot_title, fontsize=font_size + 6)

    if legend_labels is not None:
        legend = ax.legend(
            loc=legend_loc,
            ncol=legend_ncol,
            fontsize=font_size)
        if legend_title is not None:
            legend.set_title(legend_title, prop={'size': font_size + 2})

    ax.tick_params(axis='both', labelsize=font_size + 2)
    min_x_value_matrix = np.min(x_value_matrix)
    max_x_value_matrix = np.max(x_value_matrix)
    min_y_value_matrix = np.min(y_value_matrix)
    max_y_value_matrix = np.max(y_value_matrix)

    if x_num_ticks is not None:
        num_x_ticks = min(x_num_ticks, len(x_value_matrix[0]))
        x_tick_labels = np.round(
            np.linspace(
                min_x_value_matrix,
                max_x_value_matrix,
                num_x_ticks),
            x_round_val)
        ax.set_xticks(
            np.linspace(
                min_x_value_matrix,
                max_x_value_matrix,
                num_x_ticks))
        ax.set_xticklabels(x_tick_labels)

    if y_num_ticks is not None:
        num_y_ticks = min(y_num_ticks, len(y_value_matrix[0]))
        y_tick_labels = np.round(
            np.linspace(
                min_y_value_matrix,
                max_y_value_matrix,
                num_y_ticks),
            y_round_val)
        ax.set_yticks(
            np.linspace(
                min_y_value_matrix,
                max_y_value_matrix,
                num_y_ticks))
        ax.set_yticklabels(y_tick_labels)

    if use_cbar:
        if cbar_ticks_generator is None:
            cbar_ticks = np.linspace(
                min_y_value_matrix,
                max_y_value_matrix,
                cbar_num_ticks)
        else:
            cbar_ticks = cbar_ticks_generator
        colors = color_list
        cmap = LinearSegmentedColormap.from_list(
            'custom_cmap', colors, N=len(colors))
        norm = Normalize(vmin=cbar_ticks[0], vmax=cbar_ticks[-1])

        cbar = plt.colorbar(
            plt.cm.ScalarMappable(
                norm=norm,
                cmap=cmap),
            ax=ax,
            ticks=cbar_ticks)
        if cbar_label is not None:
            cbar.set_label(cbar_label, fontsize=font_size + 2)
        cbar.ax.tick_params(labelsize=font_size)

    if cbar_tick_labels is not None:
        cbar.ax.set_yticklabels(cbar_tick_labels)

    if x_lim is not None:
        ax.set_xlim(x_lim)

    if save_path is not None:
        plt.savefig(save_path, bbox_inches='tight')
        plt.show()
    else:
        plt.show()


nMin = 3
nMax = 1000
n_values = list(range(nMin, nMax, 1))
pVal = 0.8
sample_range = range(0, 100, 1)
seed = 10

SCRIPT_DIR = os.getcwd()

path = os.path.normpath(os.path.join(
    SCRIPT_DIR,
    "benchmark/ModuleDev/Profiling/operator_results"
))

# Operator Benchmark

results_init_avg = load_profiling_averages(
    path=path,
    method_name="init_operator",
    nrange=n_values,
    seed=seed
)

results_build_avg = load_profiling_averages(
    path=path,
    method_name="build_operator",
    nrange=n_values,
    seed=seed
)

results_expm_avg = load_profiling_averages(
    path=path,
    method_name="build_expm_operator",
    nrange=n_values,
    seed=seed
)

init_build_merged_result = merge_by_sum(
    results_init_avg, results_build_avg)

params = {
    'figsize': (12, 8),
    'plot_title': 'Spectral Decomposition vs Matrix Exponential',
    'x_label': 'Graph Size (N)',
    'y_label': 'Execution Time (seconds)',
    'legend_labels': ['Spectral Decomposition', 'Matrix Exponential'],
    'legend_loc': 'best',
    'legend_ncol': 1,
    'color_list': ['b', 'g'],
    'line_style_list': ['--', '-'],
    'save_path': os.path.normpath(os.path.join(
        SCRIPT_DIR,
        "benchmark/ModuleDev/ImgOutput/benchmark-operator.png"
    )),
    'use_loglog': False,
    'use_cbar': False,
    'cbar_label': None,
    'cbar_ticks': None,
    'cbar_tick_labels': None,
    'x_lim': None,
    'y_num_ticks': 5,
    'y_round_val': 3,
    'title_font_size': 34,
    'xlabel_font_size': 28,
    'ylabel_font_size': 28,
    'legend_font_size': 24,
    'legend_title_font_size': 26,
    'tick_font_size': 24,
    'marker_list': ['x', 'o'],  # Add markers for data points
    'marker_interval': 50,  # Set marker interval
    'use_grid': True  # Ensure grid is enabled
}

x_value_matrix = [
    list(
        init_build_merged_result.keys()), list(
            results_expm_avg.keys())]
y_value_matrix = [
    list(
        init_build_merged_result.values()), list(
            results_expm_avg.values())]

plot_qwak2(
    x_value_matrix=x_value_matrix,
    y_value_matrix=y_value_matrix,
    **params)

plt.grid(True)  # Explicitly enable gridlines
plt.show()

copy_to_latex = input(
    "Do you want to copy the generated image to the LaTeX project? (y/n): ").strip().lower()
if copy_to_latex == 'y':
    latex_project_path = os.path.normpath(os.path.join(
        SCRIPT_DIR,
        "../QWAK-Paper_Revised/img/NewBenchmark"
    ))
    shutil.copy(params['save_path'], latex_project_path)
    print(f"Image copied to {latex_project_path}")
else:
    print("Image not copied.")
