import bpy
import mathutils
import os
import numpy as np

# import SSSmodule
filename1 = "SSSmodule.py"
exec(bpy.data.texts[filename1].as_string())

scn = bpy.data.scenes["Scene"]

dir = os.path.dirname(bpy.data.filepath)
filename = os.path.join(dir, 'imu.txt')
file3=open(filename, "w")


# set times of frequency are amplified for IMU data 
stepscale = 10
# set the fps of camera
fps = bpy.context.scene.render.fps
# set the gravity value m/s^2
gravity = -9.81
# set number of frames
numbFrame = bpy.context.scene.frame_end

# change the path name when you customize the trajectory
trajectory = bpy.data.objects["animatePath"]

# set fps and length of dataset, (frame_end - frame_start)/fps is the duration[s]
bpy.context.scene.frame_start = 1
bpy.context.scene.frame_end = numbFrame * stepscale
bpy.context.scene.render.fps = fps
trajectory.data.path_duration = numbFrame * stepscale

# set the frequency of noise conherent with length of dataset
Action = 'Camera.Action'
Fcurves = bpy.data.actions[Action].fcurves
for item in Fcurves:
    for modifier in item.modifiers:
        if modifier.type == "NOISE":
            modifier.scale = modifier.scale * stepscale
    for keyframe in item.keyframe_points:
        if keyframe.co[0] != 1.0:
            keyframe.co[0] = keyframe.co[0] * stepscale        


# write IMU data
for f in range(scn.frame_start, scn.frame_end +1, scn.frame_step):
    
    trans=list()
    orien=list()
    index = f
    # first and last frame approximation
    if f==scn.frame_start:
        index=index+1
    elif f==(scn.frame_end):
        index=index-1

    for i in range(index-1,index+2,1):
        # go to frame i
        scn.frame_set(i)
        
        mat = scn.camera.matrix_world
        trans.append(mat.to_translation())
        orien.append(getRotation(mat))
        # record the value of middle frame among three frames as the value of current frame.
        if i == index:
             quat = np.asarray(getRotation(mat))
             RCameraToWorld = quaternion_to_rotation(quat)
        
    # world frame acceleration by numerical differentiation
    step = 1/(fps*stepscale)
    accel_x = (trans[2][0]+trans[0][0]-2*trans[1][0]) / (step**2)
    accel_y = (trans[2][1]+trans[0][1]-2*trans[1][1]) / (step**2)
    accel_z = (trans[2][2]+trans[0][2]-2*trans[1][2]) / (step**2) - gravity
    accelWorld = np.array([accel_x,accel_y,accel_z])
    
    # camera frame acceleration
    accel = np.transpose(RCameraToWorld).dot(np.transpose(accelWorld))

    # world frame angular velocity: 
    rotationPrev = quaternion_to_rotation(orien[1])
    rotationLater = quaternion_to_rotation(orien[2])
    angVelWorld = angularVelocity(rotationPrev,rotationLater,step)
    
    # camera frame angular velocity
    angVel = np.transpose(RCameraToWorld).dot(np.transpose(angVelWorld))
    
    number = f
    # print("Current Frame: %d" % f)
    file3.write("%s " %str(number))
    # write translation
    for item in accel:
        file3.write("%s " %str(round(item,6)))
    # write quaternion
    for i, item in enumerate(angVel):
        if i != len(angVel)-1:
            file3.write("%s " %str(round(item,6)))
        else:
            file3.write("%s" %str(round(item,6)))

    file3.write("\n")
     
file3.close()

scn.frame_set(1)
# set fps and length of dataset, (frame_end - frame_start)/fps is the duration[s]
bpy.context.scene.frame_start = 1
bpy.context.scene.frame_end = numbFrame
bpy.context.scene.render.fps = fps
trajectory.data.path_duration = numbFrame

# recover the frequency of noise conherent with length of dataset to original
Action = 'Camera.Action'
Fcurves = bpy.data.actions[Action].fcurves
for item in Fcurves:
    for modifier in item.modifiers:
        if modifier.type == "NOISE":
            modifier.scale = modifier.scale / stepscale
    for keyframe in item.keyframe_points:
        if keyframe.co[0] != 1.0:
            keyframe.co[0] = keyframe.co[0] / stepscale 
