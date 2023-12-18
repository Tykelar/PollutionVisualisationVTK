
import vtk
import pandas as pd
import numpy as np
#from vtk.util.numpy_support import numpy_to_vtk

import vtkmodules.vtkInteractionStyle
import vtkmodules.vtkRenderingOpenGL2
from vtkmodules.vtkCommonColor import vtkNamedColors
from vtkmodules.vtkFiltersSources import vtkConeSource
from vtkmodules.vtkRenderingCore import (
    vtkActor,
    vtkPolyDataMapper,
    vtkRenderWindow,
    vtkRenderer
)
import os
import sys
DIR_NAME = "../../NOx/"
import time
import copy

#Define Colors
colors = vtkNamedColors()
print("...")

# Read structures data
buildings = pd.read_csv('../../Structures/buildings.txt', sep='\t')
trees = pd.read_csv('../../Structures/trees_baseline.txt', sep='\t')
roads = pd.read_csv('../../Structures/roads.txt', sep='\t')


all_nox_files_names =  []
file_names = sorted(os.listdir(DIR_NAME))

all_nox_data = [ pd.read_csv(f"{DIR_NAME}/{x}", sep='\s+') for x in file_names]

nox_data = None

current_file_index = 0

if all_nox_data:
    nox_data = all_nox_data[current_file_index]
else:
    print("No files detected")
    sys.exit(0)

# Single File Impute read
#nox_data = pd.read_csv('../../NOx/B_NOx_12.dat', sep='\s+')

# # Functions Definitions for the structures

#Function Create Building

def create_building(x, y, z, id):
    # Define the eight vertices of the cube
    points = vtk.vtkPoints()
    points.InsertNextPoint(x[0], y[0], z)  # 0: bottom-left-front
    points.InsertNextPoint(x[1], y[1], z)  # 1: bottom-right-front
    points.InsertNextPoint(x[2], y[2], z)  # 2: top-right-front
    points.InsertNextPoint(x[3], y[3], z)  # 3: top-left-front
    points.InsertNextPoint(x[0], y[0], 0)  # 4: bottom-left-back
    points.InsertNextPoint(x[1], y[1], 0)  # 5: bottom-right-back
    points.InsertNextPoint(x[2], y[2], 0)  # 6: top-right-back
    points.InsertNextPoint(x[3], y[3], 0)  # 7: top-left-back

    # Define the six faces of the cube (topology)
    faces = vtk.vtkCellArray()

    face = vtk.vtkPolygon()
    face.GetPointIds().SetNumberOfIds(4)
    for j in range(4):  # bottom face
        face.GetPointIds().SetId(j, j + 4)
    faces.InsertNextCell(face)

    face = vtk.vtkPolygon()
    face.GetPointIds().SetNumberOfIds(4)
    for j in range(4):  # top face
        face.GetPointIds().SetId(j, j)
    faces.InsertNextCell(face)

    for i in range(4):  # side faces
        face = vtk.vtkPolygon()
        face.GetPointIds().SetNumberOfIds(4)
        face.GetPointIds().SetId(0, i)
        face.GetPointIds().SetId(1, (i + 1) % 4)
        face.GetPointIds().SetId(2, (i + 1) % 4 + 4)
        face.GetPointIds().SetId(3, i + 4)
        faces.InsertNextCell(face)

    # Create a polydata object
    cube = vtk.vtkPolyData()

    # Set the points and polygons
    cube.SetPoints(points)
    cube.SetPolys(faces)

    # Create mapper and actor
    mapper = vtk.vtkPolyDataMapper()
    mapper.SetInputData(cube)

    actor = vtk.vtkActor()
    actor.SetMapper(mapper)
    actor.GetProperty().SetColor(colors.GetColor3d('Peru'))


    return actor


#Function Create Tree

def create_tree(x, y, z, id):
    # Define the eight vertices of the cube
    points = vtk.vtkPoints()
    points.InsertNextPoint(x[0], y[0], z)  # 0: bottom-left-front
    points.InsertNextPoint(x[1], y[1], z)  # 1: bottom-right-front
    points.InsertNextPoint(x[2], y[2], z)  # 2: top-right-front
    points.InsertNextPoint(x[3], y[3], z)  # 3: top-left-front
    points.InsertNextPoint(x[0], y[0], 0)  # 4: bottom-left-back
    points.InsertNextPoint(x[1], y[1], 0)  # 5: bottom-right-back
    points.InsertNextPoint(x[2], y[2], 0)  # 6: top-right-back
    points.InsertNextPoint(x[3], y[3], 0)  # 7: top-left-back

    # Define the six faces of the cube (topology)
    faces = vtk.vtkCellArray()

    face = vtk.vtkPolygon()
    face.GetPointIds().SetNumberOfIds(4)
    for j in range(4):  # bottom face
        face.GetPointIds().SetId(j, j + 4)
    faces.InsertNextCell(face)

    face = vtk.vtkPolygon()
    face.GetPointIds().SetNumberOfIds(4)
    for j in range(4):  # top face
        face.GetPointIds().SetId(j, j)
    faces.InsertNextCell(face)

    for i in range(4):  # side faces
        face = vtk.vtkPolygon()
        face.GetPointIds().SetNumberOfIds(4)
        face.GetPointIds().SetId(0, i)
        face.GetPointIds().SetId(1, (i + 1) % 4)
        face.GetPointIds().SetId(2, (i + 1) % 4 + 4)
        face.GetPointIds().SetId(3, i + 4)
        faces.InsertNextCell(face)

    # Create a polydata object
    cube = vtk.vtkPolyData()

    # Set the points and polygons
    cube.SetPoints(points)
    cube.SetPolys(faces)

    # Create a mapper and actor
    mapper = vtk.vtkPolyDataMapper()
    mapper.SetInputData(cube)

    actor = vtk.vtkActor()
    actor.SetMapper(mapper)
    actor.GetProperty().SetColor(colors.GetColor3d('Green'))


    return actor


#Function Create Roads

def create_road(x, y, id):
    # Define the vertices of the road
    points = vtk.vtkPoints()
    points.InsertNextPoint(x[0], y[0], 0)  # 0: bottom-left-front
    points.InsertNextPoint(x[1], y[1], 0)  # 1: bottom-right-front
    points.InsertNextPoint(x[2], y[2], 0)  # 2: bottom-left-back
    points.InsertNextPoint(x[3], y[3], 0)  # 3: bottom-right-back
    

    # Define the face of the road (topology)
    faces = vtk.vtkCellArray()

    face = vtk.vtkPolygon()
    face.GetPointIds().SetNumberOfIds(4)
    for j in range(4):
        face.GetPointIds().SetId(j, j + 1)
    faces.InsertNextCell(face)


    # Create a polydata object
    rectangle = vtk.vtkPolyData()

    # Set the points and polygons
    rectangle.SetPoints(points)
    rectangle.SetPolys(faces)

    # Create a mapper and actor
    mapper = vtk.vtkPolyDataMapper()
    mapper.SetInputData(rectangle)

    actor = vtk.vtkActor()
    actor.SetMapper(mapper)
    actor.GetProperty().SetColor(colors.GetColor3d('Grey'))

    return actor


# # Pollution Image representation

def grid_creation(nox_data, image_data, color_mapper, image_actor):
    # Determine the grid dimensions
    min_x = nox_data['x'].min()
    min_y = nox_data['y'].min()
    max_x = nox_data['x'].max()
    max_y = nox_data['y'].max()
    print(min_x, min_y, max_x, max_y)
    width = int((max_x - min_x) / 3) + 1
    height = int((max_y - min_y) / 3) + 1

    # Determine the spacing
    spacing_x = (max_x - min_x) / (width - 1)
    spacing_y = (max_y - min_y) / (height - 1)
    print(image_data.GetDimensions())
    # Create an image data object
    image_data.SetDimensions(width, height, 1)

    image_data.SetSpacing(spacing_x, spacing_y, 1) # Set spacing here
    image_data.SetOrigin(min_x, min_y, 0) # Set origin here
    image_data.AllocateScalars(vtk.VTK_FLOAT, 1)

    for index, row in nox_data.iterrows():
        i = int((row['x'] - min_x) / 3)
        j = int((row['y'] - min_y) / 3)
        concentration = row['conc']
        image_data.SetScalarComponentFromFloat(i, j, 0, 0, concentration)
    
    define_color_mapper(ctf=ctf,
                        image_data=image_data,
                        renderer=renderer,
                        color_mapper=color_mapper,
                        image_actor=image_actor)



# # Lookup Tables for Reversion of Color Gradient

# Reversion of Default Table

def define_lookup_table(lookupTable, ctf):
    #lookup_table.SetTableRange(min_concentration, max_concentration) #Set values if desired to visualise for a certain spectrum
    lookupTable.SetNumberOfTableValues(256) # The number can be altered for a smoother gradient
    lookupTable.Build()

    # Reverse the lookup table
    for i in range(256):
        lookupTable.SetTableValue(i, *lookupTable.GetTableValue(255-i))

    # #### Visualisation with specified number of colors
    
    ctf.AddRGBPoint(0, 0, 0, 0)
    ctf.AddRGBPoint(1, 1, 1, 0)
    ctf.AddRGBPoint(2, 1, 0, 0)
    #The first parameter decides which of the two will represent the color for the highest density region meanwhile the other 3 decide on the color chosen
    #The higher the id (first parameter) of the colors, the higher the concentration it will be represention, with the highest accounting for the densest region
    #There can be as many colors as the users want as long they are defined in new lines by incrementing the value of the first parameter

    #Color Codes: 
    # (x, 0, 0, 1) - blue
    # (x, 0, 1, 0) - green
    # (x, 1, 1, 0) - yellow
    # (x, 1, 0, 0) - red
    # (x, 1, 1, 1) - white
    # (x, 0, 0, 0) - black
    return ctf


# # Calling the functions for the structures


def create_structures(renderer):
    # For each building id, create the corresponding actor and add it to the renderer
    for id in buildings['id'].unique():
        building_data = buildings[buildings['id'] == id]
        x = building_data['x'].values
        y = building_data['y'].values
        z = building_data['z'].values[0]  # height is the same for all points of a building
        actor = create_building(x, y, z, id)
        renderer.AddActor(actor)

        # For each tree id, create the corresponding actor and add it to the renderer
    for id in trees['id'].unique():
        tree_data = trees[trees['id'] == id]
        x = tree_data['x'].values
        y = tree_data['y'].values
        z = tree_data['z'].values[0]  # height is the same for all points of a building
        actor = create_tree(x, y, z, id)
        renderer.AddActor(actor)

        # For each road id, create the corresponding actor and add it to the renderer
    for id in roads['id'].unique():
        road_data = roads[roads['id'] == id]
        x = road_data['x'].values
        y = road_data['y'].values
        actor = create_road(x, y, id)
        renderer.AddActor(actor)


# # Glyph Definitions and Pollution Mapper

def define_color_mapper(ctf, image_data, renderer, color_mapper, image_actor, first_time=False):
    
    color_mapper.SetLookupTable(ctf)
    color_mapper.SetInputData(image_data)
    color_mapper.Update()
    #TODO: Check this better :)
    renderer.RemoveActor(image_actor)
   
    image_actor.GetMapper().SetInputData(color_mapper.GetOutput())

    # Add the image actor to the renderer
    renderer.AddActor(image_actor)



# # Legend

def create_scalar_bar(ctf, renderer, scalar_bar):
    
    scalar_bar.SetLookupTable(ctf) # Use here the object created for the lookup table
    scalar_bar.SetTitle("Pollution Concentration")
    scalar_bar.SetNumberOfLabels(3) # Adjust as to provide the number of labels in the table
    scalar_bar.SetLabelFormat("%.2f") # Adjust to format the concentration values

    #Position and size properties
    scalar_bar.SetPosition(0.1, 0.01)
    scalar_bar.SetWidth(0.4)
    scalar_bar.SetHeight(0.1)

    # Add the scalar bar to the renderer
    renderer.AddActor2D(scalar_bar)


def key_press_callback(obj, event,
                        all_nox_data,
                        nox_data,
                        image_data, color_mapper, image_actor):

    key = obj.GetKeySym()
    global current_file_index 
    print(f"Past Index: {current_file_index}")

    if key == "Left":
        print(len(all_nox_data))
        current_file_index = (current_file_index - 1) 
        #print("Left arrow key pressed")

    elif key == "Right":
        current_file_index = (current_file_index + 1)
        #print("Right arrow key pressed")

    time.sleep(2)
    nox_data = all_nox_data[current_file_index]
    print(nox_data)
    print(f"Current Index: {current_file_index}")
    grid_creation(nox_data=nox_data,
                image_data=image_data,
                color_mapper=color_mapper,
                image_actor=image_actor)



# Initialize the renderer
renderer = vtk.vtkRenderer()
#renderer.SetBackground(colors.GetColor3d('LightBlue')) #Note: Background colors often make the visualization more unclear

# Create a render window and add the renderer to it
render_window = vtk.vtkRenderWindow()
render_window.AddRenderer(renderer)
render_window.SetSize(900, 600)
render_window.SetWindowName('25 Abril Maquete com registos de poluicao NO2')


# # Create Interactor

# Create a render window interactor and set the render window for it
interactor = vtk.vtkRenderWindowInteractor()

lookupTable = vtk.vtkLookupTable()
image_data = vtk.vtkImageData()
# Create a scalar bar actor
scalar_bar = vtk.vtkScalarBarActor()
ctf = vtk.vtkColorTransferFunction()
# Create an image actor
image_actor = vtk.vtkImageActor()
# Create a color mapper
color_mapper = vtk.vtkImageMapToColors()


ctf = define_lookup_table(lookupTable=lookupTable, ctf=ctf)
create_structures(renderer=renderer)


grid_creation(nox_data=nox_data,
            image_data=image_data, image_actor=image_actor, color_mapper=color_mapper)


define_color_mapper(ctf=ctf,
                    image_data=image_data,
                    renderer=renderer, image_actor=image_actor, color_mapper=color_mapper)

create_scalar_bar(ctf=ctf,
                  renderer=renderer,
                  scalar_bar=scalar_bar)


interactor.SetRenderWindow(render_window)
interactor.AddObserver("KeyPressEvent",  lambda obj, event: key_press_callback(obj,
                                                                                event, all_nox_data,
                                                                                nox_data,
                                                                                image_data, color_mapper, image_actor))



# Start the visualization
interactor.Initialize()
interactor.Start()


