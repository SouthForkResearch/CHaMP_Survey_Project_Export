#!/usr/bin/env python

"""
    Tool for converting a CHaMP SurveyGeodatabase into open-format GIS datasets.
"""
import os 
import shutil
import sys
import time
import arcpy
import CHaMP_Data


def main(strInputSurveyGDB,strOutputPath):
    
    print "Starting CHaMP Survey Export Tool at " + str(time.asctime())
    print "Input SurveyGDB: " + str(strInputSurveyGDB)
    print "Output Path: " + str(strOutputPath)

    reload(CHaMP_Data)
    SurveyGDB = CHaMP_Data.SurveyGeodatabase(strInputSurveyGDB)
    
    listTables = []
   

    ## OutputWorkspace Prep
    ### http://stackoverflow.com/questions/185936/delete-folder-contents-in-python ###
    print "Checking output directory..."
    for file in os.listdir(strOutputPath):
        file_path = os.path.join(strOutputPath, file)
        try:
            if os.path.isfile(file_path):
                print "Deleting existing file: " + str(file_path)
                os.unlink(file_path)
            elif os.path.isdir(file_path): 
                shutil.rmtree(file_path)
                print "Deleting existing directory: " + str(file_path)
        except Exception, e:
            print e
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

    print "Export Complete  at " + str(time.asctime())        
            
    return


if __name__ == "__main__":

    main(sys.argv[1],
         sys.argv[2])