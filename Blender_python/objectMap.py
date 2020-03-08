import bpy
import mathutils
import os


#######record groundtruth of object pose#######
dir = os.path.dirname(bpy.data.filepath)
filename = os.path.join(dir, 'objectmap.txt')
file2=open(filename, "w")

# make sure objects with same class label are named with same prefix, e.g. chair1 and chair1.001
# two chair instances with same class label.
objects = [bpy.data.objects["chair1"],
            bpy.data.objects["chair1.002"],
            bpy.data.objects["chair1.003"],
            bpy.data.objects["chair2"],
            bpy.data.objects["chair2.001"],
            bpy.data.objects["chair3"],
            bpy.data.objects["chair3.001"],
            bpy.data.objects["table1"],
            bpy.data.objects["table1.001"],
            bpy.data.objects["table2"],
            bpy.data.objects["table3"],
            bpy.data.objects["room4"]]
            
#rectify = mathutils.Matrix([[1,0,0,0],[0,0,1,0],[0,-1,0,0],[0,0,0,1]])

for item in objects:
    
    mat = item.matrix_world
    trans = mat.to_translation()
    orien = mat.to_quaternion()
    name, sep, tail = item.name.partition(".")
    
    # print("Current Frame: %d" % f)
    file2.write("%s " %name)
    # write translation
    for item in trans:
        file2.write("%s " %str(round(item,6)))
    # write quaternion
    for i, item in enumerate(orien):
        if i != len(orien)-1:
            file2.write("%s " %str(round(item,6)))
        else:
            file2.write("%s" %str(round(item,6)))

    file2.write("\n")
     
file2.close()