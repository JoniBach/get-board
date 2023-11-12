import bpy
from mathutils import Matrix

class ShrinkCubesProperties(bpy.types.PropertyGroup):
    tolerance: bpy.props.FloatProperty(
        name="Tolerance",
        default=10.0,
        description="Tolerance for shrinking cubes (+ or -)",
        min=-100.0,
        max=100.0
    )

def shrink_selected_cubes(obj, shrink_amount_mm):
    # Check if the object is a cube
    if obj.type == 'MESH' and obj.data.name.startswith('Cube'):
        # Get the original scale of the object
        original_scale = obj.scale.copy()

        # Calculate the shrink scale factor for each axis
        scale_factor = 1 - (shrink_amount_mm / 1000)
        scale_x = original_scale.x * scale_factor
        scale_y = original_scale.y * scale_factor
        scale_z = original_scale.z 

        # Apply the shrink transformation
        obj.scale = (scale_x, scale_y, scale_z)

class OBJECT_OT_ShrinkCubes(bpy.types.Operator):
    bl_idname = "object.shrink_cubes"
    bl_label = "Shrink Cubes"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        properties = context.scene.shrink_cubes_properties
        tolerance = properties.tolerance

        # Get the selected objects
        selected_objects = context.selected_objects

        # Iterate through selected objects and apply shrink_selected_cubes with the specified tolerance
        for obj in selected_objects:
            shrink_selected_cubes(obj, tolerance)

        return {'FINISHED'}


class ShrinkCubesPanel(bpy.types.Panel):
    bl_label = "Shrink Cubes"
    bl_idname = "PT_ShrinkCubesPanel"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = 'Boardgasm'
    bl_context = "objectmode"

    def draw(self, context):
        layout = self.layout
        properties = context.scene.shrink_cubes_properties

        layout.prop(properties, "tolerance")
        layout.operator(OBJECT_OT_ShrinkCubes.bl_idname)


def register():
    bpy.utils.register_class(ShrinkCubesProperties)
    bpy.utils.register_class(OBJECT_OT_ShrinkCubes)
    bpy.utils.register_class(ShrinkCubesPanel)
    bpy.types.Scene.shrink_cubes_properties = bpy.props.PointerProperty(type=ShrinkCubesProperties)


def unregister():
    bpy.utils.unregister_class(ShrinkCubesProperties)
    bpy.utils.unregister_class(OBJECT_OT_ShrinkCubes)
    bpy.utils.unregister_class(ShrinkCubesPanel)
    del bpy.types.Scene.shrink_cubes_properties


if __name__ == "__main__":
    register()
