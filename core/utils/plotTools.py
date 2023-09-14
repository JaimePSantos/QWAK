import numpy as np
from matplotlib import pyplot as plt
import math
import copy
import os
import seaborn as sns
import pandas as pd
from matplotlib.colors import LinearSegmentedColormap, Normalize,ListedColormap


def plot_qwak(x_value_matrix, y_value_matrix, **kwargs):
    # Unpack optional parameters from kwargs with default values
    x_label = kwargs.get('x_label', None)
    y_label = kwargs.get('y_label', None)
    plot_title = kwargs.get('plot_title', None)
    legend_labels = kwargs.get('legend_labels', None)
    legend_title = kwargs.get('legend_title', None)
    legend_ncol = kwargs.get('legend_ncol', 3)
    legend_loc = kwargs.get('legend_loc', 'best')
    save_path = kwargs.get('save_path', None)
    font_size = kwargs.get('font_size', 12)
    figsize = kwargs.get('figsize', (10, 6))
    color_list = kwargs.get('color_list', None)
    line_style_list = kwargs.get('line_style_list', None)
    use_loglog = kwargs.get('use_loglog', False)
    use_cbar = kwargs.get('use_cbar', False)
    cbar_label = kwargs.get('cbar_label', None)
    cbar_ticks_generator = kwargs.get('cbar_ticks', None)
    cbar_num_ticks = kwargs.get('cbar_num_ticks', 3)
    cbar_tick_labels = kwargs.get('cbar_tick_labels', ['a', 'b', 'c'])
    x_num_ticks = kwargs.get('x_num_ticks', None)
    y_num_ticks = kwargs.get('y_num_ticks', None)
    x_round_val = kwargs.get('x_round_val', 3)
    y_round_val = kwargs.get('y_round_val', 3)
    v_line_values = kwargs.get('v_line_values', None)
    v_line_colors = kwargs.get('v_line_colors', None)
    v_line_style = kwargs.get('v_line_style', '--')
    x_lim = kwargs.get('x_lim', None)
    v_line_list_index = kwargs.get('v_line_list_index', None)
    use_grid = kwargs.get('use_grid', False)
    marker_list = kwargs.get('marker_list', None)
    cbar_ticks = kwargs.get('cbar_ticks', None)
    title_font_size = kwargs.get('title_font_size', None)
    xlabel_font_size = kwargs.get('xlabel_font_size', None)
    ylabel_font_size = kwargs.get('ylabel_font_size', None)
    legend_font_size = kwargs.get('legend_font_size', None)
    legend_title_font_size = kwargs.get('legend_title_font_size', None)
    tick_font_size = kwargs.get('tick_font_size', None)
    cbar_label_font_size = kwargs.get('cbar_label_font_size', None)
    use_grid = kwargs.get('use_grid', False)
    marker_list = kwargs.get('use_grid', None)
    
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

    # plot the data for each row of the data matrix
    fig, ax = plt.subplots(figsize=figsize)
    if use_loglog:
        ax.loglog()
    if use_grid:
        ax.grid(True)

    axis_matrix_counter = 0
    color_matrix_counter = 0
    marker = None
    for xvalues, yvalues in zip(x_value_matrix, y_value_matrix):
        color = None
        line_style = None
        label = None
        if color_list is not None:
            color = color_list[axis_matrix_counter]
        if line_style_list is not None:
            line_style = line_style_list[axis_matrix_counter]
        if marker_list is not None:
            marker = marker_list[axis_matrix_counter] 
        if legend_labels is not None:
            label = legend_labels[axis_matrix_counter]
        ax.plot(xvalues, yvalues, label=label,
                color=color, linestyle=line_style, marker=marker)
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
        ax.set_xlabel(x_label, fontsize=xlabel_font_size if xlabel_font_size else font_size + 2)
    if y_label is not None:
        ax.set_ylabel(y_label, fontsize=ylabel_font_size if ylabel_font_size else font_size + 2)

    # set the plot title
    if plot_title is not None:
        ax.set_title(plot_title, fontsize=title_font_size if title_font_size else font_size + 4)

    # set the legend
    if legend_labels is not None:
        legend = ax.legend(
            loc=legend_loc,
            ncol=legend_ncol,
            fontsize=legend_font_size if legend_font_size else font_size - 1)
        if legend_title is not None:
            legend.set_title(legend_title, prop={'size': legend_title_font_size if legend_title_font_size else font_size - 1})

    # set font size for ticks
    ax.tick_params(axis='both', labelsize=tick_font_size if tick_font_size else font_size)

    # add colorbar
    if use_cbar:
        custom_cmap = ListedColormap(color_list)
        norm = Normalize(vmin=0, vmax=len(color_list) - 1)  # Adjust the normalization based on the number of colors
        cbar = plt.colorbar(
            plt.cm.ScalarMappable(
                norm=norm,
                cmap=custom_cmap),
            ax=ax,
        ticks=np.linspace(0, len(color_list) - 1, cbar_num_ticks))  # Set fewer ticks
        if cbar_label is not None:
            cbar.set_label(cbar_label, fontsize=cbar_label_font_size if cbar_label_font_size else font_size + 2)
        if cbar_tick_labels is not None:
            cbar.set_ticklabels(cbar_tick_labels)  # Set custom labels
        cbar.ax.tick_params(labelsize=tick_font_size if tick_font_size else font_size)


    if x_lim is not None:
        ax.set_xlim(x_lim)

    # save or show the plot
    if save_path is not None:
        plt.savefig(save_path)
        plt.show()
    else:
        plt.show()


def plot_qwak_heatmap(
        p_values,
        t_values,
        prob_values,
        x_num_ticks=5,
        y_num_ticks=5,
        x_round_val=3,
        y_round_val=3,
        filepath=None,
        N=None,
        xlabel=None,
        ylabel=None,
        cbar_label=None,
        font_size=12,
        cmap='coolwarm',
        x_vline_value=None,
        y_hline_value=None,
        **kwargs):
    # Get parameters from kwargs with their default values
    figsize = kwargs.pop('figsize', (8, 6))
    x_num_ticks = kwargs.get('x_num_ticks', x_num_ticks)
    y_num_ticks = kwargs.get('y_num_ticks', y_num_ticks)
    x_round_val = kwargs.get('x_round_val', x_round_val)
    y_round_val = kwargs.get('y_round_val', y_round_val)
    filepath = kwargs.get('filepath', filepath)
    N = kwargs.get('N', N)
    xlabel = kwargs.get('xlabel', xlabel)
    ylabel = kwargs.get('ylabel', ylabel)
    cbar_label = kwargs.get('cbar_label', cbar_label)
    font_size = kwargs.get('font_size', font_size)
    cmap = kwargs.get('cmap', cmap)
    x_vline_value = kwargs.get('x_vline_value', x_vline_value)
    y_hline_value = kwargs.get('y_hline_value', y_hline_value)
    title_font_size = kwargs.pop('title_font_size', 20)
    xlabel_font_size = kwargs.pop('xlabel_font_size', 22)
    ylabel_font_size = kwargs.pop('ylabel_font_size', 22)
    legend_font_size = kwargs.pop('legend_font_size', 14)
    legend_title_font_size = kwargs.pop('legend_title_font_size', 14)
    tick_font_size = kwargs.pop('tick_font_size', 18)


    flat_p = [item for sublist in p_values for item in sublist]
    flat_t = [item for sublist in t_values for item in sublist]
    flat_prob = [item for sublist in prob_values for item in sublist]
    data = {'p': flat_p, 't': flat_t, 'prob': flat_prob}
    df = pd.DataFrame(data)
    pivot = df.pivot('t', 'p', 'prob')

    fig, ax = plt.subplots(figsize=figsize)
    sns.heatmap(pivot, cmap=cmap, vmin=0, vmax=1, cbar_kws={'label': cbar_label}, linewidths=0, **kwargs)
    if N is not None:
        plt.title(f'N={N}', fontsize=title_font_size)

    # add x and y axis labels
    if xlabel is not None:
        ax.set_xlabel(xlabel, fontsize=xlabel_font_size)
    if ylabel is not None:
        ax.set_ylabel(ylabel, fontsize=ylabel_font_size)
    # set customizations
    ax.invert_yaxis()
    ax.tick_params(axis='both', which='major', labelsize=tick_font_size)
    
    cbar = ax.collections[0].colorbar
    cbar.ax.tick_params(labelsize=legend_font_size)
    cbar.ax.set_ylabel(cbar_label, fontsize=legend_title_font_size)

    # generate tick labels based on p and t values
    num_p_ticks = min(x_num_ticks, len(p_values[0]))
    num_t_ticks = min(y_num_ticks, len(t_values[0])) - 1  # -1 to exclude 0 for y-axis
    p_tick_labels = np.round(np.linspace(100 * min(flat_p), 100 * max(flat_p), num_p_ticks), x_round_val)
    t_tick_labels = np.round(np.linspace(min(flat_t), max(flat_t), num_t_ticks + 1)[1:], y_round_val)  # [1:] to exclude 0 for y-axis

    # set x and y tick labels
    ax.set_xticks(np.linspace(0, len(p_values[0]), num_p_ticks))  # Include 0 for x-axis
    ax.set_yticks(np.linspace(0, len(t_values[0]), num_t_ticks + 1)[1:])  # [1:] to exclude 0 for y-axis
    ax.set_xticklabels(p_tick_labels, rotation=0)
    ax.set_yticklabels(t_tick_labels)

    
    if x_vline_value is not None:
        x_tick_value = (x_vline_value - min(flat_p)) / (max(flat_p) - min(flat_p)) * len(p_values[0])
        ax.axvline(x=x_tick_value, linestyle=':',marker='D',markersize=5, linewidth=1, color='white')
    if y_hline_value is not None:
        y_tick_value = (y_hline_value - min(flat_t)) / (max(flat_t) - min(flat_t)) * len(t_values[0])
        ax.axhline(y=y_tick_value, linestyle=':',marker='D',markersize=5, linewidth=1, color='white')

    if filepath is not None:
        plt.savefig(filepath, bbox_inches='tight')
        plt.show()
    else:
        plt.show()