import numpy as np
import matplotlib as mpl
from matplotlib import pyplot as plt
from qwak.qwak import QWAK
from qwak.Errors import EmptyProbDistList
from matplotlib.colors import LinearSegmentedColormap, BoundaryNorm, Normalize


def plot_data(x_value_matrix, y_value_matrix, x_label=None, y_label=None, title=None, legend_labels=None,
              legend_title=None,
              legend_ncol=3,
              legend_loc='best',
              save_path=None, font_size=12, figsize=(10, 6), color_list=None, line_style_list=None,
              use_loglog=False, use_cbar=False, cbar_label=None, cbar_ticks_generator=None, cbar_num_ticks=3,
              cbar_tick_labels=['a', 'b', 'c'],
              x_num_ticks=None, y_num_ticks=None, x_round_val=3, y_round_val=3, v_line_values=None, v_line_style='--',
              x_lim=None, **kwargs):

    # Unpack optional parameters
    x_label = kwargs.get('x_label', x_label)
    y_label = kwargs.get('y_label', y_label)
    title = kwargs.get('title', title)
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
    cbar_ticks_generator = kwargs.get('cbar_ticks', cbar_ticks_generator)
    cbar_num_ticks = kwargs.get('cbar_num_ticks', cbar_num_ticks)
    cbar_tick_labels = kwargs.get('cbar_tick_labels', cbar_tick_labels)
    x_num_ticks = kwargs.get('x_num_ticks', x_num_ticks)
    y_num_ticks = kwargs.get('y_num_ticks', y_num_ticks)
    x_round_val = kwargs.get('x_round_val', x_round_val)
    y_round_val = kwargs.get('y_round_val', y_round_val)
    v_line_values = kwargs.get('v_line_values', v_line_values)
    v_line_style = kwargs.get('v_line_style', v_line_style)
    x_lim = kwargs.get('x_lim', x_lim)

    #test if x_value_matrix and y_value_matrix are lists of lists, seperately, and if not make them into lists of lists

    if not isinstance(x_value_matrix[0], list) and not isinstance(x_value_matrix[0],np.ndarray):
        x_value_matrix = [x_value_matrix]
        print('hi1')
    if not isinstance(y_value_matrix[0], list) and not isinstance(y_value_matrix[0],np.ndarray):
        y_value_matrix = [y_value_matrix]
        print('hi2')

    # plot the data for each row of the data matrix
    fig, ax = plt.subplots(figsize=figsize)
    if use_loglog:
        ax.loglog()
    # ax.set_xlim([x_values[0], x_values[-1]])
    i = 0
    for xvalues, yvalues in zip(x_value_matrix, y_value_matrix):
        color = None
        line_style = None
        label = None
        if color_list is not None:
            color = color_list[i]
        if line_style_list is not None:
            line_style = line_style_list[i]
        if legend_labels is not None:
            label = legend_labels[i]
        ax.plot(xvalues, yvalues, label=label,
                color=color, linestyle=line_style)
        if v_line_values is not None:
            ax.axvline(x=v_line_values[i][0], ymin=0, ymax=v_line_values[i][1] / ax.get_ylim()[1], color=color,
                       linestyle=v_line_style, linewidth=1.5)
        i += 1

    # set the axis labels
    if x_label is not None:
        ax.set_xlabel(x_label, fontsize=font_size + 2)
    if y_label is not None:
        ax.set_ylabel(y_label, fontsize=font_size + 2)

    # set the plot title
    if title is not None:
        ax.set_title(title, fontsize=font_size + 4)

    # set the legend
    if legend_labels is not None:
        legend = ax.legend(loc=legend_loc, ncol=legend_ncol, fontsize=font_size - 1)
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
        x_tick_labels = np.round(np.linspace(min_x_value_matrix, max_x_value_matrix, num_x_ticks), x_round_val)
        ax.set_xticks(np.linspace(min_x_value_matrix, max_x_value_matrix, num_x_ticks))
        ax.set_xticklabels(x_tick_labels)

    if y_num_ticks is not None:
        num_y_ticks = min(y_num_ticks, len(y_value_matrix[1]))
        y_tick_labels = np.round(np.linspace(min_y_value_matrix, max_y_value_matrix, num_y_ticks), y_round_val)
        ax.set_yticks(np.linspace(min_y_value_matrix, max_y_value_matrix, num_y_ticks))
        ax.set_yticklabels(y_tick_labels)

    # add colorbar
    if use_cbar:
        if cbar_ticks_generator is None:
            cbar_ticks = np.linspace(min_y_value_matrix, max_y_value_matrix, cbar_num_ticks)
        else:
            cbar_ticks = cbar_ticks_generator
        colors = color_list
        cmap = LinearSegmentedColormap.from_list('custom_cmap', colors, N=len(colors))
        # norm = BoundaryNorm(cbar_ticks, len(cbar_ticks)-1)
        norm = Normalize(vmin=cbar_ticks[0], vmax=cbar_ticks[-1])

        cbar = plt.colorbar(plt.cm.ScalarMappable(norm=norm, cmap=cmap), ax=ax, ticks=cbar_ticks)
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

def searchProbStepsPlotting(qwak: QWAK):
    """Plots the probability of finding the target as a function of the number of steps.

    Parameters
    ----------
    qwak : QWAK
        QWAK object containing the results of the simulation.
    """
    markedProbability = 0
    markedProbDistList = []
    markdElements = qwak.getMarkedElements()
    probDistList  = qwak.getProbDistList()
    if probDistList == []:
        raise EmptyProbDistList("The probability distribution list is empty.")
    for probDist in probDistList:
        for element in markdElements:
            markedProbability += probDist.searchNodeProbability(element[0])
        markedProbDistList.append(markedProbability)
        markedProbability = 0
    return markedProbDistList

def searchProbStepsPlotting2(qwak: QWAK,probDistList):
    """Plots the probability of finding the target as a function of the number of steps.

    Parameters
    ----------
    qwak : QWAK
        QWAK object containing the results of the simulation.
    """
    markedProbability = 0
    markedProbDistList = []
    markdElements = qwak.getMarkedElements()
    probDistList  = probDistList
    if probDistList == []:
        raise EmptyProbDistList("The probability distribution list is empty.")
    for probDist in probDistList:
        for element in markdElements:
            markedProbability += probDist.searchNodeProbability(element[0])
        markedProbDistList.append(markedProbability)
        markedProbability = 0
    # print(markedProbDistList)
    return markedProbDistList