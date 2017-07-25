---
title: CHaMP Survey Export Tool
---

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

<h2>Run CHaMP Data Export Tool (aka Harold)</h2>

<p>This tool takes the expected feature classes from a CHaMP Survey Geodatabase and exports them to shapefiles. It also takes all expected rasters and exports them to tiff files. It will not include any feature classes or rasters which are copies and have a slightly different name than the original data.</p>

Notes: 
Process one year of data at a time.

	
### Steps To Run Harold:
1. Pull Harold Code from [Survey Data Export](https://github.com/SouthForkResearch/CHaMP_Survey_Project_Export) repository.
2. Pull CrewUploadedSurveyGDB.zip from AWS to a folder on c:  
3. Unzip CrewUploadedSurveyGDB.zip to Visit_DataForHarold  
4. In the Windows Start Menu Type: <strong>cmd</strong> to open a command window.
5. Type `python`, the path to the tool, the input data folder path and name, the output folder path and name, the batch log file path, and the list of visits to run (optional). For example:
	
`python "C:\GIS\Tools\CHaMP_Survey_Data_Export_Tool\BatchExport.py" C:\CHaMP\Processing\Visit_DataForHarold C:\SurveyDataExportFiles\CHaMP C:\SurveyDataExportFiles\BatchLog.txt C:\VisitRunLists\DET_CHaMP_AL_yyyymmdd.csv)`
	
Where:  
Tool path: `C:\GIS\Tools\CHaMP_Survey_Data_Export_Tool\BatchExport.py`  
Input Data folder: `C:\CHaMP\Processing\Visit_Data\Visit_DataForHarold`  
Output folder: `C:\SurveyDataExportFiles\CHaMP`  
Batch Log file path: `C:\SurveyDataExportFiles\BatchLog.txt`  
List of Visits to run: `C:\VisitRunLists\DET_CHaMP_AL_yyyymmdd.csv`  
				
6. Hit Enter
7. The exported data will be located in the \year\watershed\site name\Visit_xxxx\Topo\GISLayers\

### Uploading Data to AWS  
8.  Double Click on the CHaMP_Upload_SurveyExport.bat file.  The script will show a prompt when it is finished.
