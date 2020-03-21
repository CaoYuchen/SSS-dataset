import bpy
import os

#switch to rgb_right when recording riight camera 
rgb = 'rgb'
#rgb = 'rgb_right'

# create /rgb folder if not exist
if not os.path.exists(rgb):
    os.makedirs(rgb)

# set data storage path    
dir = os.path.dirname(bpy.data.filepath)
filename = os.path.join(dir, rgb+'\\')
print(filename)
bpy.context.scene.render.filepath = filename

# use left camera as default to capture depth image
bpy.context.scene.camera = bpy.data.objects["Camera"]
#bpy.context.scene.camera = bpy.data.objects["CameraRight"]

# turn on depth of field
bpy.data.objects["Camera"].data.dof.use_dof = True
#bpy.data.objects["CameraRight"].data.dof.use_dof = True


# set image format as 16-bit grayscale PNG
bpy.context.scene.render.image_settings.file_format = 'PNG'
bpy.context.scene.render.image_settings.color_mode = 'RGB'
bpy.context.scene.render.image_settings.color_depth = '8'
bpy.context.scene.render.image_settings.compression = 30

# set data as rgb image
bpy.context.scene.view_settings.view_transform = 'Filmic'
bpy.data.scenes["Scene"].node_tree.nodes["Switch"].check = False


# render and export data under ./rgb folder
# you can either use code below or click Render->Render Animation to render & export the images

bpy.ops.render.render(animation=True, write_still=False, use_viewport=True, layer="", scene="")
