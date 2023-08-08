#!/usr/bin/env python
# coding: utf-8

# In[1]:


# Imports
import os

import matplotlib.pyplot as plt
from riverrem.REMMaker import REMMaker, clear_osm_cache
import requests
import rioxarray as rxr


# In[2]:


# Function to download and load dtm as data array
def load_dtm(data_url, site_name, file_name):
    """Creates DataArray of Elevation Model Data
    
    Parameters
    ----------
    data_url: str
        Url to the desired data.
    data_name: str
        The name of the data.
        
    Returns
    ---------
    dtm : dataarray
        A dataarray of the elevation model.

    """
    
    override_cache = False
    data_dir = site_name
    data_path = (os.path.join(data_dir, file_name))
    
    # Cache data file
    if not os.path.exists(data_dir):
        print('{} does not exist. Creating...'.format(data_dir))
        os.makedirs(data_dir)

    if (not os.path.exists(data_path)) or override_cache:
        print('{} does not exist. Downloading...'.format(data_path))
        # Download full data file as zipfile
        response = requests.get(data_url)

        # Write in respose content using context manager
        with open(data_path, 'wb') as data_file:
            data_file.write(response.content)
    # Open and plot the DTM
    dtm = rxr.open_rasterio(data_path, masked=True)
              
    return dtm


# In[3]:


# Function to plot elevation models
def plot_model(model, title, coarsen, ax):
    """
    Creates a plot of the DTM or REM.
    
    Parameters
    ------------
    model: dataarray
        The dataarray to plot.

    title: str
        The title of the plot.
        
    coarsen: boolean
        True = coarsen data, False = do not coarsen.
        
    ax: axes
        A matplotlib axes object.

    Returns
    -------
    A plot of the elevation model with specified title.
    """

    # Hide x and y axes labels and ticks
    ax.xaxis.set_tick_params(labelbottom=False)
    ax.yaxis.set_tick_params(labelleft=False)
    ax.set_xticks([])
    ax.set_yticks([])

    # If DTM, coarsen
    if coarsen == True:
        model.coarsen(
            x=3,
            boundary='trim').mean().coarsen(
                y=3,
                boundary='trim').mean().squeeze()
    # Plot DTM
    model.plot(ax=ax)

    # Add title
    ax.set_title(title, fontsize=14)
    
    ax.legend('off')
    ax.axis('off')


# In[4]:


# Function to plot a histogram of the REM 
def plot_hist(model, title, color):
    """Creates a Single Histogram of Elevation Model Data
    
    Parameters
    ----------
    model: dataarray
        The dataarray to plot.

    title: str
        The title of the plot.
        
    color: str
        Desired color of the plot.
        
    Returns
    -------
    The histogram of the elevation model with specified title and color.
    """

    # Create REM histogram plot 
    fig, ax = plt.subplots(figsize=(10, 6))
    model.plot.hist(color=color, bins=20)
    ax.set_title(title)
    plt.show()


# In[ ]:


def plot_hists(model, titles, main_title, color, fig, ax):
    """Creates Multiple Histograms of Elevation Model Data
    
    Parameters
    ----------
    model: dataarray
        The dataarray to plot.

    titles: str
        The title of the subplot.
    
    main_title: str
        The main plot title.
        
    color: str
        Desired color of the plot.
    
    fig: figure
        A matplotlib figure object.
    
    ax: axes
        A matplotlib axes object.

        
    Returns
    -------
    Histogram of elevation models with specified titles and color.
    """
    
    model.plot.hist(color=color, bins=20, ax=ax)
    ax.set_title(titles, fontsize=12)
    ax.set(xlabel=None)
    fig.suptitle(main_title, fontsize=16)
    fig.supxlabel('Elevation (m)')
    fig.supylabel('Frequency')


# In[5]:


# Function to run REMMaker with UAV dtms
def run_rem_maker(site_name, k=100):
    """Function to run the REMMaker tool on UAV DTMs
    
    Parameters
    -----------
    site_name: str
        Name of the site with existing DTM.
    k: int
        Number of interpolation points.
        
    Returns
    ----------
    '{site_name}_dtm_REM.tif': image saved locally
        REM image file.
    """
    
    # Input the DTM file path and desired output directory
    override_cache = False
    uav_dtm_path = os.path.join(site_name, ('{}_dtm.tif').format(site_name))
    uav_out_dir = os.path.join(site_name, 'remmaker')
    if (not os.path.exists(uav_out_dir)) or override_cache:
            print('{} does not exist. Downloading...'.format(uav_out_dir))
            os.makedirs(uav_out_dir)
    uav_rem_path = os.path.join(uav_out_dir, 
                                  ('{}_dtm_REM.tif').format(site_name))

    # Run the REMMaker if the path to the REM does not already exist
    if (not os.path.exists(uav_rem_path)) or override_cache:
        rem_maker = REMMaker(dem=uav_dtm_path, 
                             out_dir=uav_out_dir, 
                             interp_pts=1000, 
                             k=100)

        # clear OSM cache
        clear_osm_cache()

        # create an REM
        rem_maker.make_rem()

        # create an REM visualization with the given colormap
        rem_maker.make_rem_viz(cmap='mako_r')

    else:
        print('The REM already exists. Not running REMMaker')

