---
title: SFR Workflow for "Maude"
---
# Overview

This is the proposed workflow for exporting champ surveys as Riverscapes Projects.

<img src="https://docs.google.com/drawings/d/1k5FEZbzcImuXO2uAhD3Vir9f3wy4G4mnIwZymx0Yi3Y/pub?w=1726&amp;h=1084">

# Workflow

## Download Data

1. Make sure `CHaMP Automation` repo is pulled and any dependencies are up to date.
   1. Update env file with API credentials
   2. Run `pip install requests[security]` if not already done on that computer to avoid a bunch of warnings.
2. Create a folder to store downloaded data.
3. Open an OSGEO command line window
4. Run `python APIDownload_byType.py` with the following parameters:
   1. output folder

   2. `--filetypes Topo` The script will download the correct set of Topo files for the visit.

   3. filter by `--visits`, `--years`, `--watersheds` and/or `--sites`. 

      > Warning: if any of these filters are not specified, all visits will be downloaded!

   4. `--logfile` path to the output log

   5. `--unzip` flag to unzip the contents to a folder named "Topo" within each visit.
5. Close the command line window.
6. Review the log file for the results of the download.

> **Verify** at this point that all of the champ visits survey data downloaded to a visit level folder and unzipped to a "Topo" folder.

## Generate Channel Unit CSV

1. Make sure latest CHaMP workbench is downloaded, and the latest visit data is synced to the database.
2. Under Tools/Options, make sure the correct Monitoring Folder is specified. This should be the same  as the "OutputFolder" for downloading data.
3. Highlight all of the visits that channel units should be generated for.
4. Click `Tools/Generate ChannelUnit CSV Files...` to generate the files.
5. Close the workbench.

> **Verify** at this point that all of the champ visits have a `ChannelUnits.csv` file in the "Topo" folders.

## Batch Export Riverscapes Projects

1. Make sure the latest changes from the `CHaMP Survey Data Export Tool` repo are pulled and any dependencies are up to date.
2. Open ESRI/ArcGIS Python command line window.
3. Run `python BatchExport.py` with the following parameters:
   1. path to Monitoring Data
   2. `--project` flag to output as RS project.

> **Verify** at this point that all of the champ visits have a `GISLayers` Folder with a `project.rs.xml` file and associated GIS data.

## Run RBT/GCD

1. ​Open Workbench and prepare Input/Output files for RBT/GCD run. This folder will likely be different than the monitoring data folder.
2. Run RBT/GCD on visits.
3. Open Log/Results in workbench to evaluate the success of the run.

> **Verify** at this point that all of the champ visits have run through RBT/GCD and have metric values.

## Upload Data to CHaMP API

1. ​--In Development--

> **Verify** at this point that all of the champ visits have a `GISLayers` Folder with a `project.rs.xml` file and associated GIS data.

## Backup/ Local Storage of Survey GDB's

1. ​Zip up monitoring data and RBT Input/output folders. Store these on local computer(s) and AWS.

> **Verify** at this point that all of the champ visits Survey Data and RBT/GCD results are stored in the local backup location.
