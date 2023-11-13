# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTIBILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU
# General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>.

bl_info = {
    "name" : "Boardgasm",
    "author" : "Joni Bach",
    "description" : "",
    "blender" : (2, 80, 0),
    "version" : (0, 0, 1),
    "location" : "",
    "warning" : "",
    "category" : "Generic"
}

if "bpy" in locals():
    import importlib
    if "create_board" in locals():
        importlib.reload(create_board)
    if "create_pieces" in locals():
        importlib.reload(create_pieces)
    if "create_tollerance" in locals():
        importlib.reload(create_tollerance)
else:
    from . import create_board
    from . import create_pieces
    from . import create_tollerance

import bpy

def register():
    bpy.utils.register_class(create_board.GridSettingsPanel)
    bpy.utils.register_class(create_board.CreateGridOperator)
    bpy.types.Scene.grid_rows = bpy.props.IntProperty(name="Rows", default=5)
    bpy.types.Scene.grid_columns = bpy.props.IntProperty(name="Columns", default=6)
    bpy.types.Scene.cube_size_x = bpy.props.FloatProperty(name="Cube Size X", default=10.0)
    bpy.types.Scene.cube_size_y = bpy.props.FloatProperty(name="Cube Size Y", default=10.0)
    bpy.types.Scene.cube_size_z = bpy.props.FloatProperty(name="Cube Size Z", default=1.0)
    bpy.types.Scene.cube_size = bpy.props.FloatProperty(name="Cube Size", default=10.0)
    bpy.types.Scene.margin = bpy.props.FloatProperty(name="Margin", default=1.0)
    bpy.types.Scene.base_height = bpy.props.FloatProperty(name="Base Height", default=1.0)
    bpy.types.Scene.cell_radius_degrees = bpy.props.FloatProperty(name="Cell Radius (Degrees)", default=0)
    
    bpy.utils.register_class(create_pieces.CreateBoxesOperator)
    bpy.utils.register_class(create_pieces.CreateBoxPanel)
    bpy.types.Scene.box_height = bpy.props.FloatProperty(name="Height (mm)", default=10.0, min=0.1, description="Height of the new box in millimeters")
    bpy.types.Scene.box_margin = bpy.props.FloatProperty(name="Margin (mm)", default=1.0, min=0.1, description="Margin around the new box in millimeters")

    bpy.utils.register_class(create_tollerance.ShrinkCubesProperties)
    bpy.utils.register_class(create_tollerance.OBJECT_OT_ShrinkCubes)
    bpy.utils.register_class(create_tollerance.ShrinkCubesPanel)
    bpy.types.Scene.shrink_cubes_properties = bpy.props.PointerProperty(type=create_tollerance.ShrinkCubesProperties)


def unregister():
    # Unregister your classes
    bpy.utils.unregister_class(create_board.GridSettingsPanel)
    bpy.utils.unregister_class(create_board.CreateGridOperator)
    del bpy.types.Scene.grid_rows
    del bpy.types.Scene.grid_columns
    del bpy.types.Scene.cube_size_x
    del bpy.types.Scene.cube_size_y
    del bpy.types.Scene.cube_size_z
    del bpy.types.Scene.cube_size
    del bpy.types.Scene.margin
    del bpy.types.Scene.base_height
    del bpy.types.Scene.cell_radius_degrees
    
    bpy.utils.unregister_class(create_board.CreateBoxesOperator)
    bpy.utils.unregister_class(create_board.CreateBoxPanel)
    del bpy.types.Scene.box_height
    del bpy.types.Scene.box_margin
    
    bpy.utils.unregister_class(create_tollerance.ShrinkCubesProperties)
    bpy.utils.unregister_class(create_tollerance.OBJECT_OT_ShrinkCubes)
    bpy.utils.unregister_class(create_tollerance.ShrinkCubesPanel)
    del bpy.types.Scene.shrink_cubes_properties
    
    

if __name__ == "__main__":
    register()