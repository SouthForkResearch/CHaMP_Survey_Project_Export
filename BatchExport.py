import CHaMP_Survey_Data_Export_Tool
import CHaMP_Survey_Data_Project_Export
import time
import os
import glob
import sys
import traceback


def run(args):
    path_output = args.path_input if args.path_output == None else args.path_output
    if not os.path.exists(path_output):
        os.makedirs(path_output)
    # Headers for Log
    printer("Start of Batch Process for CHaMP Data Export Tool ", args.outLogFile)
    printer(str(time.asctime()), args.outLogFile)

    listFilterVisits = None
    if args.filterCSVFile is not None and os.path.isfile(args.filterCSVFile):
        import csv
        with open(args.filterCSVFile, "rt") as csvfile:
            listFilterVisits = [item for row in csv.reader(csvfile) for item in row]
            # reader = csv.reader(csvfile)
            # for row in reader:
            #     for item in row:
            #         listFilterVisits.append(item)

    # Loop through source directory
    # TODO: loop through dirs only (files throw an error).
    for year in os.listdir(args.path_input):
        for watershed in os.listdir(os.path.join(args.path_input, year)):
            for site in os.listdir(os.path.join(args.path_input, year, watershed)):
                path_site = os.path.join(args.path_input, year, watershed, site)
                for visit in os.listdir(path_site):
                    VisitID = visit.lstrip("VISIT_")
                    if listFilterVisits is None or VisitID in listFilterVisits:
                        path_topo = os.path.join(path_site, visit, "Topo")
                        list_surveygdb = glob.glob(os.path.join(path_topo, "*.gdb"))
                        list_tin = glob.glob(os.path.join(path_topo, "tin*"))
                        list_wsetin = glob.glob(os.path.join(path_topo, "wsetin*"))
                        # todo Use better try raise except here
                        if len(list_surveygdb) == 1:
                            path_output_visit = os.path.join(path_topo, args.output_folder_name) if path_output is None \
                                                    else os.path.join(path_output, year, watershed, site,
                                                    str(visit), "Topo", args.out_folder_name)
                            if not os.path.isdir(path_output_visit):
                                os.makedirs(path_output_visit)
                            # try:
                            printer("   " + site + ": START", args.outLogFile)
                            if args.project and all(len(item) == 1 for item in [list_surveygdb, list_tin, list_wsetin]):
                                tin = list_tin[0]
                                wsetin = list_wsetin[0]
                                raw_instrument_file = None
                                aux_instrument_file = None
                                if len(glob.glob(os.path.join(path_topo, "*.job"))) <> 0:
                                    raw_instrument_file = glob.glob(os.path.join(path_topo, "*.raw"))[0]
                                    aux_instrument_file = glob.glob(os.path.join(path_topo, "*.job"))[0]
                                elif len(glob.glob(os.path.join(path_topo, "*.mjf"))) <> 0:
                                    raw_instrument_file = glob.glob(os.path.join(path_topo, "*.mjf"))[0]
                                    aux_instrument_file = glob.glob(os.path.join(path_topo, "*.raw"))[0]
                                dxf_file = glob.glob(os.path.join(path_topo, "*.dxf"))[0]
                                map_images_folder = os.path.join(path_topo, "MapImages") if os.path.exists(os.path.join(path_topo, "MapImages")) else None

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
                            elif len(list_surveygdb) == 0:
                                CHaMP_Survey_Data_Export_Tool.main(list_surveygdb[0], path_output_visit)
                            else:
                                printer("   " + site + ": ERROR, does not have correct input data requirements",
                                        args.outLogFile)
                            printer("   " + site + ": COMPLETE", args.outLogFile)
                            # except:
                                # printer("   " + site + ": EXCEPTION", args.outLogFile)
                                # tb = sys.exc_info()[2]
                                # tbinfo = traceback.format_tb(tb)[0]
                                # printer("{0} \n {1}: {2}".format(tbinfo, sys.exc_type, sys.exc_value), args.outLogFile)
                        else:
                            printer("   " + str(site) + ": Data Incomplete", args.outLogFile)
                    else:
                        printer("   Visit " + str(VisitID) + " not run due to filter.", args.outLogFile)
    printer("Batch Complete", args.outLogFile)
    printer(str(time.asctime()), args.outLogFile)


def printer(string, logfile=None):  # Output messages to interpreter and log file
    print string
    if logfile:
        with open(logfile, 'a') as f:
            f.write("{}\n".format(string))


def main():
    import argparse
    parser = argparse.ArgumentParser(description="Export CHaMP Survey Data in folders or as Riverscapes Projects",
                                     epilog=r"data in 'path_input' must be in standard CHaMP structure "
                                            r"(i.e. Year/Watershed/Site/VisitID/Topo)")
    parser.add_argument('path_input', help='Path to data', type=str)
    parser.add_argument('--path_output', help='Path to outputs', type=str, default=None)
    parser.add_argument('--outLogFile', help="output log file for batch process", type=str)
    parser.add_argument('--filterCSVFile', help='csv file with visitID to filter', type=str)
    parser.add_argument('--out_folder_name',
                        help='name of new folder in visit folder to save exported data',
                        type=str,
                        default="GISLayers")
    parser.add_argument('--project', help="Export topo data as Riverscapes Project", action="store_true", default=False)

    args = parser.parse_args()
    run(args)


if __name__ == '__main__':
    main()
