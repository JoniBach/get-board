import bpy
import math

# Define the number of rows and columns
rows = 5
columns = 6

# Define the dimensions of each cube
cube_size_x = 10.0  # 10mm
cube_size_y = 10.0  # 10mm
cube_size_z = 1.0   # 1mm (height of cubes)

# Define the margin size
margin = 1.0  # 1mm
gap = margin * 2 

# Height of the base
base_height = 1.0  # 1mm

# Create the base
bpy.ops.mesh.primitive_cube_add(size=1)
base_obj = bpy.context.object
base_obj.scale.x = rows * (cube_size_y + gap)
base_obj.scale.y = columns * (cube_size_x + gap)
base_obj.scale.z = base_height

# Position the base to align the corner with the corner of the grid
base_obj.location.y = (columns * (cube_size_x + gap) - gap) / 2
base_obj.location.x = (rows * (cube_size_y + gap) - gap) / 2
base_obj.location.z = base_height / 2

# Rotate the base to zero degrees in the X-axis (ensure base is flat)
base_obj.rotation_euler[0] = 0

# Create the grid of cubes
for i in range(rows):
    for j in range(columns):
        x_pos = i * (cube_size_x + gap)
        y_pos = j * (cube_size_y + gap)

        # Create a new cube with specified dimensions
        bpy.ops.mesh.primitive_cube_add(size=1)
        cube_obj = bpy.context.object
        cube_obj.scale.x = cube_size_x
        cube_obj.scale.y = cube_size_y
        cube_obj.scale.z = cube_size_z
        cube_obj.location.x = x_pos + cube_size_x / 2
        cube_obj.location.y = y_pos + cube_size_y / 2
        cube_obj.location.z = (cube_size_z + base_height) / 2

# Deselect the objects
base_obj.select_set(False)
