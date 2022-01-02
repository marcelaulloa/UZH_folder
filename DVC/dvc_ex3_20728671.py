import pandas as pd 
import numpy as np
import bokeh.palettes as bp
from bokeh.plotting import figure
from bokeh.io import output_file, show, save
from bokeh.models import ColumnDataSource, HoverTool, ColorBar, RangeTool
from bokeh.transform import linear_cmap
from bokeh.layouts import gridplot


# ==========================================================================
# Goal: Visualize Covid-19 Tests statistics in Switzerland with linked plots
# Dataset: covid19_tests_switzerland_bag.csv
# Data Interpretation: 
# 		n_negative: number of negative cases in tests
# 		n_positive: number of positive cases in tests
# 		n_tests: number of total tests
# 		frac_negative: fraction of POSITIVE cases in tests
# ==========================================================================



### Task1: Data Preprocessing


## T1.1 Read the data to the dataframe "raw"
# You can read the latest data from the url, or use the data provided in the folder (update Nov.3, 2020)

url = 'covid19_tests_switzerland_bag.csv'
df = pd.read_csv(url, index_col=0)

## T1.2 Create a ColumnDataSource containing: date, positive number, positive rate, total tests
# All the data can be extracted from the raw dataframe.

# date = ...
# pos_num = ...
# pos_rate = ...
# test_num = ...
#
#
# source = ColumnDataSource(...)


## T1.3 Map the range of positive rate to a colormap using module "linear_cmap"
# "low" should be the minimum value of positive rates, and "high" should be the maximum value

# mapper = linear_cmap(...)




### Task2: Data Visualization
# Reference link:
# (range tool example) https://docs.bokeh.org/en/latest/docs/gallery/range_tool.html?highlight=rangetool


## T2.1 Covid-19 Total Tests Scatter Plot
# x axis is the time, and y axis is the total test number. 
# Set the initial x_range to be the first 30 days.

# TOOLS = "box_select,lasso_select,wheel_zoom,pan,reset,help"
# p = figure(...)
# p.scatter(...)
#
# p.title.text = 'Covid-19 Tests in Switzerland'
# p.yaxis.axis_label = "Total Tests"
# p.xaxis.axis_label = "Date"
# p.sizing_mode = "stretch_both"

# Add a hovertool to display date, total test number
# hover = HoverTool(...)
# p.add_tools(hover)


## T2.2 Add a colorbar to the above scatter plot, and encode positve rate values with colors; please use the color mapper defined in T1.3 

# color_bar = ColorBar(...)




## T2.3 Covid-19 Positive Number Plot using RangeTool
# In this range plot, x axis is the time, and y axis is the positive test number.

# select = figure(...)

# Define a RangeTool to link with x_range in the scatter plot
# range_tool = RangeTool(...)


# Draw a line plot and add the RangeTool to the plot
# select ...
# select.yaxis.axis_label = "Positive Cases"
# select.xaxis.axis_label = "Date"



# Add a hovertool to the range plot and display date, positive test number
# hover2 = HoverTool(...)
# select.add_tools(hover2)


## T2.4 Layout arrangement and display

# linked_p = ...
# show(linked_p)
# output_file("dvc_ex3.html")
# save(linked_p)

