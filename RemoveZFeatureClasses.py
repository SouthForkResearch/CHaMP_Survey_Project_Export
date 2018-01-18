import arcpy
import Riverscapes
import os
import topoproject
from xml.etree import ElementTree as ET
import datetime, time


def main(topo_project_xml):

    topo_project = topoproject.TopoProject(topo_project_xml)

    repair_layer_names = ["Survey_Extent",
                          "BankfullExtent",
                          "BankfullCenterline",
                          "BankfullIslands",
                          "BankfullCrossSections",
                          "WaterExtent",
                          "WettedCenterline",
                          "WettedIslands",
                          "WettedCrossSections",
                          "ChannelUnits",
                          "ChannelUnitsField",
                          "Thalweg"]

    list_repair_fcs = [topo_project.getpath(l) for l in repair_layer_names if topo_project.getpath(l) is not None]
    for fc in list_repair_fcs:
        arcpy.env.outputMFlag = "Disabled"
        arcpy.env.outputZFlag = "Disabled"

        fc_path = os.path.dirname(fc)
        fc_name = os.path.basename(fc)
        fc_temp_name = fc_name.rstrip(".shp") + "_orig" + ".shp"
        fc_temp = os.path.join(fc_path, fc_temp_name)

        arcpy.Rename_management(fc, fc_temp)
        arcpy.FeatureClassToFeatureClass_conversion(fc_temp, fc_path, fc_name)
        arcpy.Delete_management(fc_temp)

        # Add to log.
        tree = ET.parse(os.path.join(os.path.dirname(topo_project_xml), "log.xml"))
        root = tree.getroot()
        log_attrib = {"created": str(datetime.datetime.utcnow()),
                      "tool": "Z-Enabled Polygon Repair",
                      "status": "complete"}
        node = ET.SubElement(root, "Message", log_attrib)
        node.text = "Repaired Z-Enabled settings for {}.".format(fc)
        Riverscapes.indent(root)
        out_tree = ET.ElementTree(root)
        out_tree.write(os.path.join(os.path.dirname(topo_project_xml), "log.xml"))

    return 0


if __name__ == "__main__":
    import argparse
    import sqlite3
    import traceback

    parser = argparse.ArgumentParser()
    parser.add_argument('sourcefolder',
                        help='source folder to search for projects',
                        type=str)
    parser.add_argument('--logfile',
                        type=str,
                        help='write the output of this script to a file')
    args = parser.parse_args()

    # Set up log table - could be same db, but different table.
    logfile = os.path.join(args.sourcefolder, "log.db") if args.logfile is None else args.logfile
    conn_log = sqlite3.connect(logfile)
    cursor = conn_log.cursor()
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
    if not any("ZPolygonRepair" in tablename for tablename in cursor.fetchall()):
        conn_log.execute('''CREATE TABLE ZPolygonRepair (timestamp text, 
                                                        year text, 
                                                        watershed text, 
                                                        site text, 
                                                        visit text, 
                                                        status text,
                                                        message text)''')
        conn_log.commit()

    for dirname, dirs, filenames in os.walk(args.sourcefolder):
        for filename in [os.path.join(dirname, name) for name in filenames]:
            if os.path.basename(filename) == "project.rs.xml":
                # Get project details
                try:
                    tree = ET.parse(filename)
                    root = tree.getroot()
                    visitid = root.findtext("./MetaData/Meta[@name='Visit']")
                    siteid = root.findtext("./MetaData/Meta[@name='Site']")
                    watershed = root.findtext("./MetaData/Meta[@name='Watershed']")
                    year = root.findtext("./MetaData/Meta[@name='Year']")

                    status = main(filename)

                    if status == 0:
                        row = (str(time.asctime()), year, watershed, siteid, str(visitid), "Success", "Polyons repaired")
                        cursor.execute("INSERT INTO ZPolygonRepair VALUES (?,?,?,?,?,?,?)", row)
                        conn_log.commit()
                        print("Successful Polygon Repair {}".format(row))
                    else:
                        row = (str(time.asctime()), year, watershed, siteid, str(visitid), "Error", status)
                        cursor.execute("INSERT INTO ZPolygonRepair VALUES (?,?,?,?,?,?,?)", row)
                        conn_log.commit()
                        print("Error with Polygon Repair {}".format(row))
                except:
                    row = (str(time.asctime()), year, watershed, siteid, str(visitid), 'Exception', traceback.format_exc())
                    cursor.execute("INSERT INTO ZPolygonRepair VALUES (?,?,?,?,?,?,?)", row)
                    conn_log.commit()
                    print("Exception {}".format(traceback.format_exc()))
