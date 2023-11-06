import bpy
from mathutils import Vector

class CreateBoxPanel(bpy.types.Panel):
    bl_label = "Create Box Panel"
    bl_idname = "PT_CreateBoxPanel"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = 'Tool'

    def draw(self, context):
        layout = self.layout

        # Add a field for height input
        layout.prop(context.scene, "box_height", text="Height (mm)")

        # Add a button to trigger the operator
        layout.operator("object.create_box")

class CreateBoxOperator(bpy.types.Operator):
    bl_idname = "object.create_box"
    bl_label = "Create Box on Top"

    def execute(self, context):
        # Get the selected object (assumes it's a box)
        selected_object = context.active_object

        if selected_object:
            # Calculate the new box's location to be on top of the selected object
            new_box_location = selected_object.location + Vector((0, 0, selected_object.dimensions.z))

            # Create a new box at the calculated location
            bpy.ops.mesh.primitive_cube_add(size=1, location=new_box_location)  # Convert mm to meters

            # Get the newly created box
            new_box = context.active_object

            # Set the scale of the new box to match the selected object's dimensions
            new_box.scale = selected_object.dimensions  # Set the scale

        return {'FINISHED'}


classes = (CreateBoxPanel, CreateBoxOperator)

def register():
    for cls in classes:
        bpy.utils.register_class(cls)
    bpy.types.Scene.box_height = bpy.props.FloatProperty(name="Height (mm)", default=10.0, min=0.1, description="Height of the new box in millimeters")

def unregister():
    for cls in classes:
        bpy.utils.unregister_class(cls)
    del bpy.types.Scene.box_height

if __name__ == "__main__":
    register()
