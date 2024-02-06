import numpy as np
from matplotlib import pyplot as plt
import math
import copy
import os
import seaborn as sns
import pandas as pd
from matplotlib.colors import LinearSegmentedColormap, Normalize


def plot_qwak(
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
        font_size=12,
        figsize=(10, 6),
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
        **kwargs):
    """
    Plots data from a matrix of x values and a matrix of y values.
    Note that all parameters can be passed via a dictionary using the **kwargs syntax.

    Parameters
    ----------
    x_value_matrix : array_like
        A matrix of x values. Each row is a set of x values for a single line.
    y_value_matrix : array_like
        A matrix of y values. Each row is a set of y values for a single line.
    x_label : str, optional
        The label for the x-axis. The default is None.
    y_label : str, optional
        The label for the y-axis. The default is None.
    plot_title : str, optional
        The title of the plot. The default is None.
    legend_labels : list, optional
        A list of strings to be used as labels for the legend. The default is None.
    legend_title : str, optional
        The title of the legend. The default is None.
    legend_ncol : int, optional
        The number of columns in the legend. The default is 3.
    legend_loc : str, optional
        The location of the legend. The default is 'best'.
    save_path : str, optional
        The path to save the plot to. The default is None.
    font_size : int, optional
        The font size of the plot. The default is 12.
    figsize : tuple, optional
        The size of the figure. The default is (10,6).
    color_list : list, optional
        A list of colors to be used for the lines. The default is None.
    line_style_list : list, optional
        A list of line styles to be used for the lines. The default is None.
    use_loglog : bool, optional
        Whether to use a log-log plot. The default is False.
    use_cbar : bool, optional
        Whether to use a colorbar. The default is False.
    cbar_label : str, optional
        The label for the colorbar. The default is None.
    cbar_ticks_generator : function, optional
        A function that generates the ticks for the colorbar. The default is None.
    cbar_num_ticks : int, optional
        The number of ticks for the colorbar. The default is 3.
    cbar_tick_labels : list, optional
        A list of strings to be used as labels for the colorbar ticks. The default is ['a','b','c'].
    x_num_ticks : int, optional
        The number of ticks for the x-axis. The default is None.
    y_num_ticks : int, optional
        The number of ticks for the y-axis. The default is None.
    x_round_val : int, optional
        The number of decimal places to round the x-axis ticks to. The default is 3.
    y_round_val : int, optional
        The number of decimal places to round the y-axis ticks to. The default is 3.
    v_line_values : list, optional
        A list of values to plot vertical lines at. The default is None.
    v_line_style : str, optional
        The style of the vertical lines. The default is '--'.
    v_line_list_index : int, optional
        The index of the line to plot the vertical lines on. The default is None.
    v_line_colors : list, optional
        A list of colors to be used for the vertical lines. The default is None.
    x_lim : tuple, optional
        The limits of the x-axis. The default is None.
    """

    # Unpack optional parameters
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
    axis_matrix_counter = 0
    color_matrix_counter = 0
    for xvalues, yvalues in zip(x_value_matrix, y_value_matrix):
        color = None
        line_style = None
        label = None
        if color_list is not None:
            color = color_list[axis_matrix_counter]
        if line_style_list is not None:
            line_style = line_style_list[axis_matrix_counter]
        if legend_labels is not None:
            label = legend_labels[axis_matrix_counter]
        ax.plot(xvalues, yvalues, label=label,
                color=color, linestyle=line_style)
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

    # set the axis labels
    if x_label is not None:
        ax.set_xlabel(x_label, fontsize=font_size + 2)
    if y_label is not None:
        ax.set_ylabel(y_label, fontsize=font_size + 2)

    # set the plot plot_title
    if plot_title is not None:
        ax.set_title(plot_title, fontsize=font_size + 4)

    # set the legend
    if legend_labels is not None:
        legend = ax.legend(
            loc=legend_loc,
            ncol=legend_ncol,
            fontsize=font_size - 1)
        if legend_title is not None:
            legend.set_title(legend_title, prop={'size': font_size - 1})

    # set font size for ticks
    ax.tick_params(axis='both', labelsize=font_size)
    min_x_value_matrix = np.min(x_value_matrix)
    max_x_value_matrix = np.max(x_value_matrix)
    min_y_value_matrix = np.min(y_value_matrix)
    max_y_value_matrix = np.max(y_value_matrix)

    # set tick labels
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

    # add colorbar
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
        # norm = BoundaryNorm(cbar_ticks, len(cbar_ticks)-1)
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
        figsize=(8, 6),
        cmap='coolwarm',
        x_vline_value=None,
        y_hline_value=None,
        **kwargs):
    """
    Plot a heatmap of the probability of a given p and t value.

    Parameters
    ----------
    p_values : list of lists
        List of lists of p values.
    t_values : list of lists
        List of lists of t values.
    prob_values : list of lists
        List of lists of probability values.
    x_num_ticks : int, optional
        Number of x-axis ticks. The default is 5.
    y_num_ticks : int, optional
        Number of y-axis ticks. The default is 5.
    x_round_val : int, optional
        Number of decimal places to round x-axis tick labels. The default is 3.
    y_round_val : int, optional
        Number of decimal places to round y-axis tick labels. The default is 3.
    filepath : str, optional
        Path to save the plot. The default is None.
    N : int, optional
        Number of samples. The default is None.
    xlabel : str, optional
        Label for the x-axis. The default is None.
    ylabel : str, optional
        Label for the y-axis. The default is None.
    cbar_label : str, optional
        Label for the colorbar. The default is None.
    font_size : int, optional
        Font size for the plot. The default is 12.
    figsize : tuple, optional
        Size of the plot. The default is (8, 6).
    cmap : str, optional
        Colormap for the plot. The default is 'coolwarm'.
    x_vline_value : float, optional
        Value to draw a vertical line at. The default is None.
    y_hline_value : float, optional
        Value to draw a horizontal line at. The default is None.
    """
    # Get parameters from kwargs with their default values
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
    figsize = kwargs.get('figsize', figsize)
    cmap = kwargs.get('cmap', cmap)
    x_vline_value = kwargs.get('x_vline_value', x_vline_value)
    y_hline_value = kwargs.get('y_hline_value', y_hline_value)

    flat_p = [item for sublist in p_values for item in sublist]
    flat_t = [item for sublist in t_values for item in sublist]
    flat_prob = [item for sublist in prob_values for item in sublist]
    data = {'p': flat_p, 't': flat_t, 'prob': flat_prob}
    df = pd.DataFrame(data)
    pivot = df.pivot('t', 'p', 'prob')

    fig, ax = plt.subplots(figsize=figsize)
    sns.heatmap(
        pivot,
        cmap=cmap,
        vmin=0,
        vmax=1,
        cbar_kws={
            'label': cbar_label},
        linewidths=0,
        **kwargs)

    # set customizations
    ax.invert_yaxis()
    ax.tick_params(axis='both', which='major', labelsize=font_size)
    cbar = ax.collections[0].colorbar
    cbar.ax.tick_params(labelsize=font_size)
    cbar.ax.set_ylabel(cbar_label, fontsize=font_size + 2)

    # generate tick labels based on p and t values
    num_p_ticks = min(x_num_ticks, len(p_values[0]))
    num_t_ticks = min(y_num_ticks, len(t_values[0]))
    p_tick_labels = np.round(
        np.linspace(
            100 * min(flat_p),
            100 * max(flat_p),
            num_p_ticks),
        x_round_val)
    t_tick_labels = np.round(
        np.linspace(
            min(flat_t),
            max(flat_t),
            num_t_ticks),
        y_round_val)

    # set x and y tick labels
    ax.set_xticks(np.linspace(0, len(p_values[0]), num_p_ticks))
    ax.set_yticks(np.linspace(0, len(t_values[0]), num_t_ticks))
    ax.set_xticklabels(p_tick_labels, rotation=0)
    ax.set_yticklabels(t_tick_labels)
    if x_vline_value is not None:
        x_tick_value = (x_vline_value - min(flat_p)) / \
            (max(flat_p) - min(flat_p)) * len(p_values[0])
        ax.axvline(
            x=x_tick_value,
            linestyle=':',
            marker='D',
            markersize=5,
            linewidth=1,
            color='white')
    if y_hline_value is not None:
        y_tick_value = (y_hline_value - min(flat_t)) / \
            (max(flat_t) - min(flat_t)) * len(t_values[0])
        ax.axhline(
            y=y_tick_value,
            linestyle=':',
            marker='D',
            markersize=5,
            linewidth=1,
            color='white')

    # add title to the plot if N is provided
    if N is not None:
        plt.title(f'N={N}', fontsize=font_size + 4)

    # add x and y axis labels
    if xlabel is not None:
        ax.set_xlabel(xlabel, fontsize=font_size + 2)
    if ylabel is not None:
        ax.set_ylabel(ylabel, fontsize=font_size + 2)

    if filepath is not None:
        plt.savefig(filepath, bbox_inches='tight')
        plt.show()
    else:
        plt.show()
