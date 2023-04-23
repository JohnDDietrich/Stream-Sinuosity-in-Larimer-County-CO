# Final Project NR 426
# Creator: John Dietrich
# March 2021

# This program analyzes stream morphology from appropriate inputs of a stream layer and a geographically matched DEM or DEMs.
# It produces a shapefile containing the start and end points for all of the stream segments greater than 5000 m in
# length.  It also contains fields containing Sinuosity (stream length/straight line distance), and gradient (straight
# line distance/ change in elevation).

# Imports
import arcpy, sys
workspace = r"C:\Users\John\OneDrive\Desktop\NR426\FinalProject\Final_Data"
arcpy.env.workspace = workspace
arcpy.env.overwriteOutput = True


# Input and output Variables hard coded
Stream = "Stream.shp"
DEM1 = "imgn41w107_1.img"
DEM2 = "USGS_1_n41w106.tif"
DEM3 = "USGS_NED_1_n41w105_IMG.img"
StreamAnalysis = "StreamAnalysis.shp"


# Input Variables using script tool
Stream = arcpy.GetParameterAsText(0)
DEM1 = arcpy.GetParameterAsText(1)
DEM2 = arcpy.GetParameterAsText(2)
DEM3 = arcpy.GetParameterAsText(3)
StreamAnalysis = arcpy.GetParameterAsText(4)


# Variable for processing intermediate files
StreamsSelect = "StreamSelect.shp"
StreamsCSV = "Streams.csv"
StartPoints = "StartPoints.shp"
EndPoints = "EndPoints.shp"
EndPointsElv = "EndPointsElv.shp"
DEM = "DEM.tif"
StreamAnalysis = "StreamAnalysis.shp"


# Allow for user input of stream feature class and DEM
# Initially hard coded


# Evaluate data
# Existance
print("Do the files exist?")
print(Stream + " file exists: "  + str(arcpy.Exists(Stream)))
print(DEM1 + " file exists: "  + str(arcpy.Exists(Stream)))
print(DEM2 + " file exists: "  + str(arcpy.Exists(Stream)))
print(DEM3 + " file exists: "  + str(arcpy.Exists(Stream)))
print()

# Evaluate Stream layer
print("Stream layer properties:")
Streamproperties = arcpy.Describe(Stream)
spref = arcpy.Describe(Stream).spatialReference
print(Stream + " coordinate system: " + spref.name)
print(Stream + " ShapeType: " + str(Streamproperties.shapeType))
print()

print("DEM layers properties:")
# Raster cell size
DEM1properties = arcpy.Describe(DEM1)
print()
print(DEM1 + " Properties:")
Rspref = DEM1properties.spatialReference
print("Coordinate System: " + str(DEM1properties.spatialReference.name))
print("Band Count:       %d" % DEM1properties.bandCount)
print("Compression Type: %s" % DEM1properties.compressionType)
print("Raster Format:    %s" % DEM1properties.format)
print("Permanent:        %s" % DEM1properties.permanent)
print("Sensor Type:      %s" % DEM1properties.sensorType)

DEM2properties = arcpy.Describe(DEM2)
print()
print(DEM2 + " Properties:")
print("Coordinate System: " + str(DEM2properties.spatialReference.name))
print("Band Count:       %d" % DEM2properties.bandCount)
print("Compression Type: %s" % DEM2properties.compressionType)
print("Raster Format:    %s" % DEM2properties.format)
print("Permanent:        %s" % DEM2properties.permanent)
print("Sensor Type:      %s" % DEM2properties.sensorType)


DEM3properties = arcpy.Describe(DEM3)
print()
print(DEM3 + " Properties:")
print("Coordinate System: " + str(DEM3properties.spatialReference.name))
print("Band Count:       %d" % DEM3properties.bandCount)
print("Compression Type: %s" % DEM3properties.compressionType)
print("Raster Format:    %s" % DEM3properties.format)
print("Permanent:        %s" % DEM3properties.permanent)
print("Sensor Type:      %s" % DEM3properties.sensorType)


# Allow for user input of stream feature class and DEM
# Initially hard coded



# Check Streams fields
print("\nChecking stream data for Length field...")
fields = arcpy.ListFields(Stream)
for x in fields:
    L = False
    if x.name == "Length":
        print("The Length field already exists")
        L = True
if L == False:
    print("The stream data does not have a Length field.  This field will be created...")

# Create Length column.
try:
    arcpy.AddField_management(Stream, "Length", "FLOAT")
except Exception as e:
    print(e)


# Check that new LENGTH field has been created
fields = arcpy.ListFields(Stream)
for x in fields:
    if x.name == "Length":
        print("The Length field has been created.")

# Populate using CalculateGeometry
print("Calculating stream segment lengths for column= Length...")
try:
    arcpy.management.CalculateGeometryAttributes(Stream, [["Length", "LENGTH"]], "METERS")
except Exception as e:
    print(e)



# Use MakeFeatureLayer to make a data layer from the streams feature class that can be selected on.
# Select streams with names and minimum length perhaps 5 km using Select by Attributes
print("Selecting the named stream segments with length > 5000 m")
StreamLayer = arcpy.MakeFeatureLayer_management(Stream, "stm", "Name <> '' And Length > 5000 ")


# Create new feature class based on selection using CopyLayer tool
arcpy.CopyFeatures_management(StreamLayer, StreamsSelect)

print("There are " + str(arcpy.GetCount_management(StreamsSelect,)) + " named stream segments with a length of 5000+ m.\n"
                                                                      "This program will evaluate the sinuosity and gradient"
                                                                      " for theses segments. ")


# Add 5 new columns: line start x, line start y, line end x, line end y, and straight-line distance for each feature
print("Adding columns for the start and end coordinates for each segment")
arcpy.AddField_management(StreamsSelect, "Start_x", "FLOAT")
arcpy.AddField_management(StreamsSelect, "Start_y", "FLOAT")
arcpy.AddField_management(StreamsSelect, "End_x", "FLOAT")
arcpy.AddField_management(StreamsSelect, "End_y", "FLOAT")



# Populate new columns using CalculateGeometry

print("Calculating the start and stop of each stream segment...")
try:
    arcpy.management.CalculateGeometryAttributes(StreamsSelect, [["Start_x", "LINE_START_X"], ["Start_y", "LINE_START_Y"],
                                                                 ["End_x", "LINE_END_X"], ["End_y", "LINE_END_Y"]],
                                                 "METERS")
except Exception as e:
    print(e)
    sys.exit()

# Export attribute table to csv

print("Writing to csv")
try:
    arcpy.conversion.TableToTable(StreamsSelect, workspace, StreamsCSV)
except Exception as e:
    print(e)



# Create new points layer using xyTableToPoint tool.
# Create a variable for the original stream layer spatial reference
# The spref variable was made above like so ::::::   spref = arcpy.Describe(Stream).spatialReference

print("Creating a point layer with the start points and a second layer with the stop points for each\n" +
      " stream segment using the same coordinate system: " + str(spref.name))

# arcpy.management.XYTableToPoint(in_table, out_feature_class, x_field, y_field, {z_field}, {coordinate_system})

arcpy.management.XYTableToPoint(StreamsCSV, StartPoints, "Start_x", "Start_y", "", spref)
arcpy.management.XYTableToPoint(StreamsCSV, EndPoints, "End_x", "End_y", "", spref)

### Raster Processing ###

# Bring together DEMs with Mosaic

# Create base raster to be mosiaced to
Rspref = DEM1properties.spatialReference

# Combine up to 3 DEM layers as necessary using MosaicToNewRaster tool
if arcpy.Exists(DEM3):
    arcpy.MosaicToNewRaster_management([DEM1, DEM2, DEM3], workspace, DEM, Rspref, "32_BIT_UNSIGNED", "", "1")
elif arcpy.Exists(Dem2):
    arcpy.MosaicToNewRaster_management([DEM1, DEM2], workspace, DEM, Rspref, "32_BIT_UNSIGNED", "", "1")
else:
    DEM = DEM1


# Estimate the elevation of each start and end point using the DEM
import arcpy.sa
arcpy.CheckOutExtension("Spatial")

arcpy.sa.ExtractValuesToPoints(StartPoints, DEM, StreamAnalysis, "INTERPOLATE")
arcpy.sa.ExtractValuesToPoints(EndPoints, DEM, EndPointsElv, "INTERPOLATE")

arcpy.CheckInExtension("Spatial")

# Join the start points layer to the end points layer
arcpy.management.JoinField(StreamAnalysis, "OBJECTID_1", EndPointsElv, "OBJECTID_1")

# Add distance fields
arcpy.AddField_management(StreamAnalysis, "Distanceft", "FLOAT")
arcpy.AddField_management(StreamAnalysis, "Distancem", "FLOAT")
arcpy.AddField_management(StreamAnalysis, "Gradient", "FLOAT")
arcpy.AddField_management(StreamAnalysis, "Sinuosity", "FLOAT")

# Calculate the distance between StartPoints and EndPoints

# Use pythagorean theorum to calculate distance between points
arcpy.management.CalculateField(StreamAnalysis, "Distanceft", "((!End_x!-!Start_x!)**2 + (!End_y!-!Start_y!)**2)**0.5")
# Convert distance to meters
arcpy.management.CalculateField(StreamAnalysis, "Distancem", "!Distanceft! * 0.3048!")
#Calculate straight line elevation gradient
arcpy.management.CalculateField(StreamAnalysis, "Gradient", "abs(!RASTERVALU! - !RASTERVA_1!)/!Distancem!")
# Calculate Sinuosity
arcpy.management.CalculateField(StreamAnalysis, "Sinuosity", "!Length!/!Distancem!")

