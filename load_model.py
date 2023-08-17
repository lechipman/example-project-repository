#!/usr/bin/env python
# coding: utf-8

# In[1]:


# Imports
import os
import pathlib
import zipfile

import matplotlib.pyplot as plt
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
    

# Function to download and load dtm as data array
def load_dtm(site_name, data_url, file_name):
    """Creates DataArray of Elevation Model Data
    
    Parameters
    ----------
    site_name: str
        The name of the site.
    data_url: str
        Url to the dataset (a .tif or zipfile containing .asc and .prj).
    file_name: str
        The name of the datafile.
        
    Returns
    ---------
    dtm : dataarray
        A dataarray of the elevation model.

    """
    
    override_cache = False
    data_dir = site_name
    data_path = os.path.join(data_dir, file_name)
    
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
            
    # If zip file, decompress
    if '.zip' in file_name:
        with zipfile.ZipFile(data_path, 'r') as lidar_zipfile:
            lidar_zipfile.extractall(data_dir)
        data_path=os.path.join(data_dir, 
                               '{}_lidar'.format(site_name), 
                               '{}_lidar.asc'.format(site_name))
            
    # Open and plot the UAV DTMs
    try:
        dtm = rxr.open_rasterio(data_path, masked=True)
        return dtm
    except:
        print('file type not supported, check your download')


# In[1]:


# Function to add rems and dtms to dictionary dictionary
def get_uav_dtms(site_data_dictionary):
    """
    Adds UAV info to dictionary.
    
    Parameters
    -------------
    site_data_dictionary: list
        List of the dictionaries with site data.
    
    Returns
    ------------
    site_data_dictionary: list
        List of dictionaries with dtm/rem url and filenames added.
    
    """
    for site in site_data_dictionary:
        site['uav_rem'] = load_dtm(data_url=('https://zenodo.org/record/'
                                             '8218054/files/{}_uav_rem.tif?download=1'
                                             .format(site['site_name'])), 
                                     site_name=site['site_name'],
                                     file_name=('{}_rem.tif'
                                                .format(site['site_name'])))
        site['uav_dtm'] = load_dtm(data_url=('https://zenodo.org/record/'
                                             '8218054/files/{}_uav_dtm.tif?download=1'
                                             .format(site['site_name'])), 
                                     site_name=site['site_name'],
                                     file_name=('{}_dtm.tif'
                                                .format(site['site_name'])))
            
    return site_data_dictionary


# In[ ]:


# Function to create dictionary to store info for lidar download
def get_lidar_url(site_names):
    """
    Creates a dictionary to store info for lidar download
    
    Parameters
    -------------
    site_names: list
        List of the site names.
    
    Returns
    ------------
    site_lidar_urls: list
        List of dictionaries with sitename, lidar url, and zip filename.
    
    """
    site_lidar_urls = []
    for site_name in site_names:
        site_lidar_urls.append({
            'site_name': site_name,
            'lidar_url': ('https://github.com/lechipman/'
                          'watershed-project/releases/download/v2.0.0/'
                          '{}_lidar.zip'.format(site_name)),
            'zip_filename': ('{}_lidar.zip'.format(site_name))
    })
    return site_lidar_urls


# In[ ]:


##Function to get the bounding polygon and save as gdf
def get_boundary_gdf(data_url, site_name):
    """Downloads boundary shapefiles and open as a gdf
    
    Parameters
    ------------
    data_url: str
        Url for the boundary shapefiles (zipfile)
    
    site_name: str
        The site name.
        
    Returns
    ------------
    gdf: geodataframe
        A geodataframe containing the boundary geometry.
    """
    override_cache = False
    data_path = os.path.join('shapefiles.zip')
     
    # Cache data file
    if (not os.path.exists(data_path)) or override_cache:
        print('{} does not exist. Downloading...'.format(data_path))
        # Download full data file as zipfile
        response = requests.get(data_url)

        # Write in respose content using context manager
        with open(data_path, 'wb') as data_file:
            data_file.write(response.content)
            
    with zipfile.ZipFile(data_path, 'r') as shape_zipfile:
        shape_zipfile.extractall(working_dir)
    data_path=os.path.join('shapefiles',
                           '{}_bounding_polygon'.format(site_name),
                           'Bounding_Polygon.shp')
    
    # Open the bounding polygon as gdf
    try:
        gdf = gpd.read_file(data_path)
        return gdf
    except:
        print('There is no bounding polygon for the {} site, ' 
              'skipping this site'.format(site_name))
        

# In[ ]:


# Function to clip the LiDAR and UAV DTMs to the REM bounding polygon
def dtm_clip(site_name, site_dtm, clip_gdf, is_lidar):
    """
  Clips the UAV and LiDAR DTM to the area of interest (AOI) using a 
  supplied shapefile. Reprojects the LiDAR to match UAV CRS.

  Parameters
  ----------
  site_name: Str
      Name of the site.
  site_dtm: DataArray
      The lidar or uav dtm to clip.
  clip_gdf: Geodataframe
      GDF of the AOI.
  is_lidar: Bool.
      Is the dtm from lidar? True = yes, False = no.

  Returns
  -------
  clipped_dtm = DataArray
      The clipped raster dataset.
  """

    # If lidar file, set path and reproject
    if is_lidar == True:  
        raster_path=os.path.join('{}'.format(site_name), 
                                 '{}_lidar_dtm.tif'.format(site_name))
        site_dtm = site_dtm.rio.reproject("EPSG:4326")
    
    # else, if uav file, set path but don't reproject
    else:
        raster_path=os.path.join('{}'.format(site_name), 
                                 '{}_dtm.tif'.format(site_name))   
    
    clipped_dtm = (site_dtm
                   .squeeze()
                   .rio.clip(clip_gdf.geometry, crs=clip_gdf.crs))
    
    # Save the clipped lidar dtm as raster for use in RiverREM function
    clipped_dtm.rio.to_raster(raster_path)
    
    return clipped_dtm
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
            print('{} does not exist. Creating...'.format(uav_out_dir))
            os.makedirs(uav_out_dir)
    uav_rem_path = os.path.join(uav_out_dir, 
                                  ('{}_dtm_REM.tif').format(site_name))

    # Run the REMMaker if the path to the REM does not already exist
    if (not os.path.exists(uav_rem_path)) or override_cache:
        print('Creating REMs for your sites. Please be patient, this '
              'step may take awhile...')
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
        print('The UAV REMMaker REM already exists. Not running REMMaker')


# In[ ]:


def run_rem_maker_lidar(site_name, k=100):
    """Run the REMMaker tool on LiDAR DTM
    
     Parameters
    -----------
    site_name: str
        Name of the site with existing DTM.
    k: int
        Number of interpolation points.
        
    Returns
    ----------
    '{site_name}_lidar_dtm_REM.tif': image saved locally
        REM image file.
    """
    
    # Input the DTM file path and desired output directory
    override_cache = False
    lidar_dtm_path = os.path.join(site_name, '{}_lidar_dtm.tif'.format(site_name))
    lidar_out_dir = os.path.join(site_name, 'remmaker_lidar')
    if (not os.path.exists(lidar_out_dir)) or override_cache:
            print('{} does not exist. Creating...'.format(lidar_out_dir))
            os.makedirs(lidar_out_dir)
    lidar_rem_path = os.path.join(lidar_out_dir, 
                                  ('{}_lidar_dtm_REM.tif').format(site_name))

    # Run the REMMaker if the path to the REM does not already exist
    if (not os.path.exists(lidar_rem_path)) or override_cache:
        print('Creating REMs for your sites. Please be patient, this '
              'step may take awhile...')
        rem_maker = REMMaker(dem=lidar_dtm_path, 
                             out_dir=lidar_out_dir, 
                             interp_pts=1000, 
                             k=100)

        # clear OSM cache
        clear_osm_cache()

        # create an REM
        rem_maker.make_rem()

        # create an REM visualization with the given colormap
        rem_maker.make_rem_viz(cmap='mako_r')

    else:
        print('The LiDAR REMMaker REM already exists. Not running REMMaker')


# In[3]:


# Function to plot elevation models
def plot_model(model, title, coarsen, ax, xpix=1, ypix=1):
    """
    Creates a plot of the DTM or REM.
    
    Parameters
    ------------
    model: dataarray
        The dataarray to plot.

    title: str
        The title of the plot.
    
    xpix, ypix: int, int
        The number of pixels to average with coarsen function.
        
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
        model = (model.coarsen(x=xpix, y=ypix, boundary='trim')
                 .mean().squeeze())
    # Plot DTM
    model.plot(ax=ax)

    # Add title
    ax.set_title(title, fontsize=14) 
    ax.legend('off')
    ax.axis('off')


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

