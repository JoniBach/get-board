import bpy, bmesh
from functools import reduce
# Iterate through selected objects in 3D view
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