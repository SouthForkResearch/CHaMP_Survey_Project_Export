import CHaMP_Survey_Data_Export_Tool
import time
import os
import glob
import sys
import traceback
import CHaMP_Data
import arcpy

def run(directorySource,directoryOutput):
        # Headers for Log
    printer("Start of Batch Process for CHaMP Data Export Tool ",directoryOutput)
    printer(str(time.asctime()),directoryOutput)

    # Loop through source directory
    for year in os.listdir(directorySource):
        for watershed in os.listdir(directorySource + "\\" + year):
            for site in os.listdir(directorySource + "\\" + year + "\\" + watershed):
                directorySite = directorySource + "\\" + year + "\\" + watershed + '\\' +  site
                for visit in os.listdir(directorySite):
                    directoryCurrent = directorySite + "\\" + visit + "\\Topo"
                    listsurveyGDB = glob.glob(directoryCurrent + "\\*.gdb")
                    if len(listsurveyGDB) == 1:
                        SurveyGDB = CHaMP_Data.SurveyGeodatabase(listsurveyGDB[0])
                        outputFolder = directoryOutput + "\\" + year + "\\" + watershed + '\\' +  site + '\\' + str(visit)
                        if not os.path.isdir(outputFolder):
                            os.makedirs(outputFolder)
                        try:
                            printer("   " + site + ": START",directoryOutput)
                            CHaMP_Survey_Data_Export_Tool.main(SurveyGDB.filename,outputFolder)
                            printer("   " + site + ": COMPLETE",directoryOutput)
                        except:
                            printer("   " + site + ": EXCEPTION",directoryOutput)
                            # Get the geoprocessing error messages
                            msgs = arcpy.GetMessage(0)
                            msgs += arcpy.GetMessages(2)
                            # Return gp error messages for use with a script tool
                            #arcpy.AddError(msgs)
                            # Print gp error messages for use in Python/PythonWin
                            printer("***" + msgs,directoryOutput)
                            # Get the traceback object
                            tb = sys.exc_info()[2]
                            tbinfo = traceback.format_tb(tb)[0]
                            # Concatenate information together concerning the error into a
                            #   message string
                            pymsg = tbinfo + "\n" + str(sys.exc_type)+ ": " + str(sys.exc_value)
                            # Return python error messages for use with a script tool
                            #arcpy.AddError(pymsg)
                            # Print Python error messages for use in Python/PythonWin
                            printer( pymsg + "***",directoryOutput)
                    else:
                        printer("   " + str(site) + ": Data Incomplete",directoryOutput)

    printer("Batch Complete",directoryOutput)
    printer(str(time.asctime()),directoryOutput)

def printer(string,path): # Output messages to interpreter and log file
    f = open(path + '\\BatchLog.txt', 'a')
    print string
    f.write(string + "\n")
    f.close()
    #arcpy.AddMessage(str(string))

if __name__ == '__main__':
    inputSourceDirectory = sys.argv[1] # Top Level Monitoring Data Folder
    inputOutputDirectory = sys.argv[2]

    run(inputSourceDirectory,inputOutputDirectory)





