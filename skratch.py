#!/usr/bin/env python
# coding: utf-8

# In[1]:


# Import directories
import os
import pathlib
import zipfile

import contextily as cx
import io
import matplotlib.pyplot as plt
import pandas as pd
import geopandas as gpd
import requests


# In[2]:


# Set working directory
working_dir = os.path.join(
    pathlib.Path.home(), 'earth-analytics', 'data', 'watershed-project')
if not os.path.exists(working_dir):
    print('{} does not exist. Creating...'.format(working_dir))
    os.makedirs(working_dir)
    
os.chdir(working_dir)


# In[3]:


# Download and import the site coordinates for plotting (saved on github)
sites_url='https://raw.githubusercontent.com/lechipman/watershed-project/master/UAV_gps_coords.csv'
download = requests.get(sites_url).content

# Reading the downloaded content and turning it into a pandas dataframe
sites_df = pd.read_csv(io.StringIO(download.decode('utf-8')))

# Select one location from each site to map
sites_short_df = sites_df.iloc[[0,7,17,29]]

# Create gdf of study sites
sites_gdf = gpd.GeoDataFrame(
    sites_short_df,
    geometry = gpd.points_from_xy(sites_short_df['lon'],
                                  sites_short_df['lat']),
                                  crs = 'EPSG:4326')
sites_gdf.head()


# In[4]:


# Download and cache watershed boundary dataset 
override_cache = False
wbd_10_url = (
    "https://prd-tnm.s3.amazonaws.com/StagedProducts/"
    "Hydrography/WBD/HU2/Shape/WBD_10_HU2_Shape.zip")

wbd_10_dir = 'water-boundary-dataset-hu10'
wbd_10_path = os.path.join(wbd_10_dir, wbd_10_dir + '.zip')

# Cache WBD file
if not os.path.exists(wbd_10_dir):
    os.makedirs(wbd_10_dir)
    
    if (not os.path.exists(wbd_10_path)) or override_cache:
        # Download full WBD 10 as zipfile 
        response = requests.get(wbd_10_url)

        # Write in respose content using context manager
        with open(wbd_10_path, 'wb') as wbd_10_file:
            wbd_10_file.write(response.content)
        
        # Decompress zip file
        with zipfile.ZipFile(wbd_10_path, 'r')as wbd_zipfile:
            wbd_zipfile.extractall(wbd_10_dir)


# In[5]:


# Select study area, St Vrain watershed, and save gdf
wbd_10_path = os.path.join(wbd_10_dir, 'Shape', 'WBDHU8.shp')
wbd_10_gdf = gpd.read_file(wbd_10_path)
vrain_gdf = wbd_10_gdf[wbd_10_gdf.name.str.contains('Vrain')]

# Set CRS to same as site points
vrain_crs_gdf = vrain_gdf.to_crs(crs = 'EPSG:4326')


# In[6]:


# Download Boulder County streams data and create gdf
# Source = University of Colorado, Boulder, GeoLibrary, https://geo.colorado.edu/catalog/47540-5ca23860d43267000b8c744e
stream_url = "https://geo.colorado.edu/apps/geolibrary/datasets/STREAMSx4.zip"
stream_dir = 'co_streams'
stream_path = os.path.join(stream_dir, stream_dir + '.zip')

override_cache = True
if not os.path.exists(stream_dir):
    os.makedirs(stream_dir)
    
    if not os.path.exists(stream_path) or override_cache:
        print('{} does not exist. Downloading...'.format(stream_path))

        # Open stream file
        response = requests.get(stream_url)

        # Open a local file with wb permission and write response content
        with open(stream_path, 'wb') as stream_file:
            stream_file.write(response.content) 

        # Decompress zip file
        with zipfile.ZipFile(stream_path, 'r') as stream_zipfile:
            stream_zipfile.extractall(stream_dir)


# In[7]:


stream_gdf = gpd.read_file(stream_path)

# Set CRS to same as site points
stream_crs_gdf = stream_gdf.to_crs(crs = 'EPSG:4326')

# Clip stream data to st vrain watershed boundary
stream_clipped_gdf = stream_crs_gdf.clip(vrain_crs_gdf)


# In[9]:


# Plot Watershed and Streams
def plot_study_sites():
    """Creates a map of study sites in the St. Vrain Watershed"""
    
    fig, ax = plt.subplots(1, 1, figsize=(8, 16))
    ax.set_title("Site Locations in the St. Vrain Watershed",
                 pad=20,
                fontsize=16)

    stream_clipped_gdf.plot(ax=ax, color='blue')
    vrain_crs_gdf.plot(ax=ax, facecolor='cyan', alpha=0.5)

    site_symbol_dict = {
        'AV GCP1': '*',
        'HW93 GCP1': '*',
        'LEG1-GCP1': '*',
        'VV GCP1' : '*'
    }

    site_name_dict = {
        'AV GCP1': 'Apple Valley North',
        'HW93 GCP1': 'Highway 93',
        'LEG1-GCP1': 'Legacy 1',
        'VV GCP1' : 'Van Vleet'
    }


    for i, gdf in sites_gdf.groupby('name'):
        gdf.plot(ax=ax,
                 marker=site_symbol_dict[i],
                 label=site_name_dict[i],
                 markersize=150,
                legend=True)

    ax.legend()
    ax.set_axis_off()
    plt.legend(bbox_to_anchor=(1, 1), loc='upper left', borderaxespad=0);
    #sites_gdf.plot(ax=ax, color='black', marker = 'x', markersize=40)

    cx.add_basemap(ax, crs=vrain_crs_gdf.crs, zoom=10)

