#!/usr/bin/env python

"""
    Tool for converting a CHaMP SurveyGeodatabase into open-format GIS datasets.
"""
import os 
import shutil
import sys
import time
import CHaMP_Data
import sfr_metadata as Metadata

toolName = "CHaMP Survey Data Export Tool"
toolVersion = "1.2"

def main(strInputSurveyGDB,strOutputPath):
    start = time.time()
    print "Starting CHaMP Survey Export Tool at " + str(time.asctime())
    print "Input SurveyGDB: " + str(strInputSurveyGDB)
    print "Output Path: " + str(strOutputPath)

    ## Prepare Metadata Writer File.
    outXMLfile = os.path.join(strOutputPath,"SurveyExportMetadata.xml")
    mWriter = Metadata.Metadata.MetadataWriter(toolName,toolVersion)
    mWriter.createRun()
    mWriter.currentRun.addParameter("Input Survey GDB",strInputSurveyGDB)
    mWriter.currentRun.addParameter("Output Path",strOutputPath)

    SurveyGDB = CHaMP_Data.SurveyGeodatabase(strInputSurveyGDB)

    ## OutputWorkspace Prep
    ### http://stackoverflow.com/questions/185936/delete-folder-contents-in-python ###
    print "Checking input SuveyGDB Folder..."
    if not os.path.isdir(strInputSurveyGDB):
        print "ERROR: Input SurveyGDB directory does not exist"

    print "Checking output directory..."
    # Make sure we're not passing in some weird short string
    if strOutputPath < 3:
        print "ERROR: Output path is too short."
        return
    # Make sure the directory is writeable
    if os.path.isdir(strOutputPath) and not os.access(strOutputPath, os.W_OK):
        print "ERROR: Output Path is not writeable"
        return
    # Make the folder if it doesn't exist
    if not os.path.isdir(strOutputPath):
        print "Output Folder does not exist: Creating {0}".format(strOutputPath)
        os.makedirs(strOutputPath)

    for file in os.listdir(strOutputPath):
        file_path = os.path.join(strOutputPath, file)
        try:
            if os.path.isfile(file_path):
                print "Deleting existing file: " + str(file_path)
                mWriter.currentRun.addMessage("Info","Deleting existing file: " + str(file_path))
                os.unlink(file_path)
            elif os.path.isdir(file_path): 
                shutil.rmtree(file_path)
                print "Deleting existing directory: " + str(file_path)
                mWriter.currentRun.addMessage("Info","Deleting existing directory: " + str(file_path))
        except Exception as e:
            print e
            mWriter.currentRun.addMessage("Exception",str(e))

    ## Rasters
    for raster in SurveyGDB.getRasterDatasets():
        valstart = time.time()
        if raster.validateExists():
            print "Validated: {0} exists in {1}s".format(str(raster.filename), int(time.time() - valstart))
            start = time.time()
            raster.exportToGeoTiff(strOutputPath)
            print "Exported: {0} in {1}s".format(str(raster.filename), int(time.time() - start))
            ###Write to Log
            mWriter.currentRun.addOutput(raster.name,str(raster.filename))
        else:
            print str(raster.filename) + " does not exist."
            mWriter.currentRun.addMessage("Warning",str(raster.filename) + " does not exist.")
    ## Tables
    ###Check exist
    ###Write to Log

    ## Vector Datasets
    for vectorFC in SurveyGDB.getVectorDatasets():
        valstart = time.time()
        if vectorFC.validateExists():
            print "Validated: {0} exists in {1}s".format(str(vectorFC.filename), int(time.time() - valstart))
            start = time.time()
            vectorFC.exportToShapeFile(strOutputPath)
            print "Exported: {0} in {1}s".format(str(vectorFC.filename), int(time.time() - start))
            mWriter.currentRun.addOutput(vectorFC.Name,str(vectorFC.filename))
        else:
            print str(vectorFC.filename) + " does not exist."
            mWriter.currentRun.addMessage("Warning",str(vectorFC.filename) + " does not exist.")
    
    ## Tables
    for table in SurveyGDB.getTables():
        if table.validateExists():
            table.exportTableToXML()
            print "Info","Exported: " + str(table.filename)
            mWriter.currentRun.addOutput(table.Name,str(table.filename))
        else:
            print str(table.filename) + " does not exist."
            mWriter.currentRun.addMessage("Warning",str(table.filename) + " does not exist.")

    # Make DXF Files
    try:
        topoTinDXF = SurveyGDB.exportTopoTINDXF(strOutputPath)
        mWriter.currentRun.addOutput("TopoTinDXF",topoTinDXF)
        print "Exported " + topoTinDXF
    except:
        mWriter.currentRun.addMessage("Error", "Cannot write output TopoTIN.dxf file.")
        print "Could not Export Topo TIN DXF"
    try:
        topoSurveyDXF = SurveyGDB.exportSurveyTopographyDXF(strOutputPath)
        mWriter.currentRun.addOutput("TopoSurveyDXF",topoSurveyDXF)
        print "Exported " + topoSurveyDXF
    except:
        mWriter.currentRun.addMessage("Error", "Cannot write output SurveyTopography.dxf file.")
        print "Could not Export  Topographic Survey DXF."
    print "Export Complete  at " + str(time.asctime())
    totaltime = ( time.time() - start )
    print "Total Time: {0}s".format(totaltime)
    print "Export Complete  at " + str(time.asctime())

    # Results     
    mWriter.currentRun.addResult("last_log_timestamp","") # Proxy for the latest change


    # Write Metadata File
    mWriter.finalizeRun()
    mWriter.writeMetadataFile(outXMLfile)
            
    return

if __name__ == "__main__":

    main(sys.argv[1],
         sys.argv[2])