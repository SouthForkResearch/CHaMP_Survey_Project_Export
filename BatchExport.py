import CHaMP_Survey_Data_Export_Tool
import time
import os
import glob
import sys
import traceback
import CHaMP_Data
import arcpy
import csv

def run(directorySource,directoryOutput,outLogFile,filterCSVFile=""):
    # Headers for Log
 
    os.makedirs(directoryOutput)
 
    printer("Start of Batch Process for CHaMP Data Export Tool ",outLogFile)
    printer(str(time.asctime()),outLogFile)
    
    listFilterVisits = []
    boolFilterVisits = False 
    if os.path.isfile(filterCSVFile):
        boolFilterVisits = True
        with open(filterCSVFile,"rt") as csvfile:
            reader = csv.reader(csvfile)
            for row in reader:
                for item in row:
                    listFilterVisits.append(item)
    
    # Loop through source directory
    for year in os.listdir(directorySource):
        for watershed in os.listdir(directorySource + "\\" + year):
            for site in os.listdir(directorySource + "\\" + year + "\\" + watershed):
                directorySite = directorySource + "\\" + year + "\\" + watershed + '\\' +  site
                for visit in os.listdir(directorySite):
                    VisitID = visit.lstrip("VISIT_")
                    if VisitID in listFilterVisits or boolFilterVisits == False:
                        directoryCurrent = directorySite + "\\" + visit + "\\Topo"
                        listsurveyGDB = glob.glob(directoryCurrent + "\\*.gdb")
                        if len(listsurveyGDB) == 1:
                            SurveyGDB = CHaMP_Data.SurveyGeodatabase(listsurveyGDB[0])
                            if directoryOutput == "":
                                outputFolder = directorySource + "\\" + year + "\\" + watershed + '\\' +  site + '\\' + str(visit) + "\\Topo\\GISLayers"
                            else:
                                outputFolder = directoryOutput + "\\" + year + "\\" + watershed + '\\' +  site + '\\' + str(visit) + "\\Topo\\GISLayers"
                            if not os.path.isdir(outputFolder):
                                os.makedirs(outputFolder)

                            try:
                                printer("   " + site + ": START",outLogFile)
                                CHaMP_Survey_Data_Export_Tool.main(SurveyGDB.filename,outputFolder)
                                printer("   " + site + ": COMPLETE",outLogFile)
                            except:
                                printer("   " + site + ": EXCEPTION",outLogFile)
                                # Get the geoprocessing error messages
                                msgs = arcpy.GetMessage(0)
                                msgs += arcpy.GetMessages(2)
                                # Return gp error messages for use with a script tool
                                #arcpy.AddError(msgs)
                                # Print gp error messages for use in Python/PythonWin
                                printer("***" + msgs,outLogFile)
                                # Get the traceback object
                                tb = sys.exc_info()[2]
                                tbinfo = traceback.format_tb(tb)[0]
                                # Concatenate information together concerning the error into a
                                #   message string
                                pymsg = tbinfo + "\n" + str(sys.exc_type)+ ": " + str(sys.exc_value)
                                # Return python error messages for use with a script tool
                                #arcpy.AddError(pymsg)
                                # Print Python error messages for use in Python/PythonWin
                                printer( pymsg + "***",outLogFile)
                        else:
                            printer("   " + str(site) + ": Data Incomplete",outLogFile)
                    else:
                        printer("   Visit " + str(VisitID) + " not run due to filter.",outLogFile)
    printer("Batch Complete",outLogFile)
    printer(str(time.asctime()),outLogFile)

def printer(string,logfile): # Output messages to interpreter and log file
    f = open(logfile, 'a')
    print string
    f.write(string + "\n")
    f.close()

if __name__ == '__main__':
    inputSourceDirectory = sys.argv[1] # Top Level Monitoring Data Folder
    outputDirectory = sys.argv[2]
    outputLogFile = sys.argv[3]
    
    if len(sys.argv) == 5:
        csvFilter = sys.argv[4]
    else:
        csvFilter = ""

    run(inputSourceDirectory,outputDirectory,outputLogFile,csvFilter)
