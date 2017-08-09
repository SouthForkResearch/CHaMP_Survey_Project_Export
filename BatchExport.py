import CHaMP_Survey_Data_Export_Tool
import CHaMP_Survey_Data_Project_Export
import time
import os
import glob
import sys
import traceback
import sqlite3


def run(args):
    path_output = args.path_input if args.path_output is None else args.path_output
    if not os.path.exists(path_output):
        os.makedirs(path_output)
    # Headers for Log
    printer("Start of Batch Process for CHaMP Data Export Tool ", args.outLogFile)
    printer(str(time.asctime()), args.outLogFile)

    yearsFilter = args.years.split(",") if args.years is not None else None
    sitesFilter = args.sites.split(",") if args.sites is not None else None
    watershedsFilter = args.watersheds.split(",") if args.watersheds is not None else None
    visitsFilter = args.visits.split(",") if args.visits is not None else None

    conn_log = sqlite3.connect(os.path.join(path_output, "export_log.db"))
    cursor = conn_log.cursor()
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
    if not any("SurveyExports" in tablename for tablename in cursor.fetchall()):
        conn_log.execute('''CREATE TABLE SurveyExports (timestamp text, 
                                                        year text, 
                                                        watershed text, 
                                                        site text, 
                                                        visit text, 
                                                        status text,
                                                        message text)''')
        conn_log.commit()

    # Loop through source directory
    for year in [item for item in os.listdir(args.path_input) if os.path.isdir(os.path.join(args.path_input, item))]:
        if yearsFilter is None or year in yearsFilter:
            path_year = os.path.join(args.path_input, year)
            for watershed in [item for item in os.listdir(path_year) if os.path.isdir(os.path.join(path_year, item))]:
                if watershedsFilter is None or watershed in watershedsFilter:
                    path_watershed = os.path.join(path_year, watershed)
                    for site in [item for item in os.listdir(path_watershed) if os.path.isdir(os.path.join(path_watershed, item))]:
                        if sitesFilter is None or site in sitesFilter:
                            path_site = os.path.join(path_watershed, site)
                            for visit in [item for item in os.listdir(path_site) if os.path.isdir(os.path.join(path_site, item))]:
                                VisitID = visit.lstrip("VISIT_")
                                if visitsFilter is None or VisitID in visitsFilter:
                                    path_topo = os.path.join(path_site, visit, "Topo")
                                    list_surveygdb = glob.glob(os.path.join(path_topo, "*.gdb"))
                                    list_tin = glob.glob(os.path.join(path_topo, "tin*"))
                                    list_wsetin = glob.glob(os.path.join(path_topo, "wsetin*"))
                                    if len(list_surveygdb) == 1:
                                        path_output_visit = os.path.join(path_topo, args.output_folder_name) if path_output is None \
                                                                else os.path.join(path_output, year, watershed, site,
                                                                str(visit), "Topo", args.out_folder_name)
                                        if not os.path.isdir(path_output_visit):
                                            os.makedirs(path_output_visit)
                                        try:
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
                                                row = (str(time.asctime()), year, watershed, site, str(VisitID), "Success", "Survey exported as Riverscapes Project.")
                                                cursor.execute("INSERT INTO SurveyExports VALUES (?,?,?,?,?,?,?)", row)
                                                conn_log.commit()
                                                printer("   " + site + ": COMPLETE", args.outLogFile)
                                            elif len(list_surveygdb) == 0:
                                                CHaMP_Survey_Data_Export_Tool.main(list_surveygdb[0], path_output_visit)
                                                row = (str(time.asctime()), year, watershed, site, str(VisitID), "Success", "Survey exported.")
                                                cursor.execute("INSERT INTO SurveyExports VALUES (?,?,?,?,?,?,?)", row)
                                                conn_log.commit()
                                                printer("   " + site + ": COMPLETE", args.outLogFile)
                                            else:
                                                printer("   " + site + ": ERROR, does not have correct input data requirements",
                                                        args.outLogFile)
                                                row = (str(time.asctime()), year, watershed, site, str(VisitID), "Error", "Data Incomplete")
                                                cursor.execute("INSERT INTO SurveyExports VALUES (?,?,?,?,?,?,?)", row)
                                                conn_log.commit()
                                        except:
                                            printer("   " + site + ": EXCEPTION", args.outLogFile)
                                            tb = sys.exc_info()[2]
                                            tbinfo = traceback.format_tb(tb)[0]
                                            printer("{0} \n {1}: {2}".format(tbinfo, sys.exc_type, sys.exc_value), args.outLogFile)
                                            traceback.print_exc(file=sys.stdout)
                                            row = (str(time.asctime()), year, watershed, site, str(VisitID), "Exception", traceback.format_exc())
                                            cursor.execute("INSERT INTO SurveyExports VALUES (?,?,?,?,?,?,?)", row)
                                            conn_log.commit()
                                    else:
                                        printer("   " + str(site) + ": Data Incomplete", args.outLogFile)
                                        row = (str(time.asctime()), year, watershed, site, str(VisitID), "Error", "Data Incomplete")
                                        cursor.execute("INSERT INTO SurveyExports VALUES (?,?,?,?,?,?,?)", row)
                                        conn_log.commit()
                                else:
                                    printer("   Visit " + str(VisitID) + " not run due to filter.", args.outLogFile)
                                    row = (str(time.asctime()), year, watershed, site, str(VisitID), "Warning", "Not exported due to filter.")
                                    cursor.execute("INSERT INTO SurveyExports VALUES (?,?,?,?,?,?,?)", row)
                                    conn_log.commit()
    printer("Batch Complete", args.outLogFile)
    printer(str(time.asctime()), args.outLogFile)

    conn_log.commit()
    conn_log.close()


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
    parser.add_argument('--project', help="Export topo data as Riverscapes Project", action="store_true", default=False)
    parser.add_argument('--years',
                        help='(Optional) Years. One or comma delimited',
                        type=str)
    parser.add_argument('--watersheds',
                        help='(Optional) Watersheds. One or comma delimited',
                        type=str)
    parser.add_argument('--sites',
                        help='(Optional) Sites. One or comma delimited',
                        type=str)
    parser.add_argument('--visits',
                        help='(Optional) Visits. One or comma delimited',
                        type=str)
    parser.add_argument('--out_folder_name',
                        help='name of new folder in visit folder to save exported data',
                        type=str,
                        default="GISLayers")
    args = parser.parse_args()
    run(args)


if __name__ == '__main__':
    main()
