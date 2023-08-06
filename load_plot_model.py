#!/usr/bin/env python
# coding: utf-8

# In[1]:


# Imports
import os

import matplotlib.pyplot as plt
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
def plot_model(model, title, coarsen):
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

    Returns
    -------
    A plot of the elevation model with specified title.
    """
    
    fig, ax = plt.subplots(1, 1, figsize=(10, 6))

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


# In[4]:


# Function to plot a histogram of the REM 
def plot_hist(model, title, color):
    """Creates a Histogram of Elevation Model Data
    
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

