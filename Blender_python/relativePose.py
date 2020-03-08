import bpy
import mathutils
import math
import os
import numpy as np


#import SSSmodule
filename1 = "SSSmodule.py"
exec(bpy.data.texts[filename1].as_string())

#######record ground truth of camera relative pose from t(n+1) to t(n) #######

scn = bpy.data.scenes["Scene"]

#Change name of "Camera" when recording other camera's ground truth
camLeft = bpy.data.objects["Camera"]
#camRight = bpy.data.objects["CameraRight"]

dir = os.path.dirname(bpy.data.filepath)
filename = os.path.join(dir, 'cameraRelativePose.txt')
file4=open(filename, "w")

# First Frame
[R_now, t_now] = [mathutils.Matrix.Identity(3),mathutils.Vector((0,0,0))]

for f in range(scn.frame_start, scn.frame_end +1, scn.frame_step):
    
    [R_pre, t_pre] = [R_now, t_now]
    [R_now, t_now] = getPose(f)
    
    # calculate relative pose
    R_pre.transpose()
    R_rel = R_pre @ R_now 
    t_rel = R_pre @ (t_now - t_pre)
    quat_rel = R_rel.to_quaternion()
    R_pre.transpose()
    
    # go to frame f
    number = f
    # write translation
    file4.write("%s " %str(number))
    for item in t_rel:
        file4.write("%s " %str(round(item,6)))
    # write quaternion    
    for i, item in enumerate(quat_rel):
        if i != len(quat_rel)-1:
            file4.write("%s " %str(round(item,6)))
        else:
            file4.write("%s" %str(round(item,6)))

    file4.write("\n")
     
file4.close()