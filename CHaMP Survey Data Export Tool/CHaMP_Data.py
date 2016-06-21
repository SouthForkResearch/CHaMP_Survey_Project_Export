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
#!/usr/bin/env python

# # Import Modules # #
import arcpy

## Survey Data Containers ## 
class SiteGeodatabase():
    """
    Site Geodatabase for CHaMP contains:
        Control_Network
        Survey Information
    """
    def __init__(self,filename):
        self.filename = filename
        self.fcControlNetwork = self.filename + '\\ControlNetwork'
        self.tableSurveyInfromation = self.filename + '\\SiteInfo'
        self.siteGDB = arcpy.Describe(filename)

    def test(self):
        status = 1
        if arcpy.Exists(self.fcControlNetwork) == 0:
            status = status*0
        if arcpy.Exists(self.tableSurveyInfromation)==0:
            status = status*0
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

    def __init__(self,filename):

        self.filename = filename
        # Feature Datasets
        self.unprojected = filename + "\\Unprojected"
        self.projected = filename + "\\Projected"

        # Survey Data
        self.Control_Points = Control_Points(self.projected)
        self.Topo_Points = Topo_Points(self.projected)
        self.Bankfull_Polygon = Bankfull_Polygon(self.projected)
        self.Bankfull_Centerline = Bankfull_Centerline(self.projected)
        self.Bankfull_CrossSections = Bankfull_CrossSections(self.projected)
        self.Bankfull_Islands = Bankfull_Islands(self.projected)
        self.Benchmarks = Benchmarks(self.projected)
        self.Breaklines = Breaklines(self.projected)
        self.Channel_Units = Channel_Units(self.projected)
        self.Channel_Units_Crew = Channel_Units_Crew(self.projected)
        self.EdgeOfWater_Points = EdgeOfWater_Points(self.projected)
        self.Error_Lines = Error_Lines(self.projected)
        self.Error_Points = Error_Points(self.projected)
        self.Stream_Features = Stream_Features(self.projected)
        self.SurveyExtent = SurveyExtent(self.projected)
        self.Thalweg = Thalweg(self.projected)
        self.Wetted_Centerline = Wetted_Centerline(self.projected)
        self.Wetted_Extent = Wetted_Extent(self.projected)
        self.Wetted_CrossSections = Wetted_CrossSections(self.projected)
        self.Wetted_Islands = Wetted_Islands(self.projected)

        self.fcLiDAR_Points = self.projected + "\\LiDAR_Points"
        self.fcTINEdits = self.projected + "\\TIN_Edits"
        self.fcGeomorphicUnits = self.projected + "\\GeomorphicUnits"
        
        # Tables
        self.tblQaQcPoints = filename + "\\QaQcPoints"
        self.tblQaQcLines = filename + "\\QaQcLines"
        self.tblQaQcPolygons = filename + "\\QaQcPolygons"
        self.tblQaQcVector = filename + "\\QaQcVector"
        self.tblQaQcTIN = filename + "\\QaQcTIN"
        self.tblLog = filename + "\\Log"
        self.tblOrthogInfo = filename + "\\OrthogInfo"
        self.tblSurveyInfo = filename + "\\SurveyInfo"
        self.tblTransformations = filename + "\\Transformations"
        
        # Imported Raw Data
        self.fcQaQcRawPoints = filename + "\\QaQc_RawPoints"
        self.tblQaQcBacksightLog = filename + "\\QaQcBacksightLog"
        self.tblQaQcUncertaintySummary = filename + "\\QaQcUncertaintySummary"
        
        # Raster Dataset
        self.DEM = DEM(self.filename)
        self.DetrendedDEM = DetrendedDEM(self.filename)
        self.WaterDepth =  WaterDepth(self.filename)
        self.WSEDEM =  WSEDEM(self.filename)
        self.DEMHillshade = DEMHillshade (self.filename)
        self.AssocSlope = AssocSlope(self.filename)
        self.AssocPDensity = AssocPDensity(self.filename)
        self.AssocIErr = AssocIErr(self.filename)
        self.Assoc3DPQ = Assoc3DPQ(self.filename)
        self.AssocD50 = AssocD50(self.filename)
        self.ErrSurface = ErrSurface(self.filename)
        self.AssocRough = AssocRough(self.filename)
        
    def getDatasets(self):
        listDatasets = [self.Control_Points,
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
                        self.WaterDepth]
        for dataset in listDatasets:
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
        for dataset in self.getDatasets():
            if dataset.Datatype == "Table":
                yield dataset

    def getExportToGISDatasets(self):
        for dataset in self.getDatasets():
            if dataset.ExportToGIS:
                yield dataset

    def getPublish(self):
        for dataset in self.getDatasets:
            if dataset.Publish:
                yield dataset

    def checkGDBVersion(self):
        if self.getGDBVersion() == self.version:
            return True
        else :
            return False

    def getGDBVersion(self):
        return 

    def getGDBVersionProperties(self):
        print "GDB Version: " + str(self.version)
        for dataset in self.getDatasets():
            print " Name: " + dataset.Name
            print " Datatype: " + dataset.Datatype
            print " Required: " + dataset.Required
            print " Include in Publish: " + dataset.Publish

    def year(self):
        """ returns type Double of contents of FieldSeason in SurveyInfo Table."""

        if arcpy.Exists(self.tblSurveyInfo):
            if arcpy.ListFields(self.tblSurveyInfo,"FieldSeason"):
                with arcpy.da.SearchCursor(self.tblSurveyInfo,["FieldSeason"]) as scTblSurveyInfo:
                    row = scTblSurveyInfo.next()
                    if type == "STRING":
                        return str(row[0])
                    else:
                        return row[0] 

## Base GIS Classes ## 
class GISField():
    lengthStringDefault = 255

    def __init__(self,nameFull,nameShort,type,strlength=lengthStringDefault):
        self.nameFull = nameFull
        self.nameShort = nameShort
        self.type = type
        self.strlength = strlength

    def getFieldMap(self,filename):
        outFieldMap = arcpy.FieldMap()
        outFieldMap.addInputField(filename,self.nameFull)
        outField = outFieldMap.outputField
        outField.name = self.nameShort
        outFieldMap.outputField = outField

        return outFieldMap

class GISTable():
    Datatype="Table"

    def __init__(self,filename):
        self.filename = filename

    def exportTableToXML(self,outputPath):
        return

class GISRaster():
    Datatype="Raster"
    
    def __init__(self,filename):
        self.filename = filename

    def validateExists(self):
        if arcpy.Exists(self.filename):
            return True
        else:
            return False

    def exportToGeoTiff(self,outputPath):
        arcpy.RasterToOtherFormat_conversion(self.filename,outputPath,"TIFF")
        return

class GISVector():
    Datatype="Vector"
    Name = ""

    def __init__(self,GDBProjectedPath):
        self.filename = GDBProjectedPath + "\\" + self.Name
        self.listFields = []

    def addField(self,field):
        self.listFields.append(field)
        return field
        
    def getFieldMapping(self):
        fieldMappings = arcpy.FieldMappings()
        for field in self.listFields:
            if len(arcpy.ListFields(self.filename,field)) == 0 :
                fieldMappings.addFieldMap(field.getFieldMap(self.filename))
        return fieldMappings
    
    def validateExists(self):
        if arcpy.Exists(self.filename):
            return True
        else:
            return False

    def exportToShapeFile(self,outputPath):
        arcpy.FeatureClassToFeatureClass_conversion(self.filename,outputPath,self.Name,field_mapping=self.getFieldMapping())
        return

class GISFile():
    Datatype="File"

    def __init__(self,Path,Name):
        self.Name = Name
        self.filename = Path + "\\" + self.Name

## Fields ## 
class FieldDescription(GISField):
    nameFull = "DESCRIPTION"
    nameShort = "DescCode"
    lengthString = 6

    def __init__(self,codeList):
        GISField.__init__(self,self.nameFull,self.nameShort,"STRING",self.lengthString)
        self.codeList = codeList
        return

class FieldPointNumber(GISField):
    nameFull="POINT_NUMBER"
    nameShort = "PNumber"
    lengthString = 10

    def __init__(self):
      GISField.__init__(self,self.nameFull,self.nameShort,"STRING",self.lengthString)
      return

class FieldExtentType(GISField):
    nameFull = "ExtentType"
    nameShort = "ExtentType"
    listValueFilter = ["Channel",""]

    def __init__(self):
        GISField.__init__(self,self.nameFull,self.nameShort,"STRING")

class FieldChannel(GISField):
    nameFull = "Channel"
    nameShort = "Channel"

    def __init__(self):
        GISField.__init__(self,self.nameFull,self.nameShort,"STRING")

class FieldCLID(GISField):
    nameFull = "CLID"
    nameShort = "CLID"

    def __init__(self):
        GISField.__init__(self,self.nameFull,self.nameShort,"STRING")

class FieldIsValid(GISField):
    nameFull = "IsValid"
    nameShort = "IsValid"

    def __init__(self):
        GISField.__init__(self,self.nameFull,self.nameShort,"STRING")

class FieldQualifying(GISField):
    nameFull = "Qualifying"
    nameShort = "Qualifying"

    def __init__(self):
        GISField.__init__(self,self.nameFull,self.nameShort,"STRING")

class FieldLineType(GISField):
    nameFull = "LineType"
    nameShort = "LineType"

    def __init__(self):
        GISField.__init__(self,self.nameFull,self.nameShort,"STRING")

class FieldChannelUnitNumber(GISField):
    nameFull = "Unit_Number"
    nameShort = "UnitNumber"

    def __init__(self):
        GISField.__init__(self,self.nameFull,self.nameShort,"STRING")

class FieldVDE(GISField):
    nameFull = "VDE"
    nameShort = "VDE"

    def __init__(self):
        GISField.__init__(self,self.nameFull,self.nameShort,"STRING")

class FieldHDE(GISField):
    nameFull = "HDE"
    nameShort = "HDE"

    def __init__(self):
        GISField.__init__(self,self.nameFull,self.nameShort,"STRING")

class FieldPointQuality(GISField):
    nameFull = "POINT_QUALITY"
    nameShort = "PQuality"

    def __init__(self):
        GISField.__init__(self,self.nameFull,self.nameShort,"STRING")

class FieldStation(GISField):
    nameFull = "Station"
    nameShort = "Station"

    def __init__(self):
        GISField.__init__(self,self.nameFull,self.nameShort,"STRING")

class FieldErrorType(GISField):
    nameFull = "ErrorType"
    nameShort = "ErrorType"

    def __init__(self):
        GISField.__init__(self,self.nameFull,self.nameShort,"STRING")

## Vector Datasets ## 
class Control_Points(GISVector):
    """
    """
    Publish = True
    ExportToGIS = True
    Name = "Control_Points"
    Required = True
    listCodes = []

    fieldDescription = FieldDescription(listCodes)
    fieldVDE = FieldVDE()
    fieldHDE = FieldHDE()
    fieldPointQuality = FieldPointQuality()
    fieldStation = FieldStation()
    fieldPointNumber = FieldPointNumber()
    fieldCPType = GISField("Type","Type","STRING")
    fieldCPSource = GISField("Source","Source","STRING")

    def __init__(self,GDBProjected):
        GISVector.__init__(self,GDBProjected)
        self.addField(self.fieldVDE)
        self.addField(self.fieldHDE)
        self.addField(self.fieldDescription)
        self.addField(self.fieldPointNumber )
        self.addField(self.fieldPointQuality)
        self.addField(self.fieldStation)
        self.addField(self.fieldCPType)
        self.addField(self.fieldCPSource)

class Topo_Points(GISVector):
    Publish = True
    ExportToGIS = True
    Name = "Topo_Points"
    Required = True
    listCodes = ["tp%"]

    fieldDescription = FieldDescription(listCodes)
    fieldVDE = FieldVDE()
    fieldHDE = FieldHDE()
    fieldPointQuality = FieldPointQuality()
    fieldStation = FieldStation()
    fieldPointNumber = FieldPointNumber()

    def __init__(self,GDBProjected):
        GISVector.__init__(self,GDBProjected)
        self.addField(self.fieldVDE)
        self.addField(self.fieldHDE)
        self.addField(self.fieldDescription)
        self.addField(self.fieldPointNumber )
        self.addField(self.fieldPointQuality)
        self.addField(self.fieldStation)

class Bankfull_Polygon(GISVector):
    Publish = True
    ExportToGIS = True
    Name = "Bankfull"
    Required = True

    fieldExtent = FieldExtentType()

    def __init__(self,GDBProjected):
        GISVector.__init__(self,GDBProjected)
        self.addField(self.fieldExtent)

class Bankfull_Centerline(GISVector):
    Publish = True
    ExportToGIS = True
    Name = "BankfullCL"
    Required = True

    fieldChannel = FieldChannel()
    fieldCLID = FieldCLID()

    def __init__(self,GDBProjected):
        GISVector.__init__(self,GDBProjected)
        self.addField(self.fieldChannel)
        self.addField(self.fieldCLID)

class Bankfull_CrossSections(GISVector):
    Publish = True
    ExportToGIS = True
    Name = "BankfullXS"
    Required = True

    fieldChannel = FieldChannel()
    fieldIsValid = FieldIsValid()

    def __init__(self,GDBProjected):
        GISVector.__init__(self,GDBProjected)
        self.addField(self.fieldChannel)
        self.addField(self.fieldIsValid)

class Bankfull_Islands(GISVector):
    Publish = True
    ExportToGIS = True
    Name = "BIslands"
    Required = True

    fieldIsValid = FieldIsValid()
    fieldQualifying = FieldQualifying()

    def __init__(self,GDBProjected):
        GISVector.__init__(self,GDBProjected)
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
    Name = "Breaklines"
    Required = True
    lineCodes = []

    fieldDescription = FieldDescription(lineCodes)
    fieldLineTypes = FieldLineType()

    def __init__(self,GDBProjected):
        GISVector.__init__(self,GDBProjected)
        self.addField(self.fieldDescription)
        self.addField(self.fieldLineTypes)

class Channel_Units(GISVector):
    Publish = True
    ExportToGIS = True
    Name = "Channel_Units"
    Required = True
    
    fieldChannelUnitNumber = FieldChannelUnitNumber()

    def __init__(self,GDBProjected):
        GISVector.__init__(self,GDBProjected)
        self.addField(self.fieldChannelUnitNumber)

class Channel_Units_Crew(GISVector):
    Publish = True
    ExportToGIS = False
    Name = "Channel_Units_Field"
    Required = True

    fieldChannelUnitNumber = FieldChannelUnitNumber()

    def __init__(self,GDBProjected):
        GISVector.__init__(self,GDBProjected)
        self.addField(self.fieldChannelUnitNumber)

class EdgeOfWater_Points(GISVector):
    Publish = True
    ExportToGIS = True
    Name = "EdgeofWater_Points"
    Required = True

    fieldDescription = FieldDescription([])
    fieldVDE = FieldVDE()
    fieldHDE = FieldHDE()
    fieldPointQuality = FieldPointQuality()
    fieldStation = FieldStation()
    fieldPointNumber = FieldPointNumber()

    def __init__(self,GDBProjected):
        GISVector.__init__(self,GDBProjected)
        self.addField(self.fieldVDE)
        self.addField(self.fieldHDE)
        self.addField(self.fieldDescription)
        self.addField(self.fieldPointNumber)
        self.addField(self.fieldPointQuality)
        self.addField(self.fieldStation)

class Error_Lines(GISVector):
    Publish = True
    ExportToGIS = True
    Name = "Error_Lines"
    Required = False
    listErrorCodes = ["*"]
    
    fieldDescription = FieldDescription(listErrorCodes)
    fieldLineType = FieldLineType()
    fieldErrorType = FieldErrorType()
    # FieldOriginalLocation

    def __init__(self,GDBProjected):
        GISVector.__init__(self,GDBProjected)
        self.addField(self.fieldDescription)
        self.addField(self.fieldLineType)
        self.addField(self.fieldErrorType)

class Error_Points(GISVector):
    Publish = True
    ExportToGIS = True
    Name = "Error_Points"
    Required = True
    listErrorCodes = ["*"]

    fieldDescription = FieldDescription(listErrorCodes)
    fieldVDE = FieldVDE()
    fieldHDE = FieldHDE()
    fieldPointQuality = FieldPointQuality()
    fieldStation = FieldStation()
    fieldPointNumber = FieldPointNumber()
    fieldErrorType = FieldErrorType()
    # FieldOriginalLocation

    def __init__(self,GDBProjected):
        GISVector.__init__(self,GDBProjected)
        self.addField(self.fieldDescription)
        self.addField(self.fieldVDE)
        self.addField(self.fieldHDE)
        self.addField(self.fieldPointQuality)
        self.addField(self.fieldPointNumber)
        self.addField(self.fieldErrorType)
        self.addField(self.fieldStation)

class Stream_Features(GISVector):
    Publish = True
    ExportToGIS = True
    Name = "Stream_Features"
    Required = True

    fieldDescription = FieldDescription([])
    fieldVDE = FieldVDE()
    fieldHDE = FieldHDE()
    fieldPointQuality = FieldPointQuality()
    fieldStation = FieldStation()
    fieldPointNumber = FieldPointNumber()

    def __init__(self,GDBProjected):
        GISVector.__init__(self,GDBProjected)
        self.addField(self.fieldVDE)
        self.addField(self.fieldHDE)
        self.addField(self.fieldDescription)
        self.addField(self.fieldPointNumber )
        self.addField(self.fieldPointQuality)
        self.addField(self.fieldStation)

class SurveyExtent(GISVector):
    Publish = True
    ExportToGIS = True
    Name = "Survey_Extent"
    Required = True

class Thalweg(GISVector):
    Publish = True
    ExportToGIS = True
    Name = "Thalweg"
    Required = True

    fieldPoolWt = GISField("PoolWt","PoolWt","LONG")
    fieldSmoothT = GISField("SmoothT","SmoothT","LONG")

    def __init__(self,GDBProjected):
        GISVector.__init__(self,GDBProjected)
        self.addField(self.fieldPoolWt)
        self.addField(self.fieldSmoothT)

class Wetted_Centerline(GISVector):
    Publish = True
    ExportToGIS = True
    Name = "CenterLine"
    Required = True

    fieldChannel = FieldChannel()
    fieldCLID = FieldCLID()

    def __init__(self,GDBProjected):
        GISVector.__init__(self,GDBProjected)
        self.addField(self.fieldChannel)
        self.addField(self.fieldCLID)

class Wetted_Extent(GISVector):
    Publish = True
    ExportToGIS = True
    Name = "WaterExtent"
    Required = True

    fieldExtentType = FieldExtentType()

    def __init__(self,GDBProjected):
        GISVector.__init__(self,GDBProjected)
        self.addField(self.fieldExtentType)

class Wetted_CrossSections(GISVector):
    Publish = True
    ExportToGIS = True
    Name = "WettedXS"
    Required = True

    fieldChannel = FieldChannel()
    fieldIsValid = FieldIsValid()

    def __init__(self,GDBProjected):
        GISVector.__init__(self,GDBProjected)
        self.addField(self.fieldChannel)
        self.addField(self.fieldIsValid)

class Wetted_Islands(GISVector):
    Publish = True
    ExportToGIS = True
    Name = "WIslands"
    Required = True

    fieldIsValid = FieldIsValid()
    fieldQualifying = FieldQualifying()

    def __init__(self,GDBProjected):
        GISVector.__init__(self,GDBProjected)
        self.addField(self.fieldIsValid)
        self.addField(self.fieldQualifying)

## Raster Datasets ## 
class DEM(GISRaster):
    name = "DEM"
    Publish = True
    ExportToGIS = True
    Required = True

    def __init__(self,path):
        GISRaster.__init__(self,path+ "\\" + self.name)

class DEMHillshade(GISRaster):
    name = "DEMHillshade"
    Publish = True
    ExportToGIS = True
    Required = True

    def __init__(self,path):
        GISRaster.__init__(self,path+ "\\" + self.name)

class DetrendedDEM(GISRaster):
    name = "Detrended"
    Publish = True
    ExportToGIS = True
    Required = True

    def __init__(self,path):
        GISRaster.__init__(self,path+ "\\" + self.name)

class WaterDepth(GISRaster):
    name = "Water_Depth"
    Publish = True
    ExportToGIS = True
    Required = True

    def __init__(self,path):
        GISRaster.__init__(self,path+ "\\" + self.name)

class WSEDEM(GISRaster):
    name = "WSEDEM"
    Publish = True
    ExportToGIS = True
    Required = True

    def __init__(self,path):
        GISRaster.__init__(self,path+ "\\" + self.name)

class AssocSlope(GISRaster):
    name = "AssocSlope"
    Publish = True
    ExportToGIS = True
    Required = True

    def __init__(self,path):
        GISRaster.__init__(self,path+ "\\" + self.name)

class AssocPDensity(GISRaster):
    name = "AssocPDensity"
    Publish = True
    ExportToGIS = True
    Required = True

    def __init__(self,path):
        GISRaster.__init__(self,path+ "\\" + self.name)

class AssocIErr(GISRaster):
    name = "AssocIErr"
    Publish = True
    ExportToGIS = True
    Required = True

    def __init__(self,path):
        GISRaster.__init__(self,path+ "\\" + self.name)

class Assoc3DPQ(GISRaster):
    name = "Assoc3DPQ"
    Publish = True
    ExportToGIS = True
    Required = True

    def __init__(self,path):
        GISRaster.__init__(self,path+ "\\" + self.name)

class AssocD50(GISRaster):
    name = "AssocD50"
    Publish = True
    ExportToGIS = True
    Required = True

    def __init__(self,path):
        GISRaster.__init__(self,path+ "\\" + self.name)

class AssocRough(GISRaster):
    name = "AssocRough"
    Publish = True
    ExportToGIS = True
    Required = True

    def __init__(self,path):
        GISRaster.__init__(self,path + "\\" + self.name)

class ErrSurface(GISRaster):
    name = "ErrSurface"
    Publish = True
    ExportToGIS = True
    Required = True

    def __init__(self,path):
        GISRaster.__init__(self,path+ "\\" + self.name)

## Tables ##

## OtherFiles ##


