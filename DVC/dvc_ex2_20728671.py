#!/usr/bin/env python
# coding: utf-8

# In[15]:


import pandas as pd 
from math import pi
import numpy as np
from bokeh.io import output_file, show, save
from bokeh.plotting import figure
from bokeh.models import ColumnDataSource, HoverTool,FactorRange
from bokeh.palettes import inferno
 
# Goal: Draw a line chart displaying averaged daily new cases for all cantons in Switzerland.
# Dataset: covid19_cases_switzerland_openzh-phase2.csv
# Interpretation: value on row i, column j is either the cumulative covid-19 case number of canton j on date i or null value

### Task 1: Data Preprocessing


## T1.1 Read data into a dataframe, set column "Date" to be the index 

url = 'https://github.com/daenuprobst/covid19-cases-switzerland/blob/master/covid19_cases_switzerland_openzh-phase2.csv'
raw_url = url+'?raw=true'
df = pd.read_csv(raw_url,index_col=0)


# Initialize the first row with zeros, and remove the last column 'CH' from dataframe

#Removing column 'CH' and all Difference columns from dataframe:
df.drop(df.columns[df.columns.get_loc('CH'):df.columns.get_loc('CH_diff_pc')+1], inplace=True, axis=1)
df = pd.DataFrame(df)

# Initializing the first row with zeros:
new_df = df.iloc[0:1,0:26]
new_df.replace(1.0,0.0, inplace=True)
new_df = new_df.fillna(0)

# Removing original first row to be replace with the one with zeros:
df = df.drop(['2020-05-31'])

# Appending new row set with zeros
new_df = new_df.append(df)

# Fill null with the value of previous date from same canton
# https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.DataFrame.fillna.html
new_df = new_df.fillna(method='ffill')

## T1.2 Calculate and smooth daily case changes

# Compute daily new cases (dnc) for each canton, e.g. new case on Tuesday = case on Tuesday - case on Monday;
# Fill null with zeros as well
dnc = new_df.diff(periods=1)
dnc = dnc.fillna(0)

# Smooth daily new case by the average value in a rolling window, and the window size is defined by step
# Why do we need smoothing? How does the window size affect the result?
# https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.DataFrame.rolling.html
step = 2
dnc_avg = dnc.rolling(step).mean()
dnc_avg = dnc_avg.fillna(0)


## T1.3 Build a ColumnDataSource 

# Extract all canton names and dates
# NOTE: be careful with the format of date when it is used as x input for a plot
cantons = list(dnc_avg.columns.values)
dnc_avg.index = pd.to_datetime(dnc_avg.index, format = '%Y-%m-%d')
date = list(dnc_avg.index)

# Create a color list to represent different cantons in the plot, you can either construct your own color patette or use the Bokeh color pallete
color_palette = inferno(26)

# Build a dictionary with date and each canton name as a key, i.e., {'date':[], 'AG':[], ..., 'ZH':[]}
# For each canton, the value is a list containing the averaged daily new cases
source_dict_1 = {'date':date}
source_dict_2 = dnc_avg.to_dict(orient='list')

source_dict = {}
for d in (source_dict_1, source_dict_2): source_dict.update(d)

source = ColumnDataSource(data=source_dict)

### Task 2: Data Visualization

## T2.1: Draw a group of lines, each line represents a canton, using date, dnc_avg as x,y. Add proper legend.
# https://docs.bokeh.org/en/latest/docs/reference/models/glyphs/line.html?highlight=line#bokeh.models.glyphs.Line
# https://docs.bokeh.org/en/latest/docs/user_guide/interaction/legends.html

p = figure(plot_width=1000, plot_height=800, x_axis_type="datetime")
p.title.text = 'Daily New Cases in Switzerland'

for canton,color in zip(cantons,color_palette): 
    p.line(x='date',y=canton, source=source, color=color,line_width=2, legend_label=canton, name=canton)

p.legend.location = "top_left"

# Make the legend of the plot clickable, and set the click_policy to be "hide"
p.legend.click_policy="hide"


## T2.2 Add hovering tooltips to display date, canton and averaged daily new case

# (Hovertip doc) https://docs.bokeh.org/en/latest/docs/user_guide/tools.html#hovertool
# (Date hover)https://stackoverflow.com/questions/41380824/python-bokeh-hover-date-time

hover = HoverTool(tooltips=[
        ('date', '@date{%F}'),
        ( 'canton',  '$name' ),
        ( 'cases', "$y{0,0}")],
        formatters={'@date': 'datetime'})
hover.mode = 'mouse'

p.add_tools(hover)

show(p)
output_file("dvc_ex2.html")
save(p)


# In[ ]:





# In[ ]:




