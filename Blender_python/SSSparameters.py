import bpy
import mathutils

# set the basic unit for Blender
bpy.context.scene.unit_settings.system = 'METRIC'
bpy.context.scene.unit_settings.scale_length = 1
bpy.context.scene.unit_settings.system_rotation = 'DEGREES'
bpy.context.scene.unit_settings.length_unit = 'METERS'
bpy.context.scene.unit_settings.mass_unit = 'KILOGRAMS'
bpy.context.scene.unit_settings.time_unit = 'SECONDS'

# set default camera as left camera
bpy.context.scene.camera = bpy.data.objects["Camera"]

# set fps and length of dataset, (frame_end - frame_start)/fps is the duration[s]
bpy.context.scene.frame_start = 1
bpy.context.scene.frame_step = 1
bpy.context.scene.render.pixel_aspect_x = 1
bpy.context.scene.render.pixel_aspect_y = 1
bpy.context.scene.frame_end = 500
bpy.context.scene.render.fps = 30

# set Resolutions
bpy.context.scene.render.resolution_x = 1024
bpy.context.scene.render.resolution_y = 768
bpy.context.scene.render.resolution_percentage = 100

# set render engine
bpy.context.scene.render.engine = 'BLENDER_EEVEE'
bpy.context.scene.eevee.taa_render_samples = 64
bpy.context.scene.display_settings.display_device = 'sRGB'

# Ambient Occlusion (softness of edge of shadows), distance and factor usually goes from 1.0 to 1.5
bpy.context.scene.eevee.use_gtao = True
bpy.context.scene.eevee.gtao_distance = 1.0
bpy.context.scene.eevee.gtao_factor = 1.0

# Bloom (set self-illuminating objects with light)
bpy.context.scene.eevee.use_bloom = True
bpy.context.scene.eevee.bloom_threshold = 3
# Screen Space Reflection (enable reflection material)
bpy.context.scene.eevee.use_ssr = True
bpy.context.scene.eevee.use_ssr_refraction = True

# Shadows (quality of shadows, higher the parameters, the longer time it takes to render)
bpy.context.scene.eevee.shadow_cascade_size = '4096'
bpy.context.scene.eevee.shadow_cube_size = '512'
bpy.context.scene.eevee.use_shadow_high_bitdepth = True
bpy.context.scene.eevee.use_soft_shadows = False

# Sunlight threshold
bpy.context.scene.eevee.light_threshold = 0.001
# overscan(recover shadows as much as possible)
bpy.context.scene.eevee.use_overscan = True

# set camera parameters/intrinsic matrix
camLeft = bpy.data.objects["Camera"]
# fov, unit is milimeter[mm]
camLeft.data.lens = 24
camLeft.data.lens_unit = 'MILLIMETERS'
# min - max range of camera input, unit is meter[m]
camLeft.data.clip_start = 0.1
camLeft.data.clip_end = 1000

# CCD sensor size, unit is milimeter[mm]
camLeft.data.sensor_width = 35
# Default has no depth of field, approximately equals to the case with F22
# Depth of Field
camLeft.data.dof.use_dof = True
camLeft.data.dof.aperture_fstop = 11
# Focus distance
camLeft.data.dof.focus_distance = 10


camRight = bpy.data.objects["CameraRight"]
# fov, unit is milimeter[mm]
camRight.data.lens = 24
camRight.data.lens_unit = 'MILLIMETERS'
# min - max range of camera input, unit is meter[m]
camRight.data.clip_start = 0.1
camRight.data.clip_end = 1000
# CCD sensor size, unit is milimeter[mm]
camRight.data.sensor_width = 35
# Default has no depth of field, approximately equals to the case with F22
# Depth of Field
camRight.data.dof.use_dof = True
camRight.data.dof.aperture_fstop = 11
# Focus distance
camRight.data.dof.focus_distance = 10

# baseline between two camera, unit is meter[m]
camRight.location[0] = 0.12

# set trajectory length (should be same with length of dataset)
trajectory = bpy.data.objects["animatePath"]
trajectory.data.path_duration = 500


# setTrajectory function
def setTrajectory():
    fpFlag = False
    print(len(camLeft.constraints))
    for constraint in camLeft.constraints:
        if constraint.type == "FOLLOW_PATH":
            fpFlag = True
            camLeft.constraints["Follow Path"].target = bpy.data.objects["animatePath"]
            camLeft.constraints["Follow Path"].influence = 1.0
            
            ### important! ### 
            # Three parameters below may vary for different Bezier curves, change accordingly to adjust camera face forward.
            # Or you can adjust it in "Object Constraint Properties" when "Camera" is selected
            camLeft.constraints["Follow Path"].forward_axis = 'FORWARD_Y'
            camLeft.constraints["Follow Path"].up_axis = 'UP_Z'
            camLeft.constraints["Follow Path"].use_curve_follow = False
    
    if fpFlag == False:
        camLeft.constraints.new("FOLLOW_PATH")
        setTrajectory()
        
# set left camera as zero point of camera groups, and follow the Bezier curve        
setTrajectory()