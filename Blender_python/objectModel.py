import bpy
import os

# create /object folder if not exist
if not os.path.exists('objects'):
    os.makedirs('objects')

# set data storage path    
dir = os.path.dirname(bpy.data.filepath)
filename = os.path.join(dir, 'objects\\')
bpy.context.scene.render.filepath = filename

# only put objects with different labels into export list
objects = [bpy.data.objects["chair1"],
            bpy.data.objects["chair2"],
            bpy.data.objects["chair3"],
            bpy.data.objects["table1"],
            bpy.data.objects["table2"],
            bpy.data.objects["table3"]
            ]

objectPose = list()
bpy.ops.object.select_all(action='DESELECT')

for object in objects:
    # record current pose
    objectPose = object.matrix_world.copy()
    object.select_set(True)
    
    # reset object's location and rotation
    bpy.ops.object.location_clear()
    bpy.ops.object.rotation_clear()
    
    # make folders for each .obj
    name, sep, tail = object.name.partition(".")
    if not os.path.exists('objects\\'+name):
        os.makedirs('objects\\'+name)
    
    # export .obj
    objectPath = os.path.join(filename, name+'\\'+name+'.obj')
    bpy.ops.export_scene.obj(filepath=objectPath, check_existing=True, axis_forward='Y', axis_up='Z', use_selection=True)
    
    # recover object orginal pose
    object.matrix_world = objectPose
    object.select_set(False)
    
  

