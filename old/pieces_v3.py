import bpy, bmesh
from mathutils import Vector
from functools import reduce

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
                new_box_location = selected_object.location + Vector((0, 0, 0)) # selected_object.dimensions.z

                # Calculate the new box's dimensions with the same height as the selected object
                new_box_dimensions = selected_object.dimensions + Vector((2 * box_margin, 2 * box_margin, 0))

                bpy.ops.mesh.primitive_cube_add(size=1, location=new_box_location)  # Convert mm to meters
                new_box = context.active_object

                # Set the scale of the new box to match the adjusted dimensions, but keep the height constant
                new_box.scale.x = new_box_dimensions.x
                new_box.scale.y = new_box_dimensions.y
                
                for obj in bpy.context.selected_objects:
                    if obj.type == 'MESH':
                        
                        bpy.context.view_layer.objects.active = obj
                        obj.select_set(True)

                        # Switch to Edit Mode for the currently active object
                        bpy.ops.object.mode_set(mode='EDIT')
                        faces = bpy.context.object.data.polygons   
                        for face in faces:                   
                            face.select=False    
                        
                            me = bpy.context.active_object.data
                            bm = bmesh.from_edit_mesh(me)

                            # Deselect all faces
                            for face in bm.faces:
                                face.select = False

                            tuples = map(lambda x: (x, x.calc_center_median().z), bm.faces)
                            top_face = reduce(lambda a, b: a if a[1] > b[1] else b, tuples)[0]

                            top_face.select_set(True)

                            bmesh.update_edit_mesh(me)

            bpy.ops.transform.translate(value=(0.0, 0.0, 1.0), constraint_axis=(False, False, True))
            bpy.ops.object.mode_set(mode='OBJECT')  

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
