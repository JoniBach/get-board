import bpy
import math

class GridSettingsPanel(bpy.types.Panel):
    bl_label = "Grid Settings"
    bl_idname = "PT_GridSettings"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = 'Tool'

    def draw(self, context):
        layout = self.layout

        # Define the properties for the grid settings
        scene = context.scene
        layout.prop(scene, "grid_rows")
        layout.prop(scene, "grid_columns")
        layout.prop(scene, "cube_size_x")
        layout.prop(scene, "cube_size_y")
        layout.prop(scene, "cube_size_z")
        layout.prop(scene, "margin")
        layout.prop(scene, "base_height")
        layout.prop(scene, "cell_radius_degrees")

        # Add a button to create the grid
        layout.operator("object.create_grid")

class CreateGridOperator(bpy.types.Operator):
    bl_idname = "object.create_grid"
    bl_label = "Create Grid"

    def execute(self, context):
        # Get the grid parameters from the scene properties
        scene = context.scene
        rows = scene.grid_rows
        columns = scene.grid_columns
        cube_size_x = scene.cube_size_x
        cube_size_y = scene.cube_size_y
        cube_size_z = scene.cube_size_z
        margin = scene.margin
        base_height = scene.base_height
        cell_radius_degrees = scene.cell_radius_degrees
        cell_radius_radians = math.radians(cell_radius_degrees)
        gap = margin * 2

        # Create the base
        bpy.ops.mesh.primitive_cube_add(size=1)
        base_obj = bpy.context.object
        base_obj.scale.x = rows * (cube_size_y + gap)
        base_obj.scale.y = columns * (cube_size_x + gap)
        base_obj.scale.z = base_height

        # Position the base to align the corner with the corner of the grid
        base_obj.location.y = (columns * (cube_size_x + gap) - gap) / 2
        base_obj.location.x = (rows * (cube_size_y + gap) - gap) / 2
        base_obj.location.z = base_height

        # Rotate the base to zero degrees in the X-axis (ensure the base is flat)
        base_obj.rotation_euler[0] = 0

        # Create the grid of cubes with rounded corners
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
                cube_obj.location.z = (cube_size_z + base_height)

                # Add a bevel modifier to round the corners
                bpy.ops.object.modifier_add(type='BEVEL')
                bevel_modifier = cube_obj.modifiers[-1]
                bevel_modifier.segments = 3  # You can adjust the number of segments for smoother corners
                bevel_modifier.width = cell_radius_radians

                # Deselect the objects
                cube_obj.select_set(False)

        return {'FINISHED'}

def register():
    bpy.utils.register_class(GridSettingsPanel)
    bpy.utils.register_class(CreateGridOperator)
    bpy.types.Scene.grid_rows = bpy.props.IntProperty(name="Rows", default=5)
    bpy.types.Scene.grid_columns = bpy.props.IntProperty(name="Columns", default=6)
    bpy.types.Scene.cube_size_x = bpy.props.FloatProperty(name="Cube Size X", default=10.0)
    bpy.types.Scene.cube_size_y = bpy.props.FloatProperty(name="Cube Size Y", default=10.0)
    bpy.types.Scene.cube_size_z = bpy.props.FloatProperty(name="Cube Size Z", default=1.0)
    bpy.types.Scene.margin = bpy.props.FloatProperty(name="Margin", default=1.0)
    bpy.types.Scene.base_height = bpy.props.FloatProperty(name="Base Height", default=1.0)
    bpy.types.Scene.cell_radius_degrees = bpy.props.FloatProperty(name="Cell Radius (Degrees)", default=0)

def unregister():
    bpy.utils.unregister_class(GridSettingsPanel)
    bpy.utils.unregister_class(CreateGridOperator)
    del bpy.types.Scene.grid_rows
    del bpy.types.Scene.grid_columns
    del bpy.types.Scene.cube_size_x
    del bpy.types.Scene.cube_size_y
    del bpy.types.Scene.cube_size_z
    del bpy.types.Scene.margin
    del bpy.types.Scene.base_height
    del bpy.types.Scene.cell_radius_degrees

if __name__ == "__main__":
    register()
