import bpy
import os
from decimal import Decimal

# create /seg folder if not exist
if not os.path.exists('seg'):
    os.makedirs('seg')

# set data storage path    
dir = os.path.dirname(bpy.data.filepath)
filename = os.path.join(dir, 'seg\\')
bpy.context.scene.render.filepath = filename

# use left camera as default to capture semantic image
bpy.context.scene.camera = bpy.data.objects["Camera"]

# set image format as 16-bit grayscale PNG
bpy.context.scene.render.image_settings.file_format = 'PNG'
bpy.context.scene.render.image_settings.color_mode = 'RGB'
bpy.context.scene.render.image_settings.color_depth = '16'
bpy.context.scene.render.image_settings.compression = 30

# set data as semantic image
bpy.context.scene.view_settings.view_transform = 'Raw'
bpy.data.scenes["Scene"].node_tree.nodes["Switch"].check = False

# turn off the lights
lamps = [obj for obj in bpy.data.scenes["Scene"].objects if (obj.type == 'LIGHT' and obj.hide_render == False)]
for lamp in lamps:
    lamp.hide_render = True

# turn off background images
bpy.data.scenes["Scene"].objects["background"].hide_render = True
bpy.data.scenes["Scene"].objects["background.001"].hide_render = True

# turn off bloom & reflection
bpy.context.scene.eevee.use_bloom = False
bpy.context.scene.eevee.use_ssr = False

# turn off hdri environment light
backgroundStrength = bpy.data.worlds["World"].node_tree.nodes["Background"].inputs[1].default_value
bpy.data.worlds["World"].node_tree.nodes["Background"].inputs[1].default_value = 0.0

# delete cached indirect light
if not bpy.context.scene.eevee.gi_cache_info == "No light cache in this scene":
    bpy.ops.scene.light_cache_free()

# make sure objects with same class label are named with same prefix, e.g. chair1 and chair1.001
# two chair instances with same class label.
objects = [ bpy.data.objects["chair1"],
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
            bpy.data.objects["floor"],
            bpy.data.objects["wall"]
            ]

# color for class
# chair1 chair2 chair3 table1 table2 table3
colors = {  "chair1" : (0.206629, 0.203046, 1, 1),
            "chair2" : (0.127456, 0.989233, 1, 1),
            "chair3" : (0.206629, 1, 0.234356, 1),
            "table1" : (1, 0.954345, 0.045231, 1),
            "table2" : (1, 0.203046, 0.323543, 1),
            "table3" : (0.587632, 1, 0.523543, 1),
            "floor"  : (0.560032, 0.200000, 0.02000, 1),
            "wall"   : (0.300000, 0.450000, 0.38000, 1)
            }

# add semantic material for each objects
materialCache = []
for object in objects:
    name, sep, tail = object.name.partition(".")
    segName = name + '_seg'
    
    # if no such material, create one
    material = bpy.data.materials.get(segName)
    if material is None:
        material = bpy.data.materials.new(segName)        
        # set material parameters
        material.use_nodes = True
        BSDF = material.node_tree.nodes["Principled BSDF"]
        material.node_tree.nodes.remove(BSDF)
        emission = material.node_tree.nodes.new(type='ShaderNodeEmission')
        material.node_tree.links.new(emission.outputs['Emission'], material.node_tree.nodes['Material Output'].inputs['Surface'])
        
    # set material color    
    material.node_tree.nodes["Emission"].inputs[0].default_value = colors[name]
    
    # if object has no such material, append it to object    
    mat = [objMat for objMat in object.data.materials if objMat.name == segName]
    if len(mat) == 0:
        object.data.materials.append(material)
    
    # change material to semantic material
    for matSlot in object.material_slots:
        materialCache.append(matSlot.material)
        matSlot.material = material
        

# render and export data under ./seg folder
# you can either use code below or click Render->Render Animation to render & export the images

bpy.ops.render.render(animation=True, write_still=False, use_viewport=False, layer="", scene="")


# recover all light settings
for lamp in lamps:
    lamp.hide_render = False
    
bpy.context.scene.eevee.use_bloom = True
bpy.context.scene.eevee.use_ssr = True
bpy.data.worlds["World"].node_tree.nodes["Background"].inputs[1].default_value = backgroundStrength
bpy.context.scene.view_settings.view_transform = 'Filmic'
bpy.data.scenes["Scene"].objects["background"].hide_render = False
bpy.data.scenes["Scene"].objects["background.001"].hide_render = False
for object in objects:
    for matSlot in object.material_slots:
        matSlot.material = materialCache.pop(0)
#bpy.ops.scene.light_cache_bake()



# record object color map
dir = os.path.dirname(bpy.data.filepath)
filename = os.path.join(dir, 'objectcolor.txt')
file=open(filename, "w")

materials = []
for key in colors:
    materials.append(bpy.data.materials[key + "_seg"])

            
for item in materials:    
    name, sep, tail = item.name.partition(".")
    name = name.replace("_seg","")
    file.write("%s " %name)
    color = item.node_tree.nodes["Emission"].inputs[0].default_value
    color_trans = [round(Decimal(color[0])*65535),round(Decimal(color[1])*65535),round(Decimal(color[2])*65535),round(Decimal(color[3])*65535)]
    file.write("%s %s %s %s" %(color_trans[0],color_trans[1],color_trans[2],color_trans[3]))

    file.write("\n")
     
file.closed