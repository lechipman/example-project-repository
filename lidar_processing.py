#!/usr/bin/env python
# coding: utf-8

# In[9]:


# Import packages
# Make sure you have RiverREM imported, check readme for instructions
import os
import pathlib

import matplotlib.pyplot as plt
from load_plot_model import load_dtm, plot_model, plot_hists, plot_hist, run_rem_maker
from riverrem.REMMaker import REMMaker, clear_osm_cache
import requests
import rioxarray as rxr


# In[2]:


# Set working directory
working_dir = os.path.join(
    pathlib.Path.home(), 'earth-analytics', 'data', 'watershed-project')

# Try/Except Block   
try:
    os.chdir(working_dir)
except:
    print('{} does not exist. Creating...'.format(working_dir))
    os.makedirs(working_dir)
    os.chdir(working_dir)
else:
    print('{} is now the working directory'.format(working_dir))


# # Load the UAV DTMs and REMs

# In[3]:


# Define urls to UAV DTMs and REMs (saved on zenodo)
# make into function
hallmeadows_rem_url = ('https://github.com/lechipman/watershed-project/releases'
                       '/download/v2.0.0/hallmeadows_rem.tif')
hallmeadows_lidar_dtm_url = ('https://github.com/lechipman/watershed-project/'
                             'releases/download/v2.0.0/hallmeadows_lidar_dtm.asc')


# In[4]:


# Load dataarrays for UAV-derived dtms and rems and lidar rems
hallmeadows_uav_rem = load_dtm(data_url = hallmeadows_rem_url, 
                          site_name = 'hallmeadows',
                          file_name = 'hallmeadows_rem.tif')
hallmeadows_lidar_dtm = load_dtm(data_url = hallmeadows_lidar_dtm_url, 
                          site_name = 'hallmeadows',
                          file_name = 'hallmeadows_lidar_dtm.asc')
