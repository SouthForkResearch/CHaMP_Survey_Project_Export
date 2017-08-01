# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# Add Z Values to Line Vertex                                                 #
# Developed for CHaMP GIS Tools                                               #
#                                                                             #
# Kelly Whitehead                                                             #
# South Fork Research, Inc.                                                   #
# Seattle Washington                                                          #
#                                                                             #
# Version 4.0                                                                 #
# Modified: 2015-04-14                                                        #
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

# # Import Modules # #
import arcpy
import sys
import os

dblIntersectTol = "0.1"

def polylines(fcLineFeatures, listfcPointFeatures):

    TempPoints = "in_memory\\ZSnap_tempPoints"
    lyrTempPointsLineIntersect = "ZsnapTempPointsLineIntersect"
    lyrLines = "ZsnapLines"

    ## Preprocessing
    if arcpy.Exists(TempPoints):
        arcpy.Delete_management(TempPoints)
    arcpy.Merge_management(listfcPointFeatures,TempPoints)
    if arcpy.Exists(lyrTempPointsLineIntersect):
        arcpy.Delete_management(lyrTempPointsLineIntersect)
    if arcpy.Exists(lyrLines):
        arcpy.Delete_management(lyrLines)
    arcpy.MakeFeatureLayer_management(TempPoints,lyrTempPointsLineIntersect)
    arcpy.MakeFeatureLayer_management(fcLineFeatures,lyrLines,"")
    arcpy.SelectLayerByLocation_management(lyrTempPointsLineIntersect,"INTERSECT",lyrLines)
    TempPointGeometry = arcpy.CopyFeatures_management(lyrTempPointsLineIntersect,arcpy.Geometry())

    ## Run
    with arcpy.da.UpdateCursor(fcLineFeatures,["OID@","SHAPE@"],'','',"True") as ucLines:

        for line in ucLines:
            if line[1] is not None: # Do not process lines with "Null Geometry"
                arcpy.AddMessage("Line Feature: " + str(line[0]))
                arcpy.AddMessage("   Point Count: " + str(line[1].pointCount))
                vertexCount = 0
                vertexArray = []

                arcpy.SelectLayerByAttribute_management(lyrLines,"NEW_SELECTION",'"FID" = ' + str(line[0]))
                arcpy.SelectLayerByLocation_management(lyrTempPointsLineIntersect,"INTERSECT",lyrLines,"","NEW_SELECTION")
                if arcpy.Exists(TempPointGeometry):
                    arcpy.Delete_management(TempPointGeometry)
                TempPointGeometry = arcpy.CopyFeatures_management(lyrTempPointsLineIntersect,arcpy.Geometry())

                for lineVertex in line[1].getPart(vertexCount):
                    arcpy.AddMessage("   Vertex: " + str(vertexCount) + " X:" + str(lineVertex.X) + " Y: " + str(lineVertex.Y))
                    vertexPoint = arcpy.Point(lineVertex.X,lineVertex.Y)
                    vertexPointGeometry = arcpy.PointGeometry(vertexPoint,fcLineFeatures)

                    for pointGeom in TempPointGeometry:
                        intersect = pointGeom.intersect(vertexPointGeometry,1)
                        if intersect.firstPoint:
                            arcpy.AddMessage("   Point Intersect: X: "+ str(intersect.firstPoint.X) + " Y: " + str(intersect.firstPoint.Y))
                            arcpy.AddMessage("       Old Z: " + str(lineVertex.Z))
                            lineVertex.Z = intersect.firstPoint.Z
                            arcpy.AddMessage("       New Z: " + str(lineVertex.Z))
                        #if intersect.pointCount == 0:
                        #    arcpy.AddWarning("   No Intersecting Point Found.") 
                    vertexArray.append([lineVertex.X,lineVertex.Y,lineVertex.Z])
                    vertexCount = vertexCount + 1
                line[1] = vertexArray
                ucLines.updateRow(line)
            else:
                arcpy.AddWarning("Line Feature: " + str(line[0]) + " Has no Geometry.")

    return

if __name__ == '__main__':
    ## Input
    inputlineFeatures = sys.argv[1] # Line Feature Class with featres selected to modify (or modify all if none are selected)
    inputList_fcPointFeatures = sys.argv[2] # Point Feature Class(es) to extract z values.

    polylines(inputlineFeatures,inputList_fcPointFeatures)
