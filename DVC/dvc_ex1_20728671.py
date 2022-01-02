#!/usr/bin/env python
# coding: utf-8

# In[395]:


import numpy as np
import pandas as pd 
from math import pi
from bokeh.io import output_file, show, save
from bokeh.plotting import figure
from bokeh.models import ColumnDataSource, HoverTool,FactorRange,CustomJS
from itertools import accumulate
# import bokeh.palettes as bp # uncomment it if you need special colors that are pre-defined

 
### Task 1: Data Preprocessing
 

## T1.1 Read online .csv file into a dataframe using pandas
# Reference links: 
# https://pandas.pydata.org/pandas-docs/stable/reference/frame.html
# https://stackoverflow.com/questions/55240330/how-to-read-csv-file-from-github-using-pandas 

original_url = 'https://github.com/daenuprobst/covid19-cases-switzerland/blob/master/demographics_switzerland_bag.csv'
raw_url = original_url+'?raw=true'
df = pd.read_csv(raw_url,index_col=0)

## T1.2 Prepare data for a grouped vbar_stack plot
# Reference link, read first before starting:
# https://docs.bokeh.org/en/latest/docs/user_guide/categorical.html#stacked-and-grouped

# Filter out rows containing 'CH'
df = pd.DataFrame(df[df['canton']!='CH'])

# Extract unique value lists of canton, age_group and sex
canton = df['canton']
age_group = df['age_group']
sex = df['sex']

canton=canton.drop_duplicates(keep='first', inplace=False).tolist()
age_group=age_group.drop_duplicates(keep='first', inplace=False).tolist()
sex=sex.drop_duplicates(keep='first', inplace=False).tolist()

# Create a list of categories in the form of [(canton1,age_group1), (canton2,age_group2), ...]
factors = []
factors = [ (c,a) for c in canton for a in age_group]    

# Use genders as stack names
stacks = ['male', 'female']

# Calculate total population size as the value for each stack identified by canton,age_group and sex

female = pd.DataFrame(df[df['sex']!='Männlich'])
female = female.groupby(['canton','age_group','sex']).sum('pop_size')
female = female['pop_size'].tolist()

male = pd.DataFrame(df[df['sex']=='Männlich'])
male = male.groupby(['canton','age_group','sex']).sum('pop_size')
male = male['pop_size'].tolist()

# Build a ColumnDataSource using above information
source = ColumnDataSource(data=dict(x=factors, male=male,female=female))

### Task 2: Data Visualization


## T2.1: Visualize the data using bokeh plot functions
p=figure(x_range=FactorRange(*factors), plot_height=500, plot_width=800, title='Canton Population Visualization')
p.yaxis.axis_label = "Population Size"
p.xaxis.axis_label = "Canton"
p.sizing_mode = "stretch_both"
p.xgrid.grid_line_color = None


renderers = p.vbar_stack(stacks,x='x', width=0.9, alpha=0.5, color=["#718dbf", "#e84d60"], source=source,legend_label=stacks,name=stacks)

## T2.2 Add the hovering tooltips to the plot using HoverTool
# To be specific, the hover tooltips should display “gender”, canton, age group”, and “population” when hovering.
# https://docs.bokeh.org/en/latest/docs/user_guide/tools.html#hovertool
# read more if you want to create fancy hover text: https://stackoverflow.com/questions/58716812/conditional-tooltip-bokeh-stacked-chart

p.legend.location = "top_left"

for r in renderers:
    stacks = r.name
    hover = HoverTool(tooltips=[
        ('gender', "%s" % stacks),
        ( 'canton, age group',  '@x' ), # use @{ } for field names with spaces
        ( 'population', "@%s" % stacks )
    ], renderers=[r])
p.add_tools(hover)
show(p)

## T2.3 Save the plot as "dvc_ex1.html" using output_file
output_file("dvc_ex1.html")


# In[ ]:




