import CHaMP_Survey_Data_Export_Tool
import CHaMP_Survey_Data_Project_Export
import time
import os
import glob
import sys
import traceback
import arcpy
import csv
from zipfile import ZipFile


def run(args):
    # Headers for Log

    os.makedirs(args.path_output)

    printer("Start of Batch Process for CHaMP Data Export Tool ", args.outLogFile)
    printer(str(time.asctime()), args.outLogFile)

    listFilterVisits = []
    boolFilterVisits = False
    if os.path.isfile(args.filterCSVFile):
        boolFilterVisits = True
        with open(args.filterCSVFile, "rt") as csvfile:
            reader = csv.reader(csvfile)
            for row in reader:
                for item in row:
                    listFilterVisits.append(item)

    # Loop through source directory
    for year in os.listdir(args.path_source_data):
        for watershed in os.listdir(os.path.join(args.path_source_data, year)):
            for site in os.listdir(os.path.join(args.path_source_data, year, watershed)):
                path_site = os.path.join(args.path_source_data, year, watershed, site)
                for visit in os.listdir(path_site):
                    VisitID = visit.lstrip("VISIT_")
                    if VisitID in listFilterVisits or boolFilterVisits == False:
                        path_topo = os.path.join(path_site, visit, "Topo")
                        dict_visit = {}
                        if len(glob.glob(os.path.join(path_topo, "*.gdb"))) <> 1:
                            raise Exception
                        dict_visit['surveyGDB'] = glob.glob(os.path.join(path_topo, "*.gdb"))[0]

                        list_surveygdb = glob.glob(os.path.join(path_topo, "*.gdb"))
                        if len(list_surveygdb) == 1:
                            path_output_visit = os.path.join(path_topo, args.output_folder_name) if args.path_output is None \
                                                    else os.path.join(args.path_output, year, watershed, site,
                                                    str(visit), "Topo", args.ouput_folder_name)
                            if not os.path.isdir(path_output_visit):
                                os.makedirs(path_output_visit)
                            try:
                                printer("   " + site + ": START", args.outLogFile)
                                if args.project:

                                    tin = None
                                    wsetin = None
                                    raw_instrument_file = None
                                    aux_instrument_file = None
                                    dxf_file = None
                                    map_images_folder = None

                                    CHaMP_Survey_Data_Project_Export.export_survey_project(list_surveygdb[0],
                                                                                           tin,
                                                                                           wsetin,
                                                                                           os.path.join(path_topo, "ChannelUnits.csv"),
                                                                                           path_output_visit,
                                                                                           VisitID,
                                                                                           site,
                                                                                           watershed,
                                                                                           year,
                                                                                           raw_instrument_file,
                                                                                           aux_instrument_file,
                                                                                           dxf_file,
                                                                                           map_images_folder)
                                else:
                                    CHaMP_Survey_Data_Export_Tool.main(list_surveygdb[0], path_output_visit)
                                printer("   " + site + ": COMPLETE", args.outLogFile)
                            except:
                                printer("   " + site + ": EXCEPTION", args.outLogFile)
                                # Get the geoprocessing error messages
                                msgs = arcpy.GetMessage(0)
                                msgs += arcpy.GetMessages(2)
                                # Return gp error messages for use with a script tool
                                # arcpy.AddError(msgs)
                                # Print gp error messages for use in Python/PythonWin
                                printer("***" + msgs, args.outLogFile)
                                # Get the traceback object
                                tb = sys.exc_info()[2]
                                tbinfo = traceback.format_tb(tb)[0]
                                # Concatenate information together concerning the error into a
                                #   message string
                                pymsg = tbinfo + "\n" + str(sys.exc_type) + ": " + str(sys.exc_value)
                                # Return python error messages for use with a script tool
                                # arcpy.AddError(pymsg)
                                # Print Python error messages for use in Python/PythonWin
                                printer(pymsg + "***", args.outLogFile)
                        else:
                            printer("   " + str(site) + ": Data Incomplete", args.outLogFile)
                    else:
                        printer("   Visit " + str(VisitID) + " not run due to filter.", args.outLogFile)
    printer("Batch Complete", args.outLogFile)
    printer(str(time.asctime()), args.outLogFile)


def printer(string, logfile):  # Output messages to interpreter and log file
    f = open(logfile, 'a')
    print string
    f.write(string + "\n")
    f.close()


def main():
    import argparse
    parser = argparse.ArgumentParser(description="Export CHaMP Survey Data in folders or as Riverscapes Projects",
                                     epilog=r"data in 'path_input' must be in standard CHaMP structure (i.e. Year/Watershed/Site/VisitID/Topo)")
    parser.add_argument('path_input', help='Path to data', type=str)
    parser.add_argument('--path_output', help='Path to outputs', type=str, default=None)
    parser.add_argument('--outputLogFile', help="output log file for batch process", type=str)
    parser.add_argument('--csvFilter', help='csv file with visitID to filter', type=str)
    parser.add_argument('--out_folder_name',
                        help='name of new folder in visit folder to save exported data',
                        type=str,
                        default="GISLayers")
    parser.add_argument('--project', help="Export topo data as Riverscapes Project", action="store_true", default=False)

    args = parser.parse_args()

    run(args)


if __name__ == '__main__':
    main()
