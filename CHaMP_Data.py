# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# Name:        CHaMP Classes for GIS Tools                                    #
# Purpose:     Developed for CHaMP Program                                    #
#                                                                             #
# Author:      Kelly Whitehead                                                #
#              South Fork Research, Inc                                       #
#              Seattle, Washington                                            #
#                                                                             #
# Created:     2013-04-23                                                     #
# Version:     13.15          Modified:   2015-05-21                          #
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# !/usr/bin/env python

# # Import Modules # #
import arcpy
from os import path
import xml.etree.ElementTree as ET


## Survey Data Containers ## 
class SiteGeodatabase():
    """
    Site Geodatabase for CHaMP contains:
        Control_Network
        Survey Information
    """

    def __init__(self, filename):
        self.filename = filename
        self.fcControlNetwork = self.filename + '\\ControlNetwork'
        self.tableSurveyInfromation = self.filename + '\\SiteInfo'
        self.siteGDB = arcpy.Describe(filename)

    def test(self):
        status = 1
        if arcpy.Exists(self.fcControlNetwork) == 0:
            status = status * 0
        if arcpy.Exists(self.tableSurveyInfromation) == 0:
            status = status * 0
        return status

    def getSiteName(self):
        sc = arcpy.SearchCursor(self.tableSurveyInfromation)
        row = sc.next()
        sitename = row.getValue("SiteName")
        del sc, row
        return sitename


class SurveyGeodatabase():
    """
    Survey Geodatabase must exist or exception on object creation.
    """
    version = 2016.01

    def __init__(self, filename):

        self.filename = filename

        # Feature Datasets
        self.unprojected = filename + "\\Unprojected"
        self.projected = filename + "\\Projected"

        # Survey Data
        self.Control_Points = Control_Points(self.projected, True)
        self.Topo_Points = Topo_Points(self.projected, True)
        self.Bankfull_Polygon = Bankfull_Polygon(self.projected)
        self.Bankfull_Centerline = Bankfull_Centerline(self.projected)
        self.Bankfull_CrossSections = Bankfull_CrossSections(self.projected)
        self.Bankfull_Islands = Bankfull_Islands(self.projected)
        self.Benchmarks = Benchmarks(self.projected, "Benchmarks", True)
        self.Breaklines = Breaklines(self.projected, True)
        self.Channel_Units = Channel_Units(self.projected)
        self.Channel_Units_Crew = Channel_Units_Crew(self.projected)
        self.EdgeOfWater_Points = EdgeOfWater_Points(self.projected, True)
        self.Error_Lines = Error_Lines(self.projected, True)
        self.Error_Points = Error_Points(self.projected, True)
        self.Stream_Features = Stream_Features(self.projected, True)
        self.SurveyExtent = SurveyExtent(self.projected)
        self.Thalweg = Thalweg(self.projected)
        self.Wetted_Centerline = Wetted_Centerline(self.projected)
        self.Wetted_Extent = Wetted_Extent(self.projected)
        self.Wetted_CrossSections = Wetted_CrossSections(self.projected)
        self.Wetted_Islands = Wetted_Islands(self.projected)

        self.UnprojectedTopoPoints = Topo_Points(self.unprojected, False)
        self.UnprojectedControlPoints = Control_Points(self.unprojected, False)
        self.UnprojectedErrorPoints = Error_Points(self.unprojected, False)
        self.UnprojectedEdgeofWaterPoints = EdgeOfWater_Points(self.unprojected, False)
        self.UnprojectedBreaklines = Breaklines(self.unprojected, False)
        self.UnprojectedStreamFeatures = Stream_Features(self.unprojected, False)

        # Tables
        self.tblQaQcPoints = GISTable(self.filename, "QaQcPoints", "QA")
        self.tblQaQcLines = GISTable(self.filename, "QaQcLines", "QA")
        self.tblQaQcPolygons = GISTable(self.filename, "QaQcPolygons", "QA")
        self.tblQaQcVector = GISTable(self.filename, "QaQcVector", "QA")
        self.tblQaQcTIN = GISTable(self.filename, "QaQcTIN", "QA")
        self.tblLog = TableLog(self.filename, "Log")
        self.tblOrthogInfo = GISTable(self.filename, "OrthogInfo")
        self.tblSurveyInfo = GISTable(self.filename, "SurveyInfo")
        self.tblTransformations = GISTable(self.filename, "Transformations")
        self.tblCrewFeedback = GISTable(self.filename, "CrewFeedback", "QA")
        self.tblMapImages = TableMapImages(self.filename, "MapImages")
        self.tblQaQcBacksightLog = GISTable(self.filename, "QaQcBacksightLog", "QA")
        self.tblQaQcUncertaintySummary = GISTable(self.filename, "QaQcUncertaintySummary", "QA")

        self.fcQaQcRawPoints = QaQcRawPoints(self.filename, True)

        # Raster Dataset
        self.DEM = DEM(self.filename)
        self.DetrendedDEM = DetrendedDEM(self.filename)
        self.WaterDepth = WaterDepth(self.filename)
        self.WSEDEM = WSEDEM(self.filename)
        self.DEMHillshade = DEMHillshade(self.filename)
        self.AssocSlope = AssocSlope(self.filename)
        self.AssocPDensity = AssocPDensity(self.filename)
        self.AssocIErr = AssocIErr(self.filename)
        self.Assoc3DPQ = Assoc3DPQ(self.filename)
        self.AssocD50 = AssocD50(self.filename)
        self.ErrSurface = ErrSurface(self.filename)
        self.AssocRough = AssocRough(self.filename)

        self.listDatasets = [self.Control_Points,
                             self.Topo_Points,
                             self.Bankfull_Polygon,
                             self.Bankfull_Centerline,
                             self.Bankfull_CrossSections,
                             self.Bankfull_Islands,
                             self.Benchmarks,
                             self.Breaklines,
                             self.Channel_Units,
                             self.Channel_Units_Crew,
                             self.EdgeOfWater_Points,
                             self.Error_Lines,
                             self.Error_Points,
                             self.Stream_Features,
                             self.SurveyExtent,
                             self.Thalweg,
                             self.Wetted_Centerline,
                             self.Wetted_Extent,
                             self.Wetted_CrossSections,
                             self.Wetted_Islands,
                             self.DEM,
                             self.DetrendedDEM,
                             self.DEMHillshade,
                             self.Assoc3DPQ,
                             self.AssocD50,
                             self.AssocIErr,
                             self.AssocPDensity,
                             self.AssocSlope,
                             self.AssocRough,
                             self.ErrSurface,
                             self.WSEDEM,
                             self.WaterDepth,
                             self.UnprojectedTopoPoints,
                             self.UnprojectedControlPoints,
                             self.UnprojectedErrorPoints,
                             self.UnprojectedEdgeofWaterPoints,
                             self.UnprojectedBreaklines,
                             self.UnprojectedStreamFeatures,
                             self.tblQaQcPoints,
                             self.tblQaQcLines,
                             self.tblQaQcPolygons,
                             self.tblQaQcVector,
                             self.tblQaQcTIN,
                             self.tblLog,
                             self.tblOrthogInfo,
                             self.tblSurveyInfo,
                             self.tblTransformations,
                             self.tblCrewFeedback,
                             self.tblMapImages,
                             self.fcQaQcRawPoints,
                             self.tblQaQcBacksightLog,
                             self.tblQaQcUncertaintySummary]

    def projection_info(self):

        sr = arcpy.Describe(self.projected).spatialReference

        dictProjection = {}
        dictProjection["SpatialReferenceName"] = str(sr.name)
        dictProjection["SpatialReferenceWKID"] = str(sr.projectionCode)
        dictProjection["SpatialReference"] = str(sr.exportToString())
        return dictProjection

    def getDatasets(self, family=None):
        """ rtype: collections.Iterable"""
        for dataset in self.listDatasets:
            if dataset.family == family or family is None:
                yield dataset

    def getRasterDatasets(self):
        for dataset in self.getDatasets():
            if dataset.Datatype == "Raster":
                yield dataset

    def getVectorDatasets(self):
        for dataset in self.getDatasets():
            if dataset.Datatype == "Vector":
                yield dataset

    def getTables(self):
        """ rtype: GISTable"""
        for dataset in self.getDatasets():
            if dataset.Datatype == "Table":
                yield dataset

    def get_survey_datasets(self, projection_status=True):
        for dataset in self.getDatasets():
            if dataset.family == "surveydata" and dataset.projected == projection_status:
                yield dataset

    def getExportToGISDatasets(self):
        for dataset in self.getDatasets():
            if dataset.ExportToGIS:
                yield dataset

    def getPublish(self):
        for dataset in self.getDatasets():
            if dataset.Publish:
                yield dataset

    def checkGDBVersion(self):
        return True if self.getGDBVersion() == self.version else False

    def getGDBVersion(self):
        return

    def getGDBVersionProperties(self):
        print "GDB Version: " + str(self.version)
        for dataset in self.getDatasets():
            print " Name: " + dataset.Name
            print " Datatype: " + dataset.Datatype
            print " Required: " + str(dataset.Required)
            print " Include in Publish: " + str(dataset.Publish)

    def year(self):
        """ returns type Double of contents of FieldSeason in SurveyInfo Table."""
        if arcpy.Exists(self.tblSurveyInfo):
            if arcpy.ListFields(self.tblSurveyInfo, "FieldSeason"):
                with arcpy.da.SearchCursor(self.tblSurveyInfo, ["FieldSeason"]) as scTblSurveyInfo:
                    row = scTblSurveyInfo.next()
                    return str(row[0]) if type == "STRING" else row[0]

    def has_unprojected(self):
        return arcpy.Exists(self.unprojected)

    def exportTopoTINDXF(self, outFolder):
        """exports dxf file (and SHP files) containing tin components of topo tin in same folder as gdb"""

        from os import path, makedirs
        arcpy.CheckOutExtension("3D")
        arcpy.env.workspace = arcpy.Describe(self.filename).path
        topoTINs = arcpy.ListDatasets("TIN*", "Tin")
        topoTIN = topoTINs[0]
        outfile = path.join(outFolder, "TopoTin") + ".dxf"

        memTinPoints = "in_memory//tin_points"
        memTinLines = "in_memory//tin_lines"
        memTinArea = "in_memory//tin_area"
        # TODO Do actual breaklines need to be pulled into their own layer?
        listTINComponents = [memTinPoints, memTinLines, memTinArea]
        for item in listTINComponents:
            if arcpy.Exists(item):
                arcpy.Delete_management(item)
        arcpy.TinNode_3d(topoTIN, memTinPoints)
        arcpy.TinEdge_3d(topoTIN, memTinLines, "DATA")
        arcpy.TinDomain_3d(topoTIN, memTinArea, "POLYGON")

        # TODO Convert Line Type from  eSRI code??
        arcpy.ExportCAD_conversion(listTINComponents, "DXF_R2007", outfile)

        return outfile

    def exportSurveyTopographyDXF(self, outFolder):
        """exports dxf file containing Topographic Survey Points, Lines and Survey Extent """
        from os import path
        outfile = path.join(outFolder, "SurveyTopography") + ".dxf"

        memTopoPoints = "in_memory//Topo_Points"
        memEOW = "in_memory//EdgeofWater_Points"
        memBreaklines = "in_memory//Breaklines"
        memSurveyExtent = "in_memory//Survey_Extent"
        memPoints = "in_memory//AllPoints"
        # memLines = "in_memory//AllLines"
        memControlPoints = "in_memory//ControlPoints"
        listmemFCs = [memTopoPoints, memEOW, memBreaklines, memSurveyExtent]
        listmemAnnotation = [memPoints, memControlPoints]

        for fc in listmemFCs + listmemAnnotation:
            if arcpy.Exists(fc):
                arcpy.Delete_management(fc)

        arcpy.CopyFeatures_management(self.Topo_Points.filename, memTopoPoints)
        arcpy.CopyFeatures_management(self.EdgeOfWater_Points.filename, memEOW)
        arcpy.CopyFeatures_management(self.Breaklines.filename, memBreaklines)
        arcpy.CopyFeatures_management(self.SurveyExtent.filename, memSurveyExtent)
        arcpy.CopyFeatures_management(self.Control_Points.filename, memControlPoints)
        arcpy.CopyFeatures_management(self.Topo_Points.filename, memPoints)

        arcpy.ExportCAD_conversion([memBreaklines, memSurveyExtent, memPoints], "DXF_R2010", outfile)

        outCSV = path.join(outFolder, "SurveyTopographyPoints") + ".csv"
        exportAsCSV(memPoints, outCSV)

        outControlCSV = path.join(outFolder, "ControlNetworkPoints") + ".csv"
        exportAsCSV(memControlPoints, outControlCSV)

        return outfile


def exportAsCSV(inFeatureClass, outCSVfile):
    import csv
    with open(outCSVfile, "wb") as csvfile:
        csvWriter = csv.writer(csvfile)

        fields = arcpy.ListFields(inFeatureClass)
        fieldsGIS = ("POINT_NUMBER", "SHAPE@Y", "SHAPE@X", "SHAPE@Z", "DESCRIPTION")
        fieldsCAD = ("PNTNO", "Y", "X", "ELEV", "DESC")

        with arcpy.da.SearchCursor(inFeatureClass, fieldsGIS) as scFeatures:
            csvWriter.writerow(fieldsCAD)
            for row in scFeatures:
                csvWriter.writerow(row)
    return


## Base GIS Classes ##
class GISDataset(object):

    def __init__(self, filename):
        self.filename = filename

    def validateExists(self):
        return True if arcpy.Exists(self.filename) else False


class GISTable(GISDataset):
    Datatype = "Table"

    def __init__(self, datapath, name, family=None, sqlitename=None):
        GISDataset.__init__(self, path.join(datapath, name))
        self.family = family
        self.name = name
        self.sqlitename = name if sqlitename is None else sqlitename

    def export_to_xml(self, output_xmlfile):
        # rootElement = ET.ElementTree("")
        #
        #
        #
        # for field, value in self.get_data():
        return

    def export_to_sqlite(self, sqlite_db):
        import sqlite3
        if self.validateExists():
            fields = [f.name for f in arcpy.ListFields(self.filename) if f.name not in ["OBJECTID", "ZminProj", "ZmaxProj", "ZrangeProj"]]
            with arcpy.da.SearchCursor(self.filename, fields) as sc:
                l_data = [tuple(row) for row in sc]
                with sqlite3.connect(sqlite_db) as conn:
                    conn.executemany("INSERT INTO " + self.sqlitename + " (" +
                                     ",".join(["{}"]*len(fields)).format(*['"' + f + '"' for f in sc.fields]) + ") VALUES (" +
                                     ",".join(["?"]*len(fields)) + ")", l_data)
                    conn.commit()

    def export_to_dbf(self, out_folder, dbf_name):
        arcpy.TableToTable_conversion(self.filename, out_folder, dbf_name)
        return path.join(out_folder, dbf_name + ".dbf")

    def get_data(self):
        if self.validateExists():
            fields = [f.name for f in arcpy.ListFields(self.filename) if f.name not in ["OBJECTID", "ZminProj", "ZmaxProj", "ZrangeProj"]]
            with arcpy.da.SearchCursor(self.filename, fields) as sc:
                for row in sc:
                    for value, field in zip(row, fields):
                        yield field, value


class GISRaster(GISDataset):
    Datatype = "Raster"

    def __init__(self, filename, name):
        GISDataset.__init__(self, filename)
        self.family = None
        self.name = name

    def exportToGeoTiff(self, outputPath):
        arcpy.RasterToOtherFormat_conversion(self.filename, outputPath, "TIFF")

    def export(self, outputPath):
        self.exportToGeoTiff(outputPath=outputPath)

    def basename(self):
        return self.name + ".tif"

    def get_extents(self):
        dict_extents = {}
        descRaster = arcpy.Describe(self.filename)
        dict_extents["right"] = descRaster.Extent.XMax
        dict_extents["left"] = descRaster.Extent.XMin
        dict_extents["top"] = descRaster.Extent.YMax
        dict_extents["bottom"] = descRaster.Extent.YMin
        dict_extents["cellsize"] = descRaster.meanCellWidth
        return dict_extents


class GISVector(GISDataset):
    Datatype = "Vector"

    def __init__(self, GDBProjectedPath, name, projected=True):
        self.Name = name if projected else name + "_Unprojected"
        GISDataset.__init__(self, path.join(GDBProjectedPath, self.Name))
        self.projected = projected
        self.listFields = []
        self.dict_field_names = {}
        self.family = None
        self.outName = name
        self.rs_type = "Vector"

    def addField(self, field):
        self.listFields.append(field)
        self.dict_field_names[field.nameFull] = field.nameShort
        return field

    def getFieldMapping(self):
        fieldMappings = arcpy.FieldMappings()
        for field in arcpy.ListFields(self.filename):
            if field.name not in ["Shape", "shape"]:
                fm = arcpy.FieldMap()
                fm.addInputField(self.filename, field.name)
                outfield = fm.outputField
                outfield.name = self.dict_field_names[field.name] if field.name in self.dict_field_names.keys() else field.name
                fm.outputField = outfield
                fieldMappings.addFieldMap(fm)
        return fieldMappings

    def exportToShapeFile(self, outputPath, outname=None, force_z_enabled=False):
        name = self.outName if outname is None else outname
        field_mappings = self.getFieldMapping()
        if force_z_enabled:
            arcpy.env.output_z_flag = True
        arcpy.FeatureClassToFeatureClass_conversion(self.filename, outputPath, name,
                                                    field_mapping=field_mappings)
        return name + ".shp"

    def export(self, ouputPath):
        self.exportToShapeFile(outputPath=ouputPath)

    def shapefile_basename(self, name=None):
        return self.outName + ".shp"

    def basename(self):
        return self.shapefile_basename()

    def test_z(self):
        return arcpy.Describe(self.filename).hasZ


## Fields ##
class GISField():
    lengthStringDefault = 255

    def __init__(self, nameFull, nameShort, type, strlength=lengthStringDefault):
        self.nameFull = nameFull
        self.nameShort = nameShort
        self.type = type
        self.strlength = strlength

    def getFieldMap(self, filename):
        outFieldMap = arcpy.FieldMap()
        outFieldMap.addInputField(filename, self.nameFull)
        outField = outFieldMap.outputField
        outField.name = self.nameShort
        outFieldMap.outputField = outField

        return outFieldMap


class FieldDescription(GISField):
    def __init__(self, codeList):
        GISField.__init__(self, "DESCRIPTION", "Code", "STRING", 6)
        self.codeList = codeList


class FieldPointNumber(GISField):
    def __init__(self):
        GISField.__init__(self, "POINT_NUMBER", "POINT_NUMB", "STRING", 10)


class FieldExtentType(GISField):
    def __init__(self):
        GISField.__init__(self, "ExtentType", "ExtentType", "STRING")
        self.listValueFilter = ["Channel", ""]


class FieldChannel(GISField):
    def __init__(self):
        GISField.__init__(self, "Channel", "Channel", "STRING")


class FieldCLID(GISField):
    def __init__(self):
        GISField.__init__(self, "CLID", "CLID", "STRING")


class FieldIsValid(GISField):
    def __init__(self):
        GISField.__init__(self, "IsValid", "IsValid", "STRING")


class FieldQualifying(GISField):
    def __init__(self):
        GISField.__init__(self, "Qualifying", "Qualifying", "STRING")


class FieldLineType(GISField):
    nameFull = "LineType"
    nameShort = "LineType"

    def __init__(self):
        GISField.__init__(self, self.nameFull, self.nameShort, "STRING")


class FieldChannelUnitNumber(GISField):
    nameFull = "Unit_Number"
    nameShort = "UnitNumber"

    def __init__(self):
        GISField.__init__(self, self.nameFull, self.nameShort, "STRING")


class FieldVDE(GISField):
    nameFull = "VDE"
    nameShort = "VDE"

    def __init__(self):
        GISField.__init__(self, self.nameFull, self.nameShort, "STRING")


class FieldHDE(GISField):
    nameFull = "HDE"
    nameShort = "HDE"

    def __init__(self):
        GISField.__init__(self, self.nameFull, self.nameShort, "STRING")


class FieldPointQuality(GISField):
    nameFull = "POINT_QUALITY"
    nameShort = "PQuality"

    def __init__(self):
        GISField.__init__(self, self.nameFull, self.nameShort, "STRING")


class FieldStation(GISField):
    nameFull = "Station"
    nameShort = "Station"

    def __init__(self):
        GISField.__init__(self, self.nameFull, self.nameShort, "STRING")


class FieldErrorType(GISField):
    nameFull = "ErrorType"
    nameShort = "ErrorType"

    def __init__(self):
        GISField.__init__(self, self.nameFull, self.nameShort, "STRING")


## Vector Datasets ##
class Control_Points(GISVector):
    """
    """
    Publish = True
    ExportToGIS = True
    Required = True
    listCodes = []
    rs_id = "control_points"
    rs_name = "Control Points"

    fieldDescription = FieldDescription(listCodes)
    fieldVDE = FieldVDE()
    fieldHDE = FieldHDE()
    fieldPointQuality = FieldPointQuality()
    fieldStation = FieldStation()
    fieldPointNumber = FieldPointNumber()
    fieldCPType = GISField("Type", "Type", "STRING")
    fieldCPSource = GISField("Source", "Source", "STRING")

    def __init__(self, FDS, projected):
        GISVector.__init__(self, FDS, "Control_Points", projected)
        self.family = "surveydata"
        self.addField(self.fieldVDE)
        self.addField(self.fieldHDE)
        self.addField(self.fieldDescription)
        self.addField(self.fieldPointNumber)
        self.addField(self.fieldPointQuality)
        self.addField(self.fieldStation)
        self.addField(self.fieldCPType)
        self.addField(self.fieldCPSource)
        self.addField(GISField("ROD_HEIGHT", "ROD_HEIGHT", "DOUBLE"))
        self.addField(GISField("EVENT_ID", "EVENT_ID", "DOUBLE"))


class Topo_Points(GISVector):
    Publish = True
    ExportToGIS = True
    Required = True
    listCodes = ["tp%"]
    rs_id = 'topo_points'
    rs_name = "Topo Points"

    fieldDescription = FieldDescription(listCodes)
    fieldVDE = FieldVDE()
    fieldHDE = FieldHDE()
    fieldPointQuality = FieldPointQuality()
    fieldStation = FieldStation()
    fieldPointNumber = FieldPointNumber()

    def __init__(self, FDS, projected):
        GISVector.__init__(self, FDS, "Topo_Points", projected)
        self.family = "surveydata"
        self.addField(self.fieldVDE)
        self.addField(self.fieldHDE)
        self.addField(self.fieldDescription)
        self.addField(self.fieldPointNumber)
        self.addField(self.fieldPointQuality)
        self.addField(self.fieldStation)
        self.addField(GISField("ROD_HEIGHT", "ROD_HEIGHT", "DOUBLE"))
        self.addField(GISField("EVENT_ID", "EVENT_ID", "DOUBLE"))

class QaQcRawPoints(GISVector):
    Publish = True
    ExportToGIS = True
    Required = True
    listCodes = [""]
    rs_id = 'QaQcPoints'
    rs_name = "QaQc Raw Points"

    fieldDescription = FieldDescription(listCodes)
    fieldVDE = FieldVDE()
    fieldHDE = FieldHDE()
    fieldPointQuality = FieldPointQuality()
    fieldStation = FieldStation()
    fieldPointNumber = FieldPointNumber()

    def __init__(self, FDS, projected):
        GISVector.__init__(self, FDS, "QaQcRawPoints", projected)
        self.family = None
        self.addField(self.fieldVDE)
        self.addField(self.fieldHDE)
        self.addField(self.fieldDescription)
        self.addField(self.fieldPointNumber)
        self.addField(self.fieldPointQuality)
        self.addField(self.fieldStation)
        self.addField(GISField("ROD_HEIGHT", "ROD_HEIGHT", "DOUBLE"))
        self.addField(GISField("EVENT_ID", "EVENT_ID", "DOUBLE"))


class Bankfull_Polygon(GISVector):
    Publish = True
    ExportToGIS = True
    Required = True
    rs_id = "bankfull_extent"
    rs_name = "BExtent"

    fieldExtent = FieldExtentType()

    def __init__(self, FDS):
        GISVector.__init__(self, FDS, "Bankfull")
        self.family = "stage"
        self.stage = 'bankfull'
        self.stage_type = "extent"
        self.addField(self.fieldExtent)


class Bankfull_Centerline(GISVector):
    Publish = True
    ExportToGIS = True
    Required = True
    rs_id = "bankfull_centerline"
    rs_name = "BCenterline"

    fieldChannel = FieldChannel()
    fieldCLID = FieldCLID()

    def __init__(self, GDBProjected):
        GISVector.__init__(self, GDBProjected, "BankfullCL")
        self.family = "stage"
        self.stage = 'bankfull'
        self.stage_type = "centerline"
        self.addField(self.fieldChannel)
        self.addField(self.fieldCLID)


class Bankfull_CrossSections(GISVector):
    Publish = True
    ExportToGIS = True
    Required = True
    rs_id = "bankfull_crosssections"
    rs_name = "BCrossSections"

    fieldChannel = FieldChannel()
    fieldIsValid = FieldIsValid()

    def __init__(self, FDS):
        GISVector.__init__(self, FDS, "BankfullXS")
        self.family = "stage"
        self.stage = 'bankfull'
        self.stage_type = "crosssections"
        self.addField(self.fieldChannel)
        self.addField(self.fieldIsValid)


class Bankfull_Islands(GISVector):
    Publish = True
    ExportToGIS = True
    Required = True
    rs_id = "bankfull_islands"
    rs_name = "BIslands"

    fieldIsValid = FieldIsValid()
    fieldQualifying = FieldQualifying()

    def __init__(self, FDS):
        GISVector.__init__(self, FDS, "BIslands")
        self.family = "stage"
        self.stage = 'bankfull'
        self.stage_type = "islands"
        self.addField(self.fieldIsValid)
        self.addField(self.fieldQualifying)


class Benchmarks(GISVector):
    Publish = True
    ExportToGIS = False
    Name = "Benchmarks"
    Required = False


class Breaklines(GISVector):
    Publish = True
    ExportToGIS = True
    Required = True
    lineCodes = []
    rs_id = 'breaklines'
    rs_name = "Breaklines"

    fieldDescription = FieldDescription(lineCodes)
    fieldLineTypes = FieldLineType()

    def __init__(self, FDS, projected):
        GISVector.__init__(self, FDS, "Breaklines", projected)
        self.family = "surveydata"
        self.addField(self.fieldDescription)
        self.addField(self.fieldLineTypes)


class Channel_Units(GISVector):
    Publish = True
    ExportToGIS = True
    Required = True

    fieldChannelUnitNumber = FieldChannelUnitNumber()

    def __init__(self, FDS):
        GISVector.__init__(self, FDS, "Channel_Units")
        self.family = "topography"
        self.addField(self.fieldChannelUnitNumber)
        self.rs_name = "Channel Units"
        self.rs_id = "ChannelUnits"
        self.rs_type = "ChannelUnits"


class Channel_Units_Crew(GISVector):
    Publish = True
    ExportToGIS = False
    Required = True

    fieldChannelUnitNumber = FieldChannelUnitNumber()

    def __init__(self, FDS):
        GISVector.__init__(self, FDS, "Channel_Units_Field")
        self.family = "topography"
        self.addField(self.fieldChannelUnitNumber)
        self.rs_name = "Channel Units"
        self.rs_id = "ChannelUnitsField"
        self.rs_type = "ChannelUnitsField"


class EdgeOfWater_Points(GISVector):
    Publish = True
    ExportToGIS = True
    Required = True
    rs_id = 'eow_points'
    rs_name = "Edge of Water Points"

    fieldDescription = FieldDescription([])
    fieldVDE = FieldVDE()
    fieldHDE = FieldHDE()
    fieldPointQuality = FieldPointQuality()
    fieldStation = FieldStation()
    fieldPointNumber = FieldPointNumber()

    def __init__(self, FDS, projected):
        GISVector.__init__(self, FDS, "EdgeofWater_Points", projected)
        self.family = "surveydata"
        self.addField(self.fieldVDE)
        self.addField(self.fieldHDE)
        self.addField(self.fieldDescription)
        self.addField(self.fieldPointNumber)
        self.addField(self.fieldPointQuality)
        self.addField(self.fieldStation)
        self.addField(GISField("ROD_HEIGHT", "ROD_HEIGHT", "DOUBLE"))
        self.addField(GISField("EVENT_ID", "EVENT_ID", "DOUBLE"))

class Error_Lines(GISVector):
    Publish = True
    ExportToGIS = True
    Required = False
    listErrorCodes = ["*"]

    fieldDescription = FieldDescription(listErrorCodes)
    fieldLineType = FieldLineType()
    fieldErrorType = FieldErrorType()

    # FieldOriginalLocation

    def __init__(self, FDS, projected):
        GISVector.__init__(self, FDS, "Error_Lines", projected)
        self.addField(self.fieldDescription)
        self.addField(self.fieldLineType)
        self.addField(self.fieldErrorType)


class Error_Points(GISVector):
    Publish = True
    ExportToGIS = True
    Required = True
    listErrorCodes = ["*"]
    rs_id = "error_points"
    rs_name = "Error Points"

    fieldDescription = FieldDescription(listErrorCodes)
    fieldVDE = FieldVDE()
    fieldHDE = FieldHDE()
    fieldPointQuality = FieldPointQuality()
    fieldStation = FieldStation()
    fieldPointNumber = FieldPointNumber()
    fieldErrorType = FieldErrorType()

    # FieldOriginalLocation

    def __init__(self, FDS, projected):
        GISVector.__init__(self, FDS, "Error_Points", projected)
        self.family = "surveydata"
        self.addField(self.fieldDescription)
        self.addField(self.fieldVDE)
        self.addField(self.fieldHDE)
        self.addField(self.fieldPointQuality)
        self.addField(self.fieldPointNumber)
        self.addField(self.fieldErrorType)
        self.addField(self.fieldStation)
        self.addField(GISField("ROD_HEIGHT", "ROD_HEIGHT", "DOUBLE"))
        self.addField(GISField("EVENT_ID", "EVENT_ID", "DOUBLE"))


class Stream_Features(GISVector):
    Publish = True
    ExportToGIS = True
    Required = True
    rs_id = "stream_features"
    rs_name = "Stream Features"

    fieldDescription = FieldDescription([])
    fieldVDE = FieldVDE()
    fieldHDE = FieldHDE()
    fieldPointQuality = FieldPointQuality()
    fieldStation = FieldStation()
    fieldPointNumber = FieldPointNumber()

    def __init__(self, FDS, projected):
        GISVector.__init__(self, FDS, "Stream_Features", projected)
        self.family = "surveydata"
        self.addField(self.fieldVDE)
        self.addField(self.fieldHDE)
        self.addField(self.fieldDescription)
        self.addField(self.fieldPointNumber)
        self.addField(self.fieldPointQuality)
        self.addField(self.fieldStation)
        self.addField(GISField("ROD_HEIGHT", "ROD_HEIGHT", "DOUBLE"))
        self.addField(GISField("EVENT_ID", "EVENT_ID", "DOUBLE"))


class SurveyExtent(GISVector):
    Publish = True
    ExportToGIS = True
    Required = True
    rs_id = "survey_extent"
    rs_name = "Survey Extent"

    def __init__(self, FDS):
        GISVector.__init__(self, FDS, "Survey_Extent")
        self.family = "surveyextents"

class Thalweg(GISVector):
    Publish = True
    ExportToGIS = True
    Required = True

    fieldPoolWt = GISField("PoolWt", "PoolWt", "LONG")
    fieldSmoothT = GISField("SmoothT", "SmoothT", "LONG")

    def __init__(self, FDS):
        GISVector.__init__(self, FDS, "Thalweg")
        self.family = "topography"
        self.rs_name = "Thalweg"
        self.rs_id = "thalweg"
        self.rs_type = "Thalweg"
        self.addField(self.fieldPoolWt)
        self.addField(self.fieldSmoothT)


class Wetted_Centerline(GISVector):
    Publish = True
    ExportToGIS = True
    Required = True
    rs_id = "wetted_centerline"
    rs_name = "WCenterline"

    fieldChannel = FieldChannel()
    fieldCLID = FieldCLID()

    def __init__(self, FDS):
        GISVector.__init__(self, FDS, "CenterLine")
        self.family = "stage"
        self.stage = 'wetted'
        self.stage_type = "centerline"
        self.addField(self.fieldChannel)
        self.addField(self.fieldCLID)


class Wetted_Extent(GISVector):
    Publish = True
    ExportToGIS = True
    Required = True
    rs_id = "wetted_extent"
    rs_name = "WExtent"

    fieldExtentType = FieldExtentType()

    def __init__(self, FDS):
        GISVector.__init__(self, FDS, "WaterExtent")
        self.family = "stage"
        self.stage = 'wetted'
        self.stage_type = "extent"
        self.addField(self.fieldExtentType)


class Wetted_CrossSections(GISVector):
    Publish = True
    ExportToGIS = True
    Required = True
    rs_id = "wetted_crosssections"
    rs_name = "WCrossSections"

    fieldChannel = FieldChannel()
    fieldIsValid = FieldIsValid()

    def __init__(self, FDS):
        GISVector.__init__(self, FDS, "WettedXS")
        self.family = "stage"
        self.stage = 'wetted'
        self.stage_type = "crosssections"
        self.addField(self.fieldChannel)
        self.addField(self.fieldIsValid)


class Wetted_Islands(GISVector):
    Publish = True
    ExportToGIS = True
    Required = True
    rs_id = "wetted_islands"
    rs_name = "WIslands"

    fieldIsValid = FieldIsValid()
    fieldQualifying = FieldQualifying()

    def __init__(self, FDS):
        GISVector.__init__(self, FDS, "WIslands")
        self.family = "stage"
        self.stage = 'wetted'
        self.stage_type = "islands"
        self.addField(self.fieldIsValid)
        self.addField(self.fieldQualifying)


## Raster Datasets ##
class DEM(GISRaster):
    name = "DEM"
    Publish = True
    ExportToGIS = True
    Required = True

    def __init__(self, path):
        GISRaster.__init__(self, path + "\\" + self.name, self.name)
        self.family = "topography"
        self.rs_name = "DEM"
        self.rs_id = "DEM"
        self.rs_type = "DEM"


class DEMHillshade(GISRaster):
    name = "DEMHillshade"
    Publish = True
    ExportToGIS = True
    Required = True

    def __init__(self, path):
        GISRaster.__init__(self, path + "\\" + self.name, self.name)
        self.family = "topography"
        self.rs_name = "Hillshade"
        self.rs_id = "DEMHillshade"
        self.rs_type = "DEMHillshade"


class DetrendedDEM(GISRaster):
    name = "Detrended"
    Publish = True
    ExportToGIS = True
    Required = True

    def __init__(self, path):
        GISRaster.__init__(self, path + "\\" + self.name, self.name)
        self.family = "topography"
        self.rs_name = "Detrended"
        self.rs_id = "Detrended"
        self.rs_type = "Detrended"


class WaterDepth(GISRaster):
    name = "Water_Depth"
    Publish = True
    ExportToGIS = True
    Required = True

    def __init__(self, path):
        GISRaster.__init__(self, path + "\\" + self.name, self.name)
        self.family = "topography"
        self.rs_name = "Water Depth"
        self.rs_id = "WaterDepth"
        self.rs_type = "WaterDepth"

    def create(self, DEM, WSEDEM):
        arcpy.env.extent = DEM
        arcpy.env.snapRaster = DEM
        rasterRawDepth = arcpy.sa.Minus(WSEDEM, DEM)
        rasterPositiveMaskBool = arcpy.sa.GreaterThan(rasterRawDepth, 0)
        rasterDepth = arcpy.sa.Abs(arcpy.sa.Times(rasterRawDepth, rasterPositiveMaskBool))
        rasterDepth.save(self.filename)


class WSEDEM(GISRaster):
    name = "WSEDEM"
    Publish = True
    ExportToGIS = True
    Required = True

    def __init__(self, path):
        GISRaster.__init__(self, path + "\\" + self.name, self.name)
        self.family = "topography"
        self.rs_name = "Water Surface DEM"
        self.rs_id = "WaterSurfaceDEM"
        self.rs_type = "WaterSurfaceDEM"


class AssocSlope(GISRaster):
    name = "AssocSlope"
    Publish = True
    ExportToGIS = True
    Required = True

    def __init__(self, path):
        GISRaster.__init__(self, path + "\\" + self.name, self.name)
        self.family = "surfaces"
        self.rs_name = "AssocSlope"
        self.rs_id = "Slope"
        self.rs_type = "Slope"


class AssocPDensity(GISRaster):
    name = "AssocPDensity"
    Publish = True
    ExportToGIS = True
    Required = True

    def __init__(self, path):
        GISRaster.__init__(self, path + "\\" + self.name, self.name)
        self.family = "surfaces"
        self.rs_name = "AssocPDensity"
        self.rs_id = "PointDensity"
        self.rs_type = "PointDensity"


class AssocIErr(GISRaster):
    name = "AssocIErr"
    Publish = True
    ExportToGIS = True
    Required = True

    def __init__(self, path):
        GISRaster.__init__(self, path + "\\" + self.name, self.name)
        self.family = "surfaces"
        self.rs_name = "AssocIErr"
        self.rs_id = "InterpolationError"
        self.rs_type = "InterpolationError"


class Assoc3DPQ(GISRaster):
    name = "Assoc3DPQ"
    Publish = True
    ExportToGIS = True
    Required = True

    def __init__(self, path):
        GISRaster.__init__(self, path + "\\" + self.name, self.name)
        self.family = "surfaces"
        self.rs_name = "Assoc3DPQ"
        self.rs_id = "PointQuality3D"
        self.rs_type = "PointQuality3D"


class AssocD50(GISRaster):
    name = "AssocD50"
    Publish = True
    ExportToGIS = True
    Required = True

    def __init__(self, path):
        GISRaster.__init__(self, path + "\\" + self.name, self.name)
        self.family = "surfaces"


class AssocRough(GISRaster):
    name = "AssocRough"
    Publish = True
    ExportToGIS = True
    Required = True

    def __init__(self, path):
        GISRaster.__init__(self, path + "\\" + self.name, self.name)
        self.family = "surfaces"
        self.rs_name = "AssocRough"
        self.rs_id = "Roughness"
        self.rs_type = "Roughness"


class ErrSurface(GISRaster):
    name = "ErrSurface"
    Publish = True
    ExportToGIS = True
    Required = True

    def __init__(self, path):
        GISRaster.__init__(self, path + "\\" + self.name, self.name)
        self.family = "surfaces"
        self.rs_name = "ErrSurface"
        self.rs_id = "ErrSurface"
        self.rs_type = "ErrSurface"

## Tables ##
class TableLog(GISTable):

    dict_fields = {"TIMESTAMP":"created",
                   "ToolName":"tool",
                   "Status":"status"}

    def export_as_xml(self, outxmlfile, exportMessage=None):
        root = ET.Element("Messages")
        with arcpy.da.SearchCursor(self.filename, "*") as sc:
            for row in sc:
                nodeMessage = ET.SubElement(root, "Message")
                for value, field in zip(row, sc.fields):
                    if field in self.dict_fields.keys():
                        nodeMessage.set(self.dict_fields[field], value)
                    if field == "Message":
                        nodeMessage.text = value
        if exportMessage:
            import datetime
            nodeMessage = ET.SubElement(root, "Message", {"created":str(datetime.datetime.utcnow()),
                                                          "tool":"CHaMP Survey Data Project Export",
                                                          "status":"Complete"})
            nodeMessage.text = exportMessage

        indent(root)
        tree = ET.ElementTree(root)
        tree.write(outxmlfile, 'utf-8', True)


class TableMapImages(GISTable):

    def get_image_data(self):
        dict_images = {}
        fields = ["FilePath", "Title", "Context", "Comments", "TIMESTAMP", "Purpose", "ImageCode"]
        with arcpy.da.SearchCursor(self.filename, fields) as sc:
            for row in sc:
                dict_images[row[0].lstrip(r'..\\')] = dict(zip(fields, row))
        return dict_images

    def export_mapimages_xml(self, outxmlfile, mapimages=None):
        root = ET.Element("MapImages")
        dict_images = self.get_image_data() if self.validateExists() else None
        for image in mapimages:
            nodeImage = ET.SubElement(root, "MapImage")
            dict_image = dict_images[image] if dict_images and dict_images.has_key(image)  else {}
            datecreated = dict_image["TIMESTAMP"] if dict_image.has_key("TIMESTAMP") else ""
            nodeImage.set("dateCreated", datecreated)
            ET.SubElement(nodeImage, "Title").text = dict_image["Title"] if dict_image.has_key("Title") else ""
            ET.SubElement(nodeImage, "Path").text = path.join("MapImages", image)
            ET.SubElement(nodeImage, "Context").text = dict_image["Context"] if dict_image.has_key("Context") else ""
            ET.SubElement(nodeImage, "ImageCode").text = dict_image["ImageCode"] if dict_image.has_key("ImageCode") else ""
            ET.SubElement(nodeImage, "Comments").text = dict_image["Comments"] if dict_image.has_key("Comments") else ""

        indent(root)
        tree = ET.ElementTree(root)
        tree.write(outxmlfile, 'utf-8', True)


## OtherFiles ##
class EsriTIN(object):

    def __init__(self, tin_path):
        self.path = tin_path
        self.basename = arcpy.Describe(tin_path).basename


    def copy_tin(self, dest_path):
        arcpy.Copy_management(self.path, dest_path)


def indent(elem, level=0, more_sibs=False):
    """ Pretty Print XML Element
    Source: http://stackoverflow.com/questions/749796/pretty-printing-xml-in-python
    """
    i = "\n"
    if level:
        i += (level - 1) * '  '
    num_kids = len(elem)
    if num_kids:
        if not elem.text or not elem.text.strip():
            elem.text = i + "  "
            if level:
                elem.text += '  '
        count = 0
        for kid in elem:
            indent(kid, level + 1, count < num_kids - 1)
            count += 1
        if not elem.tail or not elem.tail.strip():
            elem.tail = i
            if more_sibs:
                elem.tail += '  '
    else:
        if level and (not elem.tail or not elem.tail.strip()):
            elem.tail = i
            if more_sibs:
                elem.tail += '  '