import bpy
import mathutils
import os

#import SSSmodule
filename1 = "SSSmodule.py"
exec(bpy.data.texts[filename1].as_string())

scn = bpy.data.scenes["Scene"]


#######record ground truth of camera pose#######

#Change name of "Camera" when recording other camera's ground truth
camLeft = bpy.data.objects["Camera"]
#camRight = bpy.data.objects["CameraRight"]

dir = os.path.dirname(bpy.data.filepath)
filename = os.path.join(dir, 'groundtruth.txt')
file = open(filename, "w")   
for f in range(scn.frame_start, scn.frame_end +1, scn.frame_step):

    # go to frame f
    scn.frame_set(f)
    # get the camera matrix on the current frame
    mat = camLeft.matrix_world
    trans = mat.to_translation()
    orien = getRotation(mat)
    
    # print("Current Frame: %d" % f)
    file.write("%s " %str(f))
    # write translation
    for item in trans:
        file.write("%s " %str(round(item,6)))
    # write quaternion
    for i, item in enumerate(orien):
        if i != len(orien)-1:
            file.write("%s " %str(round(item,6)))
        else:
            file.write("%s" %str(round(item,6)))
                     
    file.write("\n")
     
file.close()




