#!/usr/bin/env python
# coding: utf-8

# In[1]:


# Imports
import os

import matplotlib.pyplot as plt


# In[6]:


# Function to plot Elevation models
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

