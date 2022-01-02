import numpy as np
from bokeh.models import ColumnDataSource, Button, Select, Div
from bokeh.sampledata.iris import flowers
from bokeh.plotting import figure, curdoc
from bokeh.layouts import column, row
import pandas as pd


# Important: You must also install pandas for the data import.

# calculate the cost of the current medoid configuration
# The cost is the sum of all minimal distances of all points to the closest medoids
def get_cost(medoids):
    meds = np.zeros((3, 150))
    colors = ['blue','red','green']
    for i in range(3):
        meds[i, :] = np.sum(np.absolute(numpy_data[:, :4] - numpy_data[medoids[i], :4]), axis=1)
    total_cost = 0
    for line in range(150):
        min_col = 0
        for col in range(3):
            if meds[col,line] < meds[min_col,line]:
                min_col = col

        numpy_data[line, 4] = colors[min_col]
        total_cost = total_cost + meds[min_col, line]

    return total_cost

def cost(k,medoids):
    total_cost = get_cost(medoids)
    total_cost_before = 0
    is_first_iteration = True

    while is_first_iteration or total_cost < total_cost_before:
        is_first_iteration = False
        total_cost_before = total_cost
        for i in range(k):
            for j in range(150):
                if j not in medoids:
                    prev_medoid = medoids[i]
                    medoids[i] = j
                    total_cost2 = get_cost(medoids)

                    if total_cost2 < total_cost:
                        total_cost = total_cost2
                    else:
                        medoids[i] = prev_medoid

    return (total_cost)
# implement the k-medoids algorithm in this function and hook it to the callback of the button in the dashboard
# check the value of the select widget and use random medoids if it is set to true and use the pre-defined medoids
# if it is set to false.
def k_medoids(div):
    # number of clusters:
    k = 3
    # Use the following medoids if random medoid is set to false in the dashboard. These numbers are indices into the
    # data array.
    if select.value == "False":
        medoids = [24, 74, 124]
    else:
        medoids = np.random.randint(150, size=3)
        for g in range(k):
            if g in medoids:
                medoids[g] = np.random.randint(150, size=1)

    total_cost = cost(k, medoids)
    df = pd.DataFrame(data=numpy_data, index=None, columns=["sepal_length", "sepal_width", "petal_length",
                                                            "petal_width", "color"])
    div.text = "The final cost is: {:.2f}".format(total_cost)
    source.data = dict(df)

# read and store the dataset
data = flowers.copy(deep=True)
data = data.drop(['species'], axis=1)
df = pd.DataFrame(data)

# create a color column in your dataframe and set it to gray on startup
df['color'] = 'gray'
# Create a ColumnDataSource from the data

source = ColumnDataSource(data=dict(df))
numpy_data = data.to_numpy()
total_cost = 0
# Create a select widget, a button, a DIV to show the final clustering cost and two figures for the scatter plots.

select = Select(title="Random Medoids", value="False", options=["False", "True"], width=300, height=50)
button = Button(label="Cluster Data", button_type="default", width=300, height=40)

div = Div(text="", width=300, height=100)

p = figure(plot_height=500, plot_width=500, )
p.scatter(x='petal_length', y='sepal_length', marker='circle', size=8, line_color='black', fill_color='color',
          fill_alpha=0.5, source=source)

p.title.text = 'Scatter plot of flower distribution by petal length and sepal length'
p.yaxis.axis_label = "Sepal length"
p.xaxis.axis_label = "Petal length"

p2 = figure(plot_height=500, plot_width=500, )
p2.scatter(x='petal_width', y='petal_length', marker='circle', size=8, line_color='black', fill_color='color',
           fill_alpha=0.5, source=source)

p2.title.text = 'Scatter plot of flower distribution by petal width and petal length'
p2.yaxis.axis_label = "Petal length"
p2.xaxis.axis_label = "Petal width"

# use curdoc to add your widgets to the document
widgets = column(select, button, div, sizing_mode="fixed", height=250, width=330)

total_cost = button.on_click(lambda: k_medoids(div))


curdoc().add_root(row([widgets, p, p2]))

curdoc().title = "DVA_ex_3"
# use on of the commands below to start your application
# bokeh serve --show dva_ex3_Marcela_Ulloa_20728671.py
