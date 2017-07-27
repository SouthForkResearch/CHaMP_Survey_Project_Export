---
title: Patch Process Survey Exports
---

This Batch Export script can be used to export several visits at one time and can be used to export both Riverscapes Projects and Flat File exports.

# Tool Usage

The batch export script should be run from the command line using the ESRI/arcpy python installation.

1. Make sure all required data for the visits that need to be exported are downloaded to a local folder, and are in the standard champ directory structure. 
   1. At a minimum the survey geodatabase is required for a [flat folder](folder_export) export.
   2. To export the project as a Riverscapes Project, the survey geodatabase, tin, water surface tin, and channelunits.csv (generated from the CHaMP Workbench) are required. The raw and aux instrument and dxf files are optional, however it is highly recommended that they be included as well.
2. Run the `Batch_Export.py` script with the following arguments:
   1. `path_input` The base-level path to the data (i.e. the folder that contains the "year" folders)
   2. `--path_output` *optional* The base-level output path. If this is not specified, the outputs will be stored in the same path as the inputs.
   3. `--outputLogFile` *optional* output log file for the batch process.
   4. `--csvFilter ` *optional* csv file with list of visits to process. If this is not specified, all visits found in the input path will be processed.
   5. `--out_folder_name` *optional* specify an output folder name to store the exported data in each visit's "Topo" folder. If no folder name is specified, "GISLayers" will be used.
   6. `--project` *flag* used to export the visit as a Riverscapes Project. If this flag is not set, the visit will be exported as a "flat file" export.