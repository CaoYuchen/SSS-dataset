import bpy

# set the frequency of noise conherent with length of dataset
Action = 'Camera.Action'
Fcurves = bpy.data.actions[Action].fcurves

# if there is no noise, make noise
for Fcurve in Fcurves:
    noises = [modifier for modifier in Fcurve.modifiers if modifier.type == "NOISE"]
    if len(noises) == 0 :
        Fcurve.modifiers.new("NOISE")
        noises = [modifier for modifier in Fcurve.modifiers if modifier.type == "NOISE"]
    for noise in noises:
        noise.strength = 0.0
        noise.phase = 10.0
        noise.scale = 1.0
 

# set linear noise along X axis
noises = [modifier for modifier in Fcurves[0].modifiers if modifier.type == "NOISE"]
noises[0].strength = 0.0
noises[0].phase = 10.0
noises[0].scale = 1.0
# if you have multiple noises for one fcurve, you should list extra below
#noises[1].strength = 0.0
#noises[1].phase = 10.0
#noises[1].scale = 1.0
#noises[1].use_restricted_range = True
#noises[1].frame_start = 0.0
#noises[1].frame_end = 250.0


# set linear noise along Y axis
noises = [modifier for modifier in Fcurves[1].modifiers if modifier.type == "NOISE"]
noises[0].strength = 0.0
noises[0].phase = 10.0
noises[0].scale = 1.0

# set linear noise along Z axis
noises = [modifier for modifier in Fcurves[2].modifiers if modifier.type == "NOISE"]
noises[0].strength = 0.0
noises[0].phase = 10.0
noises[0].scale = 1.0

# set angular noise around X axis
noises = [modifier for modifier in Fcurves[3].modifiers if modifier.type == "NOISE"]
noises[0].strength = 0.0
noises[0].phase = 10.0
noises[0].scale = 1.0

# set angular noise around Y axis
noises = [modifier for modifier in Fcurves[4].modifiers if modifier.type == "NOISE"]
noises[0].strength = 0.0
noises[0].phase = 10.0
noises[0].scale = 1.0

# set angular noise around Z axis
noises = [modifier for modifier in Fcurves[5].modifiers if modifier.type == "NOISE"]
noises[0].strength = 0.0
noises[0].phase = 10.0
noises[0].scale = 1.0

