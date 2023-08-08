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
# make into function; note when I upload the lidar urls, the crs is lost,
# so I call them locally later in code - question for elsa?
highway93_dtm_url = ('https://zenodo.org/record/8218054/files/'
                     'highway93_uav_dtm.tif?download=1')
highway93_rem_url = ('https://zenodo.org/record/8218054/files/'
                     'highway93_uav_rem.tif?download=1')
highway93_lidar_dtm_url = ('https://zenodo.org/record/8218054/files/'
                           'highway93_lidar_dtm.asc?download=1')
applevalley_dtm_url = ('https://zenodo.org/record/8218054/files/'
                       'applevalley_uav_dtm.tif?download=1')
applevalley_rem_url = ('https://zenodo.org/record/8218054/files/'
                       'applevalley_uav_rem.tif?download=1')
applevalley_lidar_dtm_url = ('https://zenodo.org/record/8218054/files/'
                             'applevalley_lidar_dtm.asc?download=1') 
hallmeadows_dtm_url = ('https://zenodo.org/record/8218054/files/'
                       'hallmeadows_uav_dtm.tif?download=1')
hallmeadows_rem_url = ('https://zenodo.org/record/8218054/files/'
                       'hallmeadows_uav_rem.tif?download=1')
hallmeadows_lidar_dtm_url = ('https://zenodo.org/record/8218054/files/'
                             'hallmeadows_lidar_dtm.asc?download=1')


# In[4]:


# Load dataarrays for UAV-derived dtms and rems and lidar rems
highway93_uav_dtm = load_dtm(data_url = highway93_dtm_url, 
                          site_name = 'highway93',
                          file_name = 'highway93_dtm.tif')
applevalley_uav_dtm = load_dtm(data_url = applevalley_dtm_url, 
                          site_name = 'applevalley',
                          file_name = 'applevalley_dtm.tif')
hallmeadows_uav_dtm = load_dtm(data_url = hallmeadows_dtm_url, 
                          site_name = 'hallmeadows',
                          file_name = 'hallmeadows_dtm.tif')
highway93_uav_rem = load_dtm(data_url = highway93_rem_url, 
                          site_name = 'highway93',
                          file_name = 'highway93_rem.tif')
applevalley_uav_rem = load_dtm(data_url = applevalley_rem_url, 
                          site_name = 'applevalley',
                          file_name = 'applevalley_rem.tif')
hallmeadows_uav_rem = load_dtm(data_url = hallmeadows_rem_url, 
                          site_name = 'hallmeadows',
                          file_name = 'hallmeadows_rem.tif')
highway93_lidar_dtm = load_dtm(data_url = highway93_lidar_dtm_url, 
                          site_name = 'highway93',
                          file_name = 'highway93_lidar_dtm.asc')
applevalley_lidar_dtm = load_dtm(data_url = applevalley_lidar_dtm_url, 
                          site_name = 'applevalley',
                          file_name = 'applevalley_lidar_dtm.asc')
hallmeadows_lidar_dtm = load_dtm(data_url = hallmeadows_lidar_dtm_url, 
                          site_name = 'hallmeadows',
                          file_name = 'hallmeadows_lidar_dtm.asc')

# Lists of UAV DTMs and REMs
uav_dtm_list = [highway93_uav_dtm, 
                applevalley_uav_dtm, 
                hallmeadows_uav_dtm]

uav_rem_list = [highway93_uav_rem, 
                applevalley_uav_rem, 
                hallmeadows_uav_rem]

lidar_dtm_list = [highway93_lidar_dtm,
                 applevalley_lidar_dtm,
                 hallmeadows_lidar_dtm]


# In[6]:


#lidar_crs = highway93_lidar_dtm_local.rio.crs
lidar_dtm_path_list = [highway93_lidar_dtm_url, 
                      applevalley_lidar_dtm, 
                      hallmeadows_lidar_dtm]


# # Process LiDAR Data

# In[14]:


def reproject_match_lidar(site_uav_rem, lidar_path, lidar_crs, site_name):
    """
    Loads the lidar DTM, reprojects and matches the resolution and boundary of the UAV REM. 
    Saves as a tif file for use in RiverREM
    
    Parameters
    ------------   
    site_uav_rem: dataarray
        The rem to reproject and match.

    lidar_path: str
        Path to LiDAR dtm.
        
    lidar_path: int
        Original crs of the LiDAR dtm.
        
    Returns
    -------
    lidar_dtm_match: dataarray.
        The processed lidar dtm.
    """
    # Create dataarray for lidar DTM
    lidar_dtm = rxr.open_rasterio(lidar_path, masked=True)
    
    # Write CRS to lidar_dtm (2876); remove this step once link updated
    lidar_dtm_crs = lidar_dtm.rio.write_crs(lidar_crs)
    
    # Reproject/match lidar DTM to UAV REM
    #lidar_dtm_match = lidar_dtm_crs.rio.reproject_match(site_uav_rem)
    
    # Save the clipped lidar dtm as raster for use in RiverREM
    #lidar_dtm_match.rio.to_raster(site_name, ("{}_lidar_dtm_clipped.tif").format(site_name))
    
    #return lidar_dtm_match
    return lidar_dtm_crs


# In[16]:


# Load dtm for example site for blog post
applevalley_lidar_dtm_matched = reproject_match_lidar(applevalley_uav_rem, 
                                                      lidar_path =applevalley_lidar_dtm_url, 
                                                      lidar_crs = 2876,
                                                      site_name='applevalley')

