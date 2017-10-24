---
title: Export Survey as Riverscapes Project
---

The CHaMP Survey Export tool was created for a one-time use workflow to transform historical champ topographic surveys from ESRI proprietary formats (File GDB) into Riverscapes-structured open source formats (shapefiles, geotiff). This tool uses a class-based dataset 'library' to find data components in the historic survey and manages the appropriate changes required (i.e. field name, field types) for the conversion. A few minor geoprocessing steps are included to add missing datasets (i.e. water depth) or erroneous data (i.e. Breaklines vertices not matching topo point z-values). Finally, the data are stored in a Riverscapes structured file format and a project.rs.xml file is written to capture this structure.

## Usage

### Command Line

Input Parameters

`surveygdb` filepath to the Survey Geodatabase  
`topoTIN`  filepath to topo TIN  
`wseTIN` filepath to Water Surface TIN
`channelunitscsv` filepath to channelunit csv file
`outputprojectfolder` existing or new folder to store new project
`visitid` the visit id for the survey as string  
`site` the site id/name for the survey  
`watershed` the watershed for the survey  
`year` the year of the survey as string  
`--rawinstrumentfile`*optional* filepath of the raw instrument file(s)
`--auxinstrumentfile` *optional* filepath of the auxiliary instrument file(s)
`--dxffile` *optional*  the dxf file
`--mapimagesfolder` *optional* the Path to map images folder
