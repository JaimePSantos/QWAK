import itertools
from qwak.qwak import QWAK
from utils.plotTools import plot_qwak

import networkx as nx
import numpy as np
import matplotlib as mpl
from matplotlib import pyplot as plt
from math import sqrt, ceil, pow
import scipy.special as sp
import sympy as simp
import math
import copy
import seaborn as sns
import matplotlib.pyplot as plt
import pandas as pd
import os
import json
import shutil

from scipy.ndimage import gaussian_filter

SCRIPT_DIR = os.getcwd()


def load_pst(filename):
    # Check if the file exists
    if os.path.exists(filename):
        # If the file exists, load the data from the file
        with open(filename, 'r') as file:
            pst_data = json.load(file)
        print(f'{filename} exists!')
    else:
        # If the file does not exist, generate the data
        print(f'{filename} doesnt exist!')
        pst_data = []
    # Return the data
    return pst_data


def pst_found_only(input_dict):
    # Create a new dictionary by filtering out key-value pairs where the value is equal to '-1'
    # Note: assuming the values in the dictionary are stored as strings,
    # as in the previous examples
    filtered_dict = {
        key: value for key,
        value in input_dict.items() if value != '-1'}
    if not filtered_dict:
        return ['PST not found for this structure!']

    # Return the filtered dictionary
    return filtered_dict


def select_elements(list_of_lists, index):
    """
    Select elements at the specified index from a list of lists.

    Parameters:
        list_of_lists: A list containing inner lists.
        index: Index of the elements to be selected from each inner list.

    Returns:
        A list of the selected elements.
    """
    selected_elements = []
    for inner_list in list_of_lists:
        try:
            selected_elements.append(round(inner_list[index], 4))
        except IndexError:
            print(f"Index {index} is out of bounds for an inner list.")

    return selected_elements


def plot_dual_y_axis(params):
    """
    Plots a graph with a shared x-axis (time) and two y-axes for pairs of values.

    Parameters:
        params: Dictionary containing all parameters for the plot.
    """
    time_list = params['time_list']
    value_pairs = params['value_pairs']
    max_labels = params.get('max_labels', None)
    save_filename = params.get('save_path', None)
    figsize = params.get('figsize', (10, 6))
    font_size = params.get('font_size', 24)
    title_font_size = params.get('title_font_size', 20)
    xlabel_font_size = params.get('xlabel_font_size', 22)
    ylabel_font_size = params.get('ylabel_font_size', 22)
    legend_font_size = params.get('legend_font_size', 14)
    legend_title_font_size = params.get('legend_title_font_size', 14)
    tick_font_size = params.get('tick_font_size', 18)
    max_label_font_size = params.get(
        'max_label_font_size',
        24)  # Default font size for max_labels

    # Create figure and axis objects
    fig, ax1 = plt.subplots(figsize=figsize)

    # Plotting data
    line_styles = ['-', '--', ':', '-.']

    for i, (first_half_values, second_half_values) in enumerate(
            value_pairs):
        ax1.plot(time_list,
                 first_half_values,
                 color='blue',
                 linestyle=line_styles[i % len(line_styles)],
                 label=f"First Half Values {i + 1}")
        ax2 = ax1.twinx()
        ax2.plot(
            time_list,
            second_half_values,
            color='green',
            linestyle='-.',
            label=f"Second Half Values {
                i + 1}")

        ax2.set_ylabel(
            f"Transfer Vertex",
            color='green',
            fontsize=ylabel_font_size)
        ax2.tick_params(
            axis="y",
            labelcolor='green',
            labelsize=tick_font_size)

        # Find local maximum y-values and their corresponding x-values
        max_points = [(y, x)
                      for x, y in zip(time_list, second_half_values)]
        # Sort by y-value, highest first
        max_points.sort(key=lambda p: p[0], reverse=True)

        # Take the top N maximums, where N is the length of max_labels
        top_max_points = max_points[:len(max_labels)]

        # Calculate the range of y-values for the second axis
        ymin, ymax = ax2.get_ylim()

        for (
                max_y_value, max_x_value), label in zip(
                top_max_points, max_labels):
            # Calculate the normalized height of the maximum y-value
            normalized_max_y = (max_y_value - ymin) / (ymax - ymin)

            # Add a vertical line at the x-value where the maximum
            # y-value occurs, but limit its height
            ax2.axvline(
                x=max_x_value,
                ymin=0,
                ymax=normalized_max_y,
                color='red',
                linestyle='--')

            # Add text annotation near the vertical line at the bottom
            ax1.annotate(label,
                         xy=(max_x_value,
                             ax1.get_ylim()[0]),
                         xycoords='data',
                         xytext=(0,
                                 -28),
                         textcoords='offset points',
                         horizontalalignment='center',
                         fontsize=max_label_font_size)  # Removed arrowprops

    ax1.set_xlabel("Time", fontsize=xlabel_font_size)
    ax1.set_ylabel(
        "Initial Vertex",
        color='blue',
        fontsize=ylabel_font_size)
    ax1.tick_params(
        axis="y",
        labelcolor='blue',
        labelsize=tick_font_size)
    ax1.tick_params(axis="x", labelsize=tick_font_size)

    plt.title(
        "Hypercube Perfect State Transfer",
        fontsize=title_font_size)

    fig.tight_layout()

    if save_filename:
        plt.savefig(save_filename)

    plt.show()


n1 = 3
graph1 = nx.path_graph(n1)
initcond1 = [0]
t1 = np.linspace(0, 3 * eval('0.707108562377582*np.pi'), 1000)
qw1 = QWAK(graph=graph1)
qw1.runMultipleWalks(timeList=t1, initStateList=initcond1)

n2 = 4
graph2 = nx.hypercube_graph(n2)
initcond2 = [0]
t2 = np.linspace(0, 4 * eval('0.5*np.pi'), 1000)
qw2 = QWAK(graph=graph2)
qw2.runMultipleWalks(timeList=t2, initStateList=initcond2)

init = initcond2[0]
target = 15

time_list = t2
# ,(select_elements(qw2.getProbVecList(),0),select_elements(qw2.getProbVecList(),3))]
value_pairs = [
    (select_elements(
        qw2.getProbVecList(), init), select_elements(
            qw2.getProbVecList(), target))]
# value_pairs = [(select_elements(qw1.getProbVecList(),0),select_elements(qw1.getProbVecList(),2))]

save_file = os.path.join(SCRIPT_DIR,
                         'Notebook',
                         'Output',
                         'PerfectStateTransfer',
                         f'Hypercube_N{len(graph2)}_T{round(t2[-1],
                                                            2)}_FROM{init}_TO{target}.png')
figsize = (8, 6)

params = {
    'time_list': time_list,
    'value_pairs': value_pairs,
    'max_labels': [r"$\frac{\pi}{2}$", r"$\frac{3\pi}{2}$"],
    'save_path': save_file,
    'figsize': (16, 10),
    'font_size': 24,
    'title_font_size': 34,  # Decreased font size
    'xlabel_font_size': 28,  # Decreased font size
    'ylabel_font_size': 28,  # Decreased font size
    'legend_font_size': 28,  # Decreased font size
    'legend_title_font_size': 30,  # Decreased font size
    'tick_font_size': 26,  # Decreased font size
    'max_label_font_size': 20,  # New parameter to control max_labels font size
}

plot_dual_y_axis(params)

copy_to_latex = input(
    "Do you want to copy the generated image to the LaTeX project? (y/n): ").strip().lower()
if copy_to_latex == 'y':
    latex_project_path = os.path.normpath(os.path.join(
        SCRIPT_DIR,
        "../QWAK-Paper_Revised/img/newFigures"
    ))
    shutil.copy(save_file, latex_project_path)
    print(f"Image copied to {latex_project_path}")
else:
    print("Image not copied.")
