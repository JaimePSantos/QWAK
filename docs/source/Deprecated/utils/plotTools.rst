plot_qwak
=========

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

plot_qwak_heatmap
=================

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

