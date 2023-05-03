from qwak.qwak import QWAK
import networkx as nx
import numpy as np
import matplotlib as mpl
from matplotlib import pyplot as plt
import scipy.special as sp
from scipy.linalg import expm
import sympy as simp
import os
from matplotlib.colors import ListedColormap, BoundaryNorm, LinearSegmentedColormap

def plot_decay_rate_matrix(decay_rate_matrix, time_list, alpha_list, alpha_label_list=None,
                           title=None, xlabel='Time', ylabel='Decay Rate', legend_loc='best',
                           save_path=None, font_size=12,figsize=(10,6),
                           color_list=None, line_style_list=None):

    # set default alpha labels
    if alpha_label_list is None:
        alpha_label_list = alpha_list

    # plot the decay rate for each alpha value
    fig, ax = plt.subplots(figsize=figsize)
    ax.loglog()
    ax.set_xlim([time_list[0], time_list[-1]])
    for i in range(len(alpha_list)):
        color = None
        line_style = None
        if color_list is not None:
            color = color_list[i]
        if line_style_list is not None:
            line_style = line_style_list[i]
        ax.plot(time_list, decay_rate_matrix[i], label=alpha_label_list[i], color=color, linestyle=line_style)

    # set the axis labels
    ax.set_xlabel(xlabel, fontsize=font_size+2)
    ax.set_ylabel(ylabel, fontsize=font_size+2)

    # set the plot title
    if title is not None:
        ax.set_title(title, fontsize=font_size+4)

    # set the legend
    legend =ax.legend(loc=legend_loc,ncol=len(alpha_list), fontsize=font_size-1)
    legend.set_title(r'$\alpha$', prop={'size': font_size - 1})

    # set font size for ticks
    ax.tick_params(axis='both', labelsize=font_size)
    fig.tight_layout()

    # save or show the plot
    if save_path is not None:
        plt.savefig(save_path)
        plt.show()
    else:
        plt.show()

def plot_search_complete(markedList, probT, tSpace, configVec, x_num_ticks=5, y_num_ticks=5, x_round_val=3, y_round_val=3, filepath=None,
                xlabel='Number of steps', ylabel='Probability of marked elements', cbar_label='Gamma', font_size=12, figsize=(8, 6),
                cbar_num_ticks=None, cbar_tick_labels=None, plot_title='Hypercube Search'):

    fig, ax = plt.subplots(figsize=figsize)

    for i, (T, walk, config, marked) in enumerate(zip(tSpace, probT, configVec, markedList)):
        max_prob = np.max(walk)
        max_prob_t = T[np.argmax(walk)]
        ax.plot(T, walk, color=config[0], linestyle=config[1], label=f'Solutions: {len(marked)}')
        ax.axvline(max_prob_t, color=config[0], linestyle='dashed', linewidth=1.5,
               ymax=max_prob/ax.get_ylim()[1])
        ax.set_xlabel(xlabel, fontsize=font_size + 2)
        ax.set_ylabel(ylabel, fontsize=font_size + 2)
        ax.set_title(plot_title, fontsize=font_size+4)

    ax.tick_params(axis='both', which='major', labelsize=font_size)

    num_t_ticks = min(y_num_ticks, len(tSpace[0]))
    t_tick_labels = np.round(np.linspace(min(tSpace[0]), max(tSpace[0]), num_t_ticks), y_round_val)

    ax.set_yticks(np.linspace(0, np.max(probT), num_t_ticks))
    ax.set_yticklabels(np.round(np.linspace(0, np.max(probT), num_t_ticks), y_round_val))

    num_x_ticks = min(x_num_ticks, len(tSpace[0]))
    x_tick_labels = np.round(np.linspace(min(tSpace[0]), max(tSpace[0]), num_x_ticks), x_round_val)

    ax.set_xticks(np.linspace(min(tSpace[0]), max(tSpace[0]), num_x_ticks))
    ax.set_xticklabels(x_tick_labels)

    ax.legend()

    if filepath is not None:
        plt.savefig(filepath, bbox_inches='tight')
        plt.show()
    else:
        plt.show()

def plot_search_hypercube(markedList, probT, tSpace, configVec, gamma_range, x_num_ticks=5, y_num_ticks=5, x_round_val=3, y_round_val=3, filepath=None,
                xlabel='Number of steps', ylabel='Probability of marked elements', cbar_label='Gamma', font_size=12, figsize=(8, 6),
                cbar_num_ticks=None, cbar_tick_labels=None, plot_title='Hypercube Search'):

    fig, ax = plt.subplots(figsize=figsize)

    max_prob = 0
    max_prob_t = 0

    for T, walk, config, marked in zip(tSpace, probT, configVec, markedList):
        ax.plot(T, walk, color=config[0], linestyle=config[1])
        ax.set_xlabel(xlabel, fontsize=font_size + 2)
        ax.set_ylabel(ylabel, fontsize=font_size + 2)
        ax.set_title(plot_title, fontsize=font_size+4)

        cur_max_prob = np.max(walk)
        if cur_max_prob > max_prob:
            max_prob = cur_max_prob
            max_prob_t = T[np.argmax(walk)]

    ax.tick_params(axis='both', which='major', labelsize=font_size)

    num_t_ticks = min(y_num_ticks, len(tSpace[0]))
    t_tick_labels = np.round(np.linspace(min(tSpace[0]), max(tSpace[0]), num_t_ticks), y_round_val)

    ax.set_yticks(np.linspace(0, max_prob, num_t_ticks))
    ax.set_yticklabels(np.round(np.linspace(0, max_prob, num_t_ticks), y_round_val))

    num_x_ticks = min(x_num_ticks, len(tSpace[0]))
    x_tick_labels = np.round(np.linspace(min(tSpace[0]), max(tSpace[0]), num_x_ticks), x_round_val)

    ax.set_xticks(np.linspace(min(tSpace[0]), max(tSpace[0]), num_x_ticks))
    ax.set_xticklabels(x_tick_labels)

    colors = [config[0] for config in configVec]
    cmap = LinearSegmentedColormap.from_list('custom_cmap', colors, N=len(colors))
    norm = BoundaryNorm(gamma_range, len(gamma_range)-1)

    if cbar_num_ticks is not None:
        cbar_ticks = np.linspace(gamma_range[0], gamma_range[-1], cbar_num_ticks)
    else:
        cbar_ticks = None

    cbar = plt.colorbar(plt.cm.ScalarMappable(norm=norm, cmap=cmap), ax=ax, ticks=cbar_ticks)
    cbar.set_label(cbar_label, fontsize=font_size + 2)
    cbar.ax.tick_params(labelsize=font_size)

    if cbar_tick_labels is not None:
        cbar.ax.set_yticklabels(cbar_tick_labels)

    ax.axvline(max_prob_t, color='black', linestyle='dashed', linewidth=1.5,
               ymax=max_prob/ax.get_ylim()[1])
    # ax.text(max_prob_t + 0.5, max_prob + 0.05, f'Max Prob = {max_prob:.{y_round_val}f}', fontsize=font_size)

    if filepath is not None:
        plt.savefig(filepath, bbox_inches='tight')
        plt.show()
    else:
        plt.show()

# create a general plotting functions with the functionality of the three functions above
def plot_search_complete_general(markedList, probT, tSpace, configVec, gamma_range, x_num_ticks=5, y_num_ticks=5, x_round_val=3, y_round_val=3, filepath=None,

                                 xlabel='Number of steps', ylabel='Probability of marked elements', cbar_label='Gamma', font_size=12, figsize=(8, 6),
                                 cbar_num_ticks=None, cbar_tick_labels=None, plot_title='Hypercube Search'):

    fig, ax = plt.subplots(figsize=figsize)

    for i, (T, walk, config, marked) in enumerate(zip(tSpace, probT, configVec, markedList)):
        max_prob = np.max(walk)
        max_prob_t = T[np.argmax(walk)]
        ax.plot(T, walk, color=config[0], linestyle=config[1], label=f'Solutions: {len(marked)}')
        ax.axvline(max_prob_t, color=config[0], linestyle='dashed', linewidth=1.5,
                   ymax=max_prob/ax.get_ylim()[1])
        ax.set_xlabel(xlabel, fontsize=font_size + 2)
        ax.set_ylabel(ylabel, fontsize=font_size + 2)
        ax.set_title(plot_title, fontsize=font_size+4)

    ax.tick_params(axis='both', which='major', labelsize=font_size)

    num_t_ticks = min(y_num_ticks, len(tSpace[0]))
    t_tick_labels = np.round(np.linspace(min(tSpace[0]), max(tSpace[0]), num_t_ticks), y_round_val)

    ax.set_yticks(np.linspace(0, np.max(probT), num_t_ticks))
    ax.set_yticklabels(np.round(np.linspace(0, np.max(probT), num_t_ticks), y_round_val))

    num_x_ticks = min(x_num_ticks, len(tSpace[0]))
    x_tick_labels = np.round(np.linspace(min(tSpace[0]), max(tSpace[0]), num_x_ticks), x_round_val)


    ax.set_xticks(np.linspace(min(tSpace[0]), max(tSpace[0]), num_x_ticks))
    ax.set_xticklabels(x_tick_labels)

    colors = [config[0] for config in configVec]
    cmap = LinearSegmentedColormap.from_list('custom_cmap', colors, N=len(colors))
    norm = BoundaryNorm(gamma_range, len(gamma_range)-1)

    if cbar_num_ticks is not None:
        cbar_ticks = np.linspace(gamma_range[0], gamma_range[-1], cbar_num_ticks)

    else:
        cbar_ticks = None

#create a function that prints all prime numbers within a range
def prime_numbers(start, end):
    for n in range(start, end + 1):
        if n > 1:
            for i in range(2, n):
                if (n % i) == 0:
                    break
            else:
                print(n)

prime_numbers(1, 100)

