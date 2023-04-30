# Watershed Project Repository

Beginning a shared repository for Julia and Lindsay's watershed project
For Final Project due next week we need to add project descrtiption, environment with RiverREM, and ipynb with code to download and plot 2 data sets (idea is to use hwy93 DTMs (either download from watershed center webpage? or uplaod to github) and plot with RiverREM)


## Collaborators and Acknowledgements
Julia Sobczak, Lindsay Chipman, Matthew Bitters, and the [Watershed Center](https://watershed.center/)

## Project Description
### Background, goals
A connected, functional floodplain retains water during periods of high flow and releases it back into the stream when flows are low. Reduced connectivity results in greater magnitude of flood events and vulnerability of surrounding ecosystems to drought. Therefore, understanding connectivity can help guide water resource  management and preparing for potential natural disasters. Through this project, we aim to map floodplain connectivity at 5 target sites in the St. Vrain Basin in Boulder, CO and use the results to evaluate if desired watershed conditions are being met. We will also compare the results between UAV or LiDAR derived data, to see which performs better in terms of quantifying floodplain connectivity.

### Methods
We will use two types of data in our analysis:
1) UAV imagery (to process in Agisoft and create DTM), source: DJI Phantom 4, collected by contractor in Spring & Fall 2022
2) LiDAR data (downloaded as DTM), source: [Colorado Hazard Mapping, Airborne Snow Observatories](https://coloradohazardmapping.com/lidarDownload)

For each of these datasets, we will create digital elevation models (DEM), and digital terrain models (DTM; DEM with vegetation removed) for each site using Agisoft software. (for the lidar data, we may also use download an already created DEM/DTM available from the [Colorado Hazard site](https://coloradohazardmapping.com/lidarDownload). We will then create relative elevation models for the five DTMs with two different methods. THe first method follows the watershed center's protocol, which relies on using the Colorado Water Conservation Board’s REM Generator Tool in ArcMap to create the REM. We would use this for both UAV- and LiDAR-derived DTMs and compare the results. The second method is to use python tools (notably the RiverREM package) to create the REM.

Our end products include an REM and histogram for each of the 5 sites, created from both UAV- and LiDAR-derived data as well as a qualitative and quantitative comparison between the two data sources to suggest which method is best for The Watershed Center to replicate Ultimately, we hope to replicate the watershed's existing process using python tools to  come up with an open and reproducible analysis for generating the REMs. Potential tools are: rasterio/rioxarray (to open and view DTMs), RiverREM (to create REM), and potentially others for plotting and reproducing data downloads and setting file paths/directories. We would use this for both UAV- and LiDAR-derived DTMs and compare.

### To do
Use zenodo to create persistent url (doi), can also upload data but file size may be too large (50MB max per file, no cap on # of files)
etc.

## Environment Requirements
How to install your environment
  * Start with [instructions for installing the ea-python environment](https://www.earthdatascience.org/workshops/setup-earth-analytics-python/setup-python-conda-earth-analytics-environment/)
  *  Install [OpenTopography RiverREM package](https://github.com/OpenTopography/RiverREM)

  ```bash
  conda install -c conda-forge riverrem
  ```
  
  * OR make your own environment.ymp file based on the earth analytics python one (e.g., edit existing file to add new packages, remove packages not needed); test first

## Data Access
For next week's assignment, include complete instructions for accesing enough data to run the workflow.
  * Working urls
  * if url points at a web form, you must have complete info on what to fill in there
  * If possible, you should host data or data subset on github (note, I thnk the DTM files are too large to host, but not sure if we can share the link to google drive for user to download?)
  * * Data must include citations

> If you need to process raw data before sending it out, you can include a notebook or script for that, that I will not run.
> Include code to access 2 data sources and plot; if can't use the download, talk with Elsa for alternative

