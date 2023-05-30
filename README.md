# Watershed Project Repository

This is the repository for Julia and Lindsay's Earth Analytics Graduate Certificate Project (Spring-Summer 2023).

Find our completed blog post at watershed_project.html or run it yourself with the watershed_project jupyter notebook.

## Summary
This repositiory contains initial code, data, and instructions to demonstrate an expoloratory effort in using Digital Terrain Models (DTM's) saved in GitHub and running the REMMaker tool in the [RiverREM](https://github.com/OpenTopography/RiverREM) python library to generate a Relative Elevation Model (REM) over one of five study sites (Highway 93, Boulder, CO) for the purposes of floodplain mapping. The overall goal of the project is to create and compare REMs created from the RiverREM library and the [Colorado Hazard Mapping](https://coloradohazardmapping.com/) tool in ArcGIS. When complete, this project will provide an open, reporducible method to create REMs from existing DTMs. It will also compare the REMs created from DTMs generated from drone imagery with those created from LiDAR. This repository will provide information on the best ways to create REMs in terms of accuracy as well as effort, resources, etc.

## Collaborators and Acknowledgements
Julia Sobczak, Lindsay Chipman, Matthew Bitters with the [Watershed Center](https://watershed.center/), and University of Colorado [Earth Lab](https://earthlab.colorado.edu/)

## Environment Requirements
How to install your environment
  * Start with [instructions for installing the ea-python environment](https://www.earthdatascience.org/workshops/setup-earth-analytics-python/setup-python-conda-earth-analytics-environment/)
  *  Install [OpenTopography RiverREM package](https://github.com/OpenTopography/RiverREM)

  ```bash
  conda install -c conda-forge riverrem
  ```

## Data Access
  * For this assignment, we hosted preprocesed data on a github release. Data was from the [Watershed Center](https://watershed.center/)
  * Please fork this repository and pull it to your local computer to run the code fully

## Workflow
 * Follow the environment installation instructions above. Run the jupyter notebook. It will import the needed librarys, including RiverREM and plot_site_map.py, as well as the data (hosted on github, see data access above) to run from start to finish. The result is a preliminary REM for one of the five study sites. 
