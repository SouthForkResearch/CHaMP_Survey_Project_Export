import CHaMP_Data
import sys
import os
import shutil

def main(strInputSurveyGDB,strOutputPath):

    reload(CHaMP_Data)

    SurveyGDB = CHaMP_Data.SurveyGeodatabase(strInputSurveyGDB)

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
                os.unlink(file_path)
            elif os.path.isdir(file_path):
                shutil.rmtree(file_path)
                print "Deleting existing directory: " + str(file_path)
        except Exception as e:
            print e

    try:
        topoTinDXF = SurveyGDB.exportTopoTINDXF(strOutputPath)

    except Exception as e:
        print e
    try:
        topoSurveyDXF = SurveyGDB.exportSurveyTopographyDXF(strOutputPath)
    except Exception as e:
        print e

    print "Complete"

if __name__ == "__main__":

    main(sys.argv[1],sys.argv[2])