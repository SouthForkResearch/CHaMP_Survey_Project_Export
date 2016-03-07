#!/usr/bin/env python

"""
    Tool for converting a CHaMP SurveyGeodatabase into open-format GIS datasets.
"""

import sys
import arcpy
import CHaMP_Data

def main(strInputSurveyGDB,strOutputPath):
    reload(CHaMP_Data)
    SurveyGDB = CHaMP_Data.SurveyGeodatabase(strInputSurveyGDB)
    
    listTables = []
    #listFiles = []

    ## OutputWorkspace Prep
    #arcpy.env.Workspace = strOutputPath
    #for dataset in arcpy.ListDatasets():
    #    if arcpy.Exists(dataset):
    #        arcpy.Delete_management(dataset)
    #        print "Deleted Existing File: " + str(dataset)
    ### Write to Log File

    ## Rasters
    for raster in SurveyGDB.getRasterDatasets():
        if raster.validateExists():
            raster.exportToGeoTiff(strOutputPath)
            print "Exported: " + str(raster.filename)
    ###Write to Log

    ## Tables
    ###Check exist
    ###Write to Log
    
    
    for vectorFC in SurveyGDB.getVectorDatasets():
        if vectorFC.validateExists():
            vectorFC.exportToShapeFile(strOutputPath)
            print "Exported: " + str(vectorFC.filename)
        else:
            print str(vectorFC.filename) + " does not exist."
    
    for table in SurveyGDB.getTables():
        if table.validateExists():
            table.exportTableToXML()
        else:
            print str(table.filename) + " does not exist."

    print "Export Complete."        
            
    return


if __name__ == "__main__":

    main(sys.argv[1],
         sys.argv[2])