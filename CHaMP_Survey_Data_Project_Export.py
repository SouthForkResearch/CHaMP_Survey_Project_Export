"""
    Tool for converting a CHaMP SurveyGeodatabase into Riverscapes Project.
"""
import os
import sys
import shutil
from distutils import dir_util
import time
import traceback
import CHaMP_Data
from Riverscapes import Riverscapes
import sfr_metadata as Metadata

toolName = "CHaMP Survey Data Project Export"
toolVersion = "1.0.0"


def export_survey_project(survey_gdb,
                          topo_tin,
                          ws_tin,
                          channelunits_csv,
                          output_folder,
                          visitid,
                          siteid,
                          watershed,
                          year,
                          raw_inst_file=None,
                          aux_inst_file=None,
                          dxf_file=None,
                          mapimages_folder=None):
    """
    export a champ survey visit to Riverscapes project
    :param survey_gdb:
    :param topo_tin:
    :param ws_tin:
    :param benchmarks_csv:
    :param channelunits_csv:
    :param output_folder:
    :return:
    """

    reload(CHaMP_Data)
    reload(Riverscapes)
    start = time.time()
    print "Starting" + toolName + " at " + str(time.asctime())
    print "Input SurveyGDB: " + str(survey_gdb)
    print "Output Path: " + str(output_folder)

    ## Prepare Metadata Writer File.
    outXMLfile = os.path.join(output_folder, "SurveyExportMetadata.xml")
    mWriter = Metadata.Metadata.MetadataWriter(toolName, toolVersion)
    mWriter.createRun()
    mWriter.currentRun.addParameter("Input Survey GDB", survey_gdb)
    mWriter.currentRun.addParameter("Output Path", output_folder)

    SurveyGDB = CHaMP_Data.SurveyGeodatabase(survey_gdb)

    for key, value in SurveyGDB.projection_info().iteritems():
        mWriter.currentRun.addResult(key, value)

    ## OutputWorkspace Prep
    ### http://stackoverflow.com/questions/185936/delete-folder-contents-in-python ###
    print "Checking input SuveyGDB Folder..."
    if not os.path.isdir(survey_gdb):
        print "ERROR: Input SurveyGDB directory does not exist"

    print "Checking output directory..."
    # Make sure we're not passing in some weird short string
    if output_folder < 3:
        print "ERROR: Output path is too short."
        return
    # Make sure the directory is writeable
    if os.path.isdir(output_folder) and not os.access(output_folder, os.W_OK):
        print "ERROR: Output Path is not writeable"
        return
    # Make the folder if it doesn't exist
    if not os.path.isdir(output_folder):
        print "Output Project Folder does not exist: Creating {0}".format(output_folder)
        os.makedirs(output_folder)

    for file in os.listdir(output_folder):
        file_path = os.path.join(output_folder, file)
        try:
            if os.path.isfile(file_path):
                print "Deleting existing file: " + str(file_path)
                mWriter.currentRun.addMessage("Info", "Deleting existing file: " + str(file_path))
                os.unlink(file_path)
            elif os.path.isdir(file_path): 
                shutil.rmtree(file_path)
                print "Deleting existing directory: " + str(file_path)
                mWriter.currentRun.addMessage("Info", "Deleting existing directory: " + str(file_path))
        except Exception as e:
            print e
            mWriter.currentRun.addMessage("Exception",str(e))

    # New Project
    rs_project = Riverscapes.Project()
    rs_project.projectPath = output_folder
    rs_project.name = "CHaMP Topo Survey" if siteid is None else siteid
    rs_project.projectType = "Topo"
    rs_project.projectVersion = toolVersion

    for name, value in {"SiteID":siteid, "VisitID":visitid, "Watershed":watershed, "Year":year}.iteritems():
        rs_project.ProjectMetadata[name] = value

    dict_instrument_tag_data = {}

    if SurveyGDB.tblSurveyInfo.validateExists():
        for field, value in SurveyGDB.tblSurveyInfo.get_data():
            if field not in ["InstrumentType", "InstrumentModel"]:
                rs_project.ProjectMetadata["CrewSpecified" + str(field)] = str(value)
            else:
                dict_instrument_tag_data[str(field)] = str(value)

    # Inputs
    inputs_folder = os.path.join(output_folder, "Inputs")
    os.makedirs(inputs_folder)

    # SQLITE
    sqlite_db_template = os.path.join(os.path.realpath(__file__).rstrip(os.path.basename(__file__)), "SurveyQualityTemplate.sqlite")
    sqlite_db = os.path.join(inputs_folder, "SurveyQualityDB.sqlite")
    shutil.copyfile(sqlite_db_template, sqlite_db)

    for table in SurveyGDB.getDatasets("QA"):
        if table.validateExists():
            table.export_to_sqlite(sqlite_db)

    rs_project.addInputDataset("Survey Quality Database",
                               "SurveyQualityDB",
                               os.path.join("Inputs", "SurveyQuality.sqlite"),
                               datasettype="SurveyQualityDB")

    if raw_inst_file:
        shutil.copy2(raw_inst_file, inputs_folder)
        ds_raw = Riverscapes.Dataset()
        ds_raw.create("Instrument File", os.path.join("Inputs", os.path.basename(raw_inst_file)), type="InstrumentFile")
        ds_raw.id = "RawFile"
        ds_raw.metadata["Type"] = "RawFile"
        for name, value in dict_instrument_tag_data.iteritems():
            ds_raw.metadata[str(name)] = str(value)
        rs_project.InputDatasets["Instrument File"] = ds_raw

    if aux_inst_file:
        shutil.copy2(aux_inst_file, inputs_folder)
        rs_project.addInputDataset("Auxilliary Instrument File",
                                   "AuxFile",
                                   os.path.join("Inputs", os.path.basename(aux_inst_file)),
                                   datasettype="AuxInstrumentFile")

    # if SurveyGDB.fcQaQcRawPoints.exists:
    if SurveyGDB.fcQaQcRawPoints.validateExists():
        raw_points_shp = SurveyGDB.fcQaQcRawPoints.exportToShapeFile(inputs_folder, "QaQcPoints")
        rs_project.addInputDataset(SurveyGDB.fcQaQcRawPoints.rs_name, SurveyGDB.fcQaQcRawPoints.rs_id,
                                   os.path.join("Inputs", raw_points_shp))

    if dxf_file:
        shutil.copy2(dxf_file, inputs_folder)
        dxf_dataset = Riverscapes.Dataset()
        dxf_dataset.create("Breaklines", os.path.join("Inputs", os.path.basename(dxf_file)))
        dxf_dataset.id = "BreaklineDXF"
        dxf_dataset.metadata["FeatureClassName"] = "Polyline"
        rs_project.InputDatasets["BreaklineDXF"] = dxf_dataset

    if channelunits_csv:
        shutil.copy2(channelunits_csv, inputs_folder)
        rs_project.addInputDataset("Channel Units CSV",
                                   "channelunitcsv",
                                   os.path.join("Inputs", os.path.basename(channelunits_csv)),
                                   datasettype="CSV")

    # Survey Data Realizations
    if SurveyGDB.has_unprojected():
        unprojected_folder = os.path.join(output_folder, "SurveyDataUnProjected")
        os.makedirs(unprojected_folder)
        unprojected_realization = Riverscapes.SurveyDataRealization(False)
        unprojected_realization.create("Survey Data Unprojected")

        for dataset in SurveyGDB.get_survey_datasets(False):
            if dataset.validateExists():
                dataset.exportToShapeFile(unprojected_folder)
                ds = Riverscapes.Dataset()
                ds.create(dataset.rs_name, os.path.join("SurveyDataUnProjected", dataset.shapefile_basename()))
                ds.id = dataset.rs_id
                unprojected_realization.datasets[ds.id] = ds
                rs_project.addRealization(unprojected_realization, "survey_data_unprojected")

        if SurveyGDB.tblTransformations.validateExists():
            SurveyGDB.tblTransformations.export_to_dbf(unprojected_folder, "Transformations.dbf")

    if SurveyGDB.projected:
        projected_folder = os.path.join(output_folder, "SurveyData")
        os.makedirs(projected_folder)
        projected_realization = Riverscapes.SurveyDataRealization(True)
        projected_realization.create("Survey Data Projected")
        projected_realization.promoted = True

        for dataset in SurveyGDB.get_survey_datasets(True):
            if dataset.validateExists():
                dataset.exportToShapeFile(projected_folder, force_z_enabled=True)
                ds = Riverscapes.Dataset()
                ds.create(dataset.rs_name, os.path.join("SurveyData", dataset.shapefile_basename()))
                ds.id = dataset.rs_id
                # check if z values for breaklines exist.
                if dataset.rs_name == "Breaklines" and not dataset.test_z():
                    import zsnap
                    zsnap(os.path.join(projected_folder, "Breaklines.shp"),[SurveyGDB.Topo_Points.filename,
                                                                            SurveyGDB.EdgeOfWater_Points.filename,
                                                                            SurveyGDB.Stream_Features.filename])
                    ds.metadata["ExportNote"] = "Enabled Z Values on Export"
                projected_realization.datasets[ds.id] = ds

        survey_extents_folder = os.path.join(projected_folder, "SurveyExtents")
        os.makedirs(survey_extents_folder)
        SurveyGDB.SurveyExtent.exportToShapeFile(survey_extents_folder)
        ds = Riverscapes.Dataset()
        ds.create(SurveyGDB.SurveyExtent.rs_name, os.path.join("SurveyData", "SurveyExtents",
                                                               SurveyGDB.SurveyExtent.shapefile_basename()))
        ds.id = SurveyGDB.SurveyExtent.rs_id
        ds.attributes["active"] = "true"
        projected_realization.survey_extents[ds.id] = ds
        rs_project.addRealization(projected_realization, "survey_data_projected")

    # Topography Realization
    topography_folder_base = os.path.join("Topography", "TIN0001")
    topography_folder = os.path.join(output_folder, topography_folder_base)
    os.makedirs(topography_folder)

    TIN = CHaMP_Data.EsriTIN(topo_tin)
    TIN.copy_tin(os.path.join(topography_folder, TIN.basename))

    ds_tin = Riverscapes.Dataset()
    ds_tin.create("TopoTIN", os.path.join(topography_folder_base, TIN.basename), "TIN")
    ds_tin.id = TIN.basename
    ds_tin.attributes["active"] = "true"

    topography_realization = Riverscapes.TopographyRealization("Topography Realization", ds_tin)
    topography_realization.id = "topography"

    stage_wetted_folder = os.path.join(topography_folder, "Stages", "Wetted")
    stage_bankfull_folder = os.path.join(topography_folder, "Stages", "Bankfull")
    os.makedirs(stage_bankfull_folder)
    os.makedirs(stage_wetted_folder)

    for dataset in SurveyGDB.getDatasets("stage"):
        if dataset.validateExists():
            ds = Riverscapes.Dataset()
            if dataset.stage == "wetted":
                dataset.exportToShapeFile(stage_wetted_folder)
                ds.create(dataset.rs_name, os.path.join(topography_folder_base, "Stages", "Wetted", dataset.shapefile_basename()))
            elif dataset.stage == "bankfull":
                dataset.exportToShapeFile(stage_bankfull_folder)
                ds.create(dataset.rs_name, os.path.join(topography_folder_base, "Stages", "Bankfull", dataset.shapefile_basename()))
            ds.id = dataset.rs_id
            ds.attributes["stage"] = dataset.stage
            ds.attributes["type"] = dataset.stage_type
            topography_realization.stages[ds.id] = ds

    for dataset in SurveyGDB.getDatasets("topography"):
        if dataset.validateExists():
            ds = Riverscapes.Dataset()
            dataset.export(topography_folder)
            ds.create(dataset.rs_name, os.path.join(topography_folder_base, dataset.basename()), dataset.rs_type)
            ds.id = dataset.rs_id
            if dataset.rs_name == "DEM":
                for key, value in dataset.get_extents().iteritems():
                    ds.metadata[key] = str(value)
            topography_realization.topography[ds.id] = ds
        elif dataset.rs_name == "WaterDepth":
            dataset.create(SurveyGDB.DEM, SurveyGDB.WSEDEM)
            ds = Riverscapes.Dataset()
            dataset.export(topography_folder)
            ds.create(dataset.rs_name, os.path.join(topography_folder_base, dataset.basename()), dataset.rs_type)
            ds.id = dataset.rs_id
            topography_realization.topography[ds.id] = ds

    WSETIN = CHaMP_Data.EsriTIN(ws_tin)
    WSETIN.copy_tin(os.path.join(topography_folder, WSETIN.basename))
    ds_wsetin = Riverscapes.Dataset()

    ds_wsetin.create("Water Surface TIN", os.path.join(topography_folder_base, WSETIN.basename), "WaterSurfaceTIN")
    ds_wsetin.id = "WaterSurfaceTIN"
    ds_wsetin.attributes["active"] = "true"

    topography_realization.topography[ds_wsetin.id] = ds_wsetin

    assoc_surfaces_folder = os.path.join(topography_folder, "AssocSurfaces")
    os.makedirs(assoc_surfaces_folder)
    for dataset in SurveyGDB.getDatasets("surfaces"):
        if dataset.validateExists():
            ds = Riverscapes.Dataset()
            dataset.export(assoc_surfaces_folder)
            ds.create(dataset.rs_name, os.path.join(topography_folder_base, "AssocSurfaces", dataset.basename()), dataset.rs_type)
            ds.id = dataset.rs_id
            topography_realization.assocated_surfaces[ds.id] = ds

    rs_project.addRealization(topography_realization, topography_realization.id)
    rs_project.writeProjectXML()

    if os.path.exists(mapimages_folder):
        mapimages_project_folder = os.path.join(output_folder, "MapImages")
        os.makedirs(mapimages_project_folder)
        import glob
        images = []
        for image in glob.glob(os.path.join(mapimages_folder, "*.png")) + glob.glob(os.path.join(mapimages_folder, "*.jpg")):
            image_name = os.path.basename(image)
            shutil.copyfile(image, os.path.join(mapimages_project_folder, image_name))
            images.append(image_name)

        SurveyGDB.tblMapImages.export_mapimages_xml(os.path.join(mapimages_project_folder, "mapimages.xml"), images)

        reports_folder = os.path.join(mapimages_folder, "Reports")
        if os.path.exists(reports_folder):
            os.makedirs(os.path.join(output_folder, "Reports"))
            dir_util.copy_tree(reports_folder, os.path.join(output_folder, "Reports"))

    if SurveyGDB.tblLog.validateExists():
        str_export = "Exported by {} version {}".format(toolName, toolVersion)
        SurveyGDB.tblLog.export_as_xml(os.path.join(output_folder, "log.xml"), str_export )

    totaltime = ( time.time() - start )
    print "Total Time: {0}s".format(totaltime)
    print "Export Complete  at " + str(time.asctime())

    # Results     
    mWriter.currentRun.addResult("last_log_timestamp", "") # Proxy for the latest change

    # Write Metadata File
    mWriter.finalizeRun()
    mWriter.writeMetadataFile(outXMLfile)
            
    return


def main():
    import argparse
    parser = argparse.ArgumentParser()

    parser.add_argument('surveygdb', help='Path to Survey Geodatabase', type=str)
    parser.add_argument('topoTIN', help='Path to topo TIN', type=str)
    parser.add_argument('wseTIN', help="Path to Water Surface TIN", type=str)
    parser.add_argument('channelunitscsv', help='Path to channelunit csv file', type=str)
    parser.add_argument('outputprojectfolder', help="folder to store new project")
    parser.add_argument('visitid', help='the visit id for the survey as string', type=str)
    parser.add_argument('site', help='the site id/name for the survey', type=str)
    parser.add_argument('watershed', help='the watershed for the survey', type=str)
    parser.add_argument('year', help='the year of the survey as string', type=str)
    parser.add_argument('--rawinstrumentfile', help="raw instrument files", type=str, default=None)
    parser.add_argument('--auxinstrumentfile', help="auxiliary instrument files", type=str, default=None)
    parser.add_argument('--dxffile', help="Path to dxf file", type=str, default=None)
    parser.add_argument('--mapimagesfolder', help="Path to map images folder", type=str, default=None)

    parser.add_argument('--logfile', help='Output a log file.', default="" )
    parser.add_argument('--verbose', help='Get more information in your logs.', action='store_true', default=False )
    args = parser.parse_args()

    # Check Args
    if not args.outputprojectfolder or not args.surveygdb:
        print "ERROR: Missing arguments"
        parser.print_help()
        exit(1)
    if not os.path.isdir(args.outputprojectfolder):
        print "ERROR: '{}' is not a folder".format(args.outputprojectfolder)
        parser.print_help()
        exit(1)

    # Initiate the log file
    #log = Logger("Program")
    #log.setup(logPath=args.logfile, verbose=args.verbose)

    try:
        export_survey_project(args.surveygdb,
                              args.topoTIN,
                              args.wseTIN,
                              args.channelunitscsv,
                              args.outputprojectfolder,
                              args.visitid,
                              args.site,
                              args.watershed,
                              args.year,
                              args.rawinstrumentfile,
                              args.auxinstrumentfile,
                              args.dxffile,
                              args.mapimagesfolder)
    except Exception as e:
        traceback.print_exc(file=sys.stdout)
        sys.exit(1)

    sys.exit(0)


if __name__ == "__main__":
    main()
