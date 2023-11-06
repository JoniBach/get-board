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

        # Add a field for margin input
        layout.prop(context.scene, "box_margin", text="Margin (mm)")

        # Add a button to trigger the operator
        layout.operator("object.create_boxes")

class CreateBoxesOperator(bpy.types.Operator):
    bl_idname = "object.create_boxes"
    bl_label = "Create Boxes on Top"

    def execute(self, context):
        # Get the selected objects
        selected_objects = bpy.context.selected_objects

        # Get user-defined margin value
        box_margin = context.scene.box_margin

        for selected_object in selected_objects:
            if selected_object.type == 'MESH':
                # Calculate the new box's location to be on top of the selected object
                new_box_location = selected_object.location + Vector((0, 0, selected_object.dimensions.z))

                # Calculate the new box's dimensions with the same height as the selected object
                new_box_dimensions = selected_object.dimensions + Vector((2 * box_margin, 2 * box_margin, 0))

                bpy.ops.mesh.primitive_cube_add(size=1, location=new_box_location)  # Convert mm to meters
                new_box = context.active_object

                # Set the scale of the new box to match the adjusted dimensions, but keep the height constant
                new_box.scale.x = new_box_dimensions.x
                new_box.scale.y = new_box_dimensions.y

        return {'FINISHED'}

classes = (CreateBoxPanel, CreateBoxesOperator)

def register():
    for cls in classes:
        bpy.utils.register_class(cls)
    bpy.types.Scene.box_height = bpy.props.FloatProperty(name="Height (mm)", default=10.0, min=0.1, description="Height of the new box in millimeters")
    bpy.types.Scene.box_margin = bpy.props.FloatProperty(name="Margin (mm)", default=1.0, min=0.1, description="Margin around the new box in millimeters")

def unregister():
    for cls in classes:
        bpy.utils.unregister_class(cls)
    del bpy.types.Scene.box_height
    del bpy.types.Scene.box_margin

if __name__ == "__main__":
    register()
