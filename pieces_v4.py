import bpy
import bmesh
from mathutils import Vector
from functools import reduce

# Function to create a box on top of the selected object
def create_box_around(selected_object, box_margin, box_height):
    if selected_object.type == 'MESH':
        
        # Calculate the new box's dimensions, including the margin
        new_box_dimensions = selected_object.dimensions + Vector((2 * box_margin, 2 * box_margin, box_height))
        
        # Calculate the new box's location to surround the selected object
        new_box_location = selected_object.location - Vector((0, 0, box_height/2 - new_box_dimensions.z/2))


        bpy.ops.mesh.primitive_cube_add(size=1, location=new_box_location)  # Convert mm to meters
        new_box = bpy.context.active_object

        # Set the scale of the new box to match the adjusted dimensions
        new_box.scale.x = new_box_dimensions.x
        new_box.scale.y = new_box_dimensions.y
        new_box.scale.z = new_box_dimensions.z

# Function to select the top face of the active object in Edit Mode
def select_top_face_in_edit_mode():
    bpy.ops.object.mode_set(mode='EDIT')
    faces = bpy.context.object.data.polygons

    for face in faces:
        face.select = False

    me = bpy.context.active_object.data
    bm = bmesh.from_edit_mesh(me)

    tuples = map(lambda x: (x, x.calc_center_median().z), bm.faces)
    top_face = reduce(lambda a, b: a if a[1] > b[1] else b, tuples)[0]

    top_face.select_set(True)

    bmesh.update_edit_mesh(me)

# Function to translate the active object in Object Mode
def translate_object_in_object_mode():
    bpy.ops.transform.translate(value=(0.0, 0.0, 1.0), constraint_axis=(False, False, True))

# Function to switch to Object Mode
def switch_to_object_mode():
    bpy.ops.object.mode_set(mode='OBJECT')

# Operator class for creating boxes on top
class CreateBoxesOperator(bpy.types.Operator):
    bl_idname = "object.create_boxes"
    bl_label = "Create Boxes Around"
    bl_options = {'REGISTER', 'UNDO'}

    # Additional height parameter for the new boxes
    box_height: bpy.props.FloatProperty(name="Box Height", default=1.0, min=0.1, description="Height of the new boxes")

    def execute(self, context):
        # Get the selected objects
        selected_objects = bpy.context.selected_objects

        # Get user-defined margin value
        box_margin = context.scene.box_margin

        for selected_object in selected_objects:
            create_box_around(selected_object, box_margin, self.box_height)

        return {'FINISHED'}

# CreateBoxPanel
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

# Registration and Unregistration
def register():
    bpy.utils.register_class(CreateBoxesOperator)
    bpy.utils.register_class(CreateBoxPanel)
    bpy.types.Scene.box_height = bpy.props.FloatProperty(name="Height (mm)", default=10.0, min=0.1, description="Height of the new box in millimeters")
    bpy.types.Scene.box_margin = bpy.props.FloatProperty(name="Margin (mm)", default=1.0, min=0.1, description="Margin around the new box in millimeters")

def unregister():
    bpy.utils.unregister_class(CreateBoxesOperator)
    bpy.utils.unregister_class(CreateBoxPanel)
    del bpy.types.Scene.box_height
    del bpy.types.Scene.box_margin

if __name__ == "__main__":
    register()
