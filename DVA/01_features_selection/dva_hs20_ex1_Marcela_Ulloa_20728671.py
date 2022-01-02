import pandas as pd
import numpy as np
from bokeh.layouts import row
from bokeh.models import ColumnDataSource, HoverTool, Select
from bokeh.plotting import figure, curdoc

# This exercise will be graded using the following Python and library versions:
###############
# Python 3.8
# Bokeh 2.2.1
# Pandas 1.1.2
###############

# define your callback function of the Select widget here. Only do this once you've followed the rest of the
# instructions below and you actually reach the part where you have to add and configure the Select widget.
# the general idea is to set the data attribute of the plots ColumnDataSource to the data entries of the different
# ColumnDataSources you construct during the data processing. This data change should then automatically be displayed
# in the plot. Take care that the bar-labels on the y axis also reflect this change.
def callback(attr, old, new):
    if new == "Mammalia" or select.value == "Mammalia":
        source.data = df_Mammalia.to_dict(orient='list')
    elif new == "Aves" or select.value == "Aves":
        source.data = df_Aves.to_dict(orient='list')
    else:
        source.data = df_Reptilia.to_dict(orient='list')
    plot.y_range.factors = source.data['species']

# read data from .csv file
df = pd.read_csv('AZA_MLE_Jul2018_utf8.csv', encoding='utf-8')
# construct list of indizes to remove unnecessary columns
cols = [1, 3]
cols.extend([i for i in range(7, 15)])
df.drop(df.columns[cols], axis=1, inplace=True)


# task 1

# rename the columns of the data frame according to the following mapping:
# 'Species Common Name': 'species'
# 'TaxonClass': 'taxon_class'
# 'Overall CI - lower': 'ci_lower'
# 'Overall CI - upper': 'ci_upper'
# 'Overall MLE': 'mle'
# 'Male Data Deficient': 'male_deficient'
# 'Female Data Deficient': 'female_deficient'
df = df.rename(columns={'Species Common Name': 'species',
                        'TaxonClass':'taxon_class',
                        'Overall CI - lower':'ci_lower',
                        'Overall CI - upper':'ci_upper',
                        'Overall MLE':'mle',
                        'Male Data Deficient':'male_deficient',
                        'Female Data Deficient':'female_deficient'})

# Remove outliers, split the dataframe by taxon_class and and construct a ColumnDataSource from the clean DataFrames
# hints:
# we only use the following three taxon classes: 'Mammalia', 'Aves', 'Reptilia'
# use dataframe.loc to access subsets of the original dataframe and to remove the outliers
# each time you sort the dataframe reset its index
# outliers are entries which have male and/or female data deficient set to yes
# reference dataframe: https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.DataFrame.html
# reference columndatasource: https://bokeh.pydata.org/en/latest/docs/reference/models/sources.html

filt_m = (df['taxon_class']=='Mammalia') & (df['male_deficient']!='yes') & (df['female_deficient']!='yes')
df_Mammalia = df.loc[filt_m]

filt_a = (df['taxon_class']=='Aves') & (df['male_deficient']!='yes') & (df['female_deficient']!='yes')
df_Aves = df.loc[filt_a]

filt_r = (df['taxon_class']=='Reptilia') & (df['male_deficient']!='yes') & (df['female_deficient']!='yes')
df_Reptilia = df.loc[filt_r]

# construct three independent dataframes based on the aforementioned taxon classes and remove the outliers

# sort the dataframes by 'mle' in descending order and then reset the index
df_Mammalia = df_Mammalia.sort_values(by='mle', ascending=False)
df_Aves = df_Aves.sort_values(by='mle', ascending=False)
df_Reptilia = df_Reptilia.sort_values(by='mle', ascending=False)

df_Mammalia.reset_index(drop=True,inplace=True)
df_Aves.reset_index(drop=True,inplace=True)
df_Reptilia.reset_index(drop=True,inplace=True)

# reduce each dataframe to contain only the 10 species with the highest 'mle'

df_Mammalia = df_Mammalia.iloc[:10]
df_Aves = df_Aves.iloc[:10]
df_Reptilia = df_Reptilia.iloc[:10]

# sort the dataframe in the correct order to display it in the plot and reset the index again.
# hint: the index decides the y location of the bars in the plot. You might have to modify it to have a visually
# appealing barchart

df_Mammalia = df_Mammalia.sort_values(by='mle', ascending=True)
df_Aves = df_Aves.sort_values(by='mle', ascending=True)
df_Reptilia = df_Reptilia.sort_values(by='mle', ascending=True)

df_Mammalia.reset_index(drop=True,inplace=True)
df_Aves.reset_index(drop=True,inplace=True)
df_Reptilia.reset_index(drop=True,inplace=True)

# There's an entry in the aves dataframe with a species named 'Penguin, Northern & Southern Rockhopper (combined)'.
# Rename that species to 'Penguin, Rockhopper'

df_Aves.replace('Penguin, Northern & Southern Rockhopper (combined)','Penguin, Rockhopper',inplace=True)

# construct a ColumDataSource for each of the dataframes
source_m = ColumnDataSource(data=df_Mammalia.to_dict(orient='list'))
source_a = ColumnDataSource(data=df_Aves.to_dict(orient='list'))
source_r = ColumnDataSource(data=df_Reptilia.to_dict(orient='list'))

# construct a fourth ColumnDataSource that is used as input for the plot and set its data to the Mammalian
# ColumnDataSource as initial value. This fourth ColmunDataSource is required to later be able to change the data
# interactively with the dropdown menu.
source = source_m

# task 2:

# configure mouse hover tool
# reference: https://bokeh.pydata.org/en/latest/docs/user_guide/categorical.html#hover-tools
# your tooltip should contain the data of 'ci_lower' and 'ci_upper' named 'low' and 'high' in the visualization

TOOLTIPS = [
    ("low", "@ci_lower{F.000}"),
    ("high", "@ci_upper{F.000}")
]
# construct a figure with the correct title, axis labels, x and y range, add the hover tool and disable the toolbar
plot = figure(y_range=source.data['species'],x_range=(0, 50), plot_height=500, plot_width=800,
               title="Medium Life Expectancy of Animals in Zoos", toolbar_location=None, tools="hover",
               tooltips=TOOLTIPS)
plot.xaxis.axis_label = "Medium life expectancy [Years]"
plot.yaxis.axis_label = "Species"
plot.xgrid.grid_line_color = None

# add the horizontal bar chart to the figure and configure it correctly
# the lower limit of the bar should be ci_lower and the upper limit ci_upper
plot.hbar(y='species', height=0.7, left='ci_lower', right='ci_upper', color="navy", source=source)

# add a Select tool (dropdown selection) and configure its 'on_change' callback. Define the callback function in the
# beginning of the document and write it such that the user can choose which taxon_class is visualized in the plot.
# the default visualization at startup should be 'Mammalia'
select = Select(title="Taxon Class", value="Mammalia", options=["Mammalia", "Aves","Reptilia"])
select.on_change("value", callback)

# use curdoc to add your plot and selection widget such that you can start a bokeh server and an interactive plotting
# session.
curdoc().add_root(row(plot, select))
curdoc().title = 'dva_hs20_ex1_20728671'

# you should be able to start a plotting session executing one of the following commands in a terminal:
# (if you're using a virtual environment you first have to activate it before using these commands. You have to be in
# the same folder as your dva_hs20_ex1_skeleton.py file.)
# Interactive session: bokeh serve --show dva_hs20_ex1_skeleton.py
# If the above doesn't work use the following: python -m bokeh serve --show dva_hs20_ex1_skeleton.py
# For interactive debugging sessions you can use one of the two commands below. As long as you don't close your last
# browser tab you can save your changes in the python file and the bokeh server will automatically reload your file,
# reflecting the changes you just made. Be aware that after changes leading to errors you usually have to restart
# the bokeh server by interrupting it in your terminal and executing the command again.
# bokeh serve --dev --show dva_hs20_ex1_skeleton.py
# python -m bokeh serve --dev --show dva_hs20_ex1_skeleton.py
