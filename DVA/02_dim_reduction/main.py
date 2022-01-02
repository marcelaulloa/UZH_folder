import glob
import os
from matplotlib import pyplot as plt
import numpy as np
from PIL import Image

from sklearn.manifold import TSNE
from sklearn.decomposition import PCA
from sklearn.preprocessing import normalize

from bokeh.plotting import figure, curdoc
from bokeh.models import ColumnDataSource
from bokeh.layouts import layout

# Dependencies
# Make sure to install the additional dependencies noted in the requirements.txt using the following command:
# pip install -r requirements.txt

# You might want to implement a helper function for the update function below or you can do all the calculations in the
# update callback function.

# Only do this once you've followed the rest of the instructions below and you actually reach the part where you have to
# configure the callback of the lasso select tool. The ColumnDataSource containing the data from the dimensionality
# reduction has an on_change callback routine that is triggered when certain parts of it are selected with the lasso
# tool. More specifically, a ColumnDataSource has a property named selected, which has an on_change routine that can be
# set to react to its "indices" attribute and will call a user defined callback function. Connect the on_change routine
# to the "indices" attribute and an update function you implement here. (This is similar to the last exercise but this
# time we use the on_change function of the "selected" attribute of the ColumnDataSource instead of the on_change
# function of the select widget).
# In simpler terms, each time you select a subset of image glyphs with the lasso tool, you want to adjust the source
# of the channel histogram plot based on this selection.
# Useful information:
# https://docs.bokeh.org/en/latest/docs/reference/models/sources.html
# https://docs.bokeh.org/en/latest/docs/reference/models/tools.html
# https://docs.bokeh.org/en/latest/docs/reference/models/selections.html#bokeh.models.selections.Selection


def callback1(attr, old, new):
    try:
        #images_indx = new
        N_BINS_CHANNEL_filtered2 = sum(N_BINS_CHANNEL_array[new, :])
        CHANNEL_s.data = dict(x=range(0, 50), red=N_BINS_CHANNEL_filtered2[0], green=N_BINS_CHANNEL_filtered2[1],blue=N_BINS_CHANNEL_filtered2[2])
    except:
        CHANNEL_s.data = dict(x=range(0,50), red=N_BINS_CHANNEL_filtered[0], green=N_BINS_CHANNEL_filtered[1], blue=N_BINS_CHANNEL_filtered[2])


# Fetch the number of images using glob or some other path analyzer
N = len(glob.glob("static/*.jpg"))

# Find the root directory of your app to generate the image URL for the bokeh server
ROOT = os.path.split(os.path.abspath("."))[1] + "/"

# Number of bins per color for the 3D color histograms
N_BINS_COLOR = 16
# Number of bins per channel for the channel histograms
N_BINS_CHANNEL = 50

# Define an array containing the 3D color histograms. We have one histogram per image each having N_BINS_COLOR^3 bins.
# i.e. an N * N_BINS_COLOR^3 array
N_BINS_COLOR_array = np.zeros(shape=(N, N_BINS_COLOR ** 3))

# Define an array containing the channel histograms, there is one per image each having 3 channel and N_BINS_CHANNEL
# bins i.e an N x 3 x N_BINS_CHANNEL array
N_BINS_CHANNEL_array = np.zeros(shape=(N, 3, N_BINS_CHANNEL))

# initialize an empty list for the image file paths
image_file_path = []

# Compute the color and channel histograms
for idx, f in enumerate(glob.glob("static/*.jpg")):
    # open image using PILs Image package

    im = Image.open(f)
    im_w, im_h = im.size
    N_Pixels = im_w * im_h
    channels = im.getbands()

    # Convert the image into a numpy array and reshape it such that we have an array with the dimensions (N_Pixel, 3)
    data = np.asarray(im)
    data = np.reshape(data, (N_Pixels, 3))

    # Compute a multi dimensional histogram for the pixels, which returns a cube
    # reference: https://numpy.org/doc/stable/reference/generated/numpy.histogramdd.html
    H, edges = np.histogramdd(data, bins=N_BINS_COLOR)

    # However, later used methods do not accept multi dimensional arrays, so reshape it to only have columns and rows
    # (N_Images, N_BINS^3) and add it to the color_histograms array you defined earlier
    # reference: https://numpy.org/doc/stable/reference/generated/numpy.reshape.html
    H = np.reshape(H, ((N_BINS_COLOR ** 3)))
    N_BINS_COLOR_array[idx] = H

    # Append the image url to the list for the server
    url = ROOT + f
    image_file_path = image_file_path + [url]

    # Compute a "normal" histogram for each color channel (rgb)
    # reference: https://numpy.org/doc/stable/reference/generated/numpy.histogram.html

    hist_red, bins_r = np.histogram(data[:, 0], N_BINS_CHANNEL, [0, 256],density=True)
    hist_green, bins_g = np.histogram(data[:, 1], N_BINS_CHANNEL, [0, 256], density=True)
    hist_blue, bins_b = np.histogram(data[:, 2], N_BINS_CHANNEL, [0, 256], density=True)

    # and add them to the channel_histograms
    N_BINS_CHANNEL_array[idx] = [hist_red, hist_green, hist_blue]

# Calculate the indicated dimensionality reductions
# references:
# https://scikit-learn.org/stable/modules/generated/sklearn.manifold.TSNE.html
# https://scikit-learn.org/stable/modules/generated/sklearn.decomposition.PCA.html

# t-SNE reduction
N_BINS_COLOR_tsne = TSNE(n_components=2).fit_transform(N_BINS_COLOR_array)

# PCA reduction
s_N_BINS_COLOR_array = normalize(N_BINS_COLOR_array)
pca = PCA(n_components=2)
N_BINS_COLOR_pca = pca.fit_transform(s_N_BINS_COLOR_array)

# Construct a data source containing the dimensional reduction result for both the t-SNE and the PCA and the image paths
COLOR_source = ColumnDataSource(
    data=dict(url=image_file_path, TSNE_X=list(N_BINS_COLOR_tsne[:, 0]), TSNE_Y=list(N_BINS_COLOR_tsne[:, 1]),PCA_X=list(N_BINS_COLOR_pca[:,0]),PCA_Y=list(N_BINS_COLOR_pca[:,1])))

# Create a first figure for the t-SNE data. Add the lasso_select, wheel_zoom, pan and reset tools to it.
plot_TSNE = figure(height=500, width=500, title="t-SNE", toolbar_location='right', tools="lasso_select,pan,wheel_zoom,reset")

# And use bokehs image_url to plot the images as glyphs
# reference: https://docs.bokeh.org/en/latest/docs/reference/models/glyphs/image_url.html
w, h = 820, 664
plot_TSNE.image_url(url="url", x='TSNE_X', y='TSNE_Y', source=COLOR_source, w=w / 30, h=h / 30, h_units="screen", w_units="screen")

# Since the lasso tool isn't working with the image_url glyph you have to add a second renderer (for example a circle
# glyph) and set it to be completely transparent. If you use the same source for this renderer and the image_url,
# the selection will also be reflected in the image_url source and the circle plot will be completely invisible.
plot_TSNE.circle(x="TSNE_X",y="TSNE_Y",source=COLOR_source, size=20, color="white", alpha=0)
plot_TSNE.yaxis.axis_label = "y"
plot_TSNE.xaxis.axis_label = "x"

# Create a second plot for the PCA result. As before, you need a second glyph renderer for the lasso tool.
# Add the same tools as in figure 1
plot_PCA = figure(height=500, width=550, title="PCA", toolbar_location='right', tools="lasso_select,pan,wheel_zoom,reset")
plot_PCA.image_url(url="url", x='PCA_X', y='PCA_Y', source=COLOR_source, w=w / 30, h=h / 30, h_units="screen", w_units="screen")
plot_PCA.circle(x="PCA_X",y="PCA_Y",source=COLOR_source, size=20, color="white", alpha=0)
plot_PCA.yaxis.axis_label = "y"
plot_PCA.xaxis.axis_label = "x"

# Construct a datasource containing the channel histogram data. Default value should be the selection of all images.
# Think about how you aggregate the histogram data of all images to construct this data source
N_BINS_CHANNEL_filtered = sum(N_BINS_CHANNEL_array[:,:])
CHANNEL_s = ColumnDataSource(data=dict(x=range(0,50), red=N_BINS_CHANNEL_filtered[0], green=N_BINS_CHANNEL_filtered[1], blue=N_BINS_CHANNEL_filtered[2]))

# Construct a histogram plot with three lines.
# First define a figure and then make three line plots on it, one for each color channel.
# Add the wheel_zoom, pan and reset tools to it.
plot_hist = figure(height=500, width=500, title="Channel Histogram", toolbar_location='right', tools="lasso_select,pan,wheel_zoom,reset", x_range=(0, 50))
plot_hist.line(x='x', y='red',color="red", line_width = 2, source=CHANNEL_s)
plot_hist.line(x='x', y='green',color='green', line_width = 2, source=CHANNEL_s)
plot_hist.line(x='x', y='blue',color='blue', line_width = 2, source=CHANNEL_s)
plot_hist.yaxis.axis_label = "Frequency"
plot_hist.xaxis.axis_label = "bins"

# Connect the on_change routine of the selected attribute of the dimensionality reduction ColumnDataSource with a
# callback/update function to recompute the channel histogram. Also read the topmost comment for more information.
COLOR_source.selected.on_change('indices',callback1)

# Construct a layout and use curdoc() to add it to your document.
curdoc().add_root(layout([[plot_TSNE, plot_PCA,plot_hist]]))

# You can use the command below in the folder of your python file to start a bokeh directory app.
# Be aware that your python file must be named main.py and that your images have to be in a subfolder name "static"

# bokeh serve --show .
# python -m bokeh serve --show .

# dev option:
# bokeh serve --dev --show .
# python -m bokeh serve --dev --show .