import bpy

def apply_boolean_difference(parent_name, child_name):
    context = bpy.context
    scene = context.scene
    parent = scene.objects.get(parent_name)
    child = scene.objects.get(child_name)

    if parent and child:
        bool = parent.modifiers.new(name='booly', type='BOOLEAN')
        bool.object = child
        bool.operation = 'DIFFERENCE'
        bpy.ops.object.modifier_apply(
            {"object": parent},
            modifier=bool.name
        )
        bpy.data.objects.remove(child)

# Example usage of the function:
parent_object_name = "Cube.003"
child_object_name = "Cube.001"
apply_boolean_difference(parent_object_name, child_object_name)
