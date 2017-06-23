# CHaMP Survey Export Tool

The CHaMP Survey Export tool exports CHaMP Survey data: 

* from ESRI File-Geodatabase Feature Classes to shapefile format
* from ESRI File-Geodatabase raster datasets to geotiff format
* select features as [AutoCAD DXF format](CAD_Exports "AutoCAD DXF format")
* select features as CSV
* ESRI TIN Components as Shapefiles

## Installation

**[Downloads and Release Notes](ReleaseNotes)**

### Dependencies

* ESRI ArcGIS 10.1 (arcpy)
* Python 2.7
* CHaMP_Data.py (comes with installation)

### Survey Data Export Tool
## Usage

This tool can be run from the command line 

### Parameters

***Input Survey GDB***

Path and name (including .gdb) of input CHaMP Survey GDB.

***Output Path***

Path of directory to create outputs. *All existing files will be deleted.*


### Batch Export Tool
## Usage

This tool can be run from the command line 

### Parameters

***Path of the data***

Path of directory above the site level, in CHaMP Workbench Folder Structure. This is commonly the "Watershed" folder i.e. .../Year/Watershed/Site/Visit/Topo/Survey.gdb

***Output Path***

Path of directory to create outputs. path/site/visit . *All existing files will be deleted.*