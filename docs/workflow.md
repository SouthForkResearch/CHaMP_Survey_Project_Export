---
title: SFR Workflow for "Maude"
---
This is the proposed workflow for exporting champ surveys as Riverscapes Projects.

<img src="https://docs.google.com/drawings/d/1k5FEZbzcImuXO2uAhD3Vir9f3wy4G4mnIwZymx0Yi3Y/pub?w=1726&amp;h=1084">

## Download Data

1. Make sure `CHaMP Automation` repo is pulled and any dependencies are up to date.
2. Create a folder to store downloaded data.
3. Open an OSGEO command line window
4. Run `python APIDownload_byType.py` with the following parameters:
   1. ​
5. Close the command line window.
6. Review the log file for the results of the download.

> **Verify** at this point that all of the champ visits survey data downloaded to a visit level folder and unzipped to a "Topo" folder.

## Generate Channel Unit CSV

1. Make sure latest CHaMP workbench is downloaded, and the latest visit data is synced to the database.
2. Highlight all of the visits that channel units should be generated for.
3. Click `Tools/Generate ChannelUnit CSV Files...` to generate the files.
4. Close the workbench.

> **Verify** at this point that all of the champ visits have a `ChannelUnits.csv` file in the "Topo" folders.

## Batch Export Riverscapes Projects

1. Make sure the latest changes from the `CHaMP Survey Data Export Tool` repo are pulled and any dependencies are up to date.
2. Open ESRI/ArcGIS Python command line window.
3. Run `python BatchExport.py` with the following parameters:
   1. ​

> **Verify** at this point that all of the champ visits have a `GISLayers` Folder with a `project.rs.xml` file and associated GIS data.

## Run RBT/GCD

1. ​

> **Verify** at this point that all of the champ visits have run through RBT/GCD and have metric values.

## Upload Data to CHaMP API

1. ​

> **Verify** at this point that all of the champ visits have a `GISLayers` Folder with a `project.rs.xml` file and associated GIS data.

## Backup/ Local Storage of Survey GDB's

1. ​

> **Verify** at this point that all of the champ visits Survey Data and RBT/GCD results are stored in the local backup location.