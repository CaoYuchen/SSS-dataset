import bpy
import os

# create /depth folder if not exist
if not os.path.exists('depth'):
    os.makedirs('depth')

# set data storage path    
dir = os.path.dirname(bpy.data.filepath)
filename = os.path.join(dir, 'depth\\')
bpy.context.scene.render.filepath = filename

# use left camera as default to capture depth image
bpy.context.scene.camera = bpy.data.objects["Camera"]

# set image format as 16-bit grayscale PNG
bpy.context.scene.render.image_settings.file_format = 'PNG'
bpy.context.scene.render.image_settings.color_mode = 'BW'
bpy.context.scene.render.image_settings.color_depth = '16'
bpy.context.scene.render.image_settings.compression = 30

# set data as depth image
bpy.context.scene.view_settings.view_transform = 'Raw'
bpy.data.scenes["Scene"].node_tree.nodes["Switch"].check = True

# depth factor: 20/65535 means the value 1 in pixel equals to 20/65535 meters in real world.
# you can change this factor for your own purpose.
bpy.data.scenes["Scene"].node_tree.nodes["Math"].inputs[1].default_value = 20

# render and export data under ./depth folder
# you can either use code below or click Render->Render Animation to render & export the images

#bpy.ops.render.render(animation=True, write_still=False, use_viewport=False, layer="", scene="")

# recover original status
#bpy.context.scene.view_settings.view_transform = 'Filmic'
#bpy.data.scenes["Scene"].node_tree.nodes["Switch"].check = False