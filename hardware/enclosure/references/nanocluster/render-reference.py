"""Render the downloaded Sinky shell in its original 3MF component layout."""
from pathlib import Path
import bpy
from mathutils import Vector

OUT = Path(__file__).resolve().parent
bpy.ops.wm.read_factory_settings(use_empty=True)
bpy.ops.import_scene.gltf(filepath=str(OUT/'sinky-nanocluster-parts.glb'))
scene = bpy.context.scene
scene.render.engine = 'BLENDER_WORKBENCH'
scene.display.shading.light = 'STUDIO'
scene.display.shading.color_type = 'MATERIAL'
scene.display.shading.show_cavity = True
scene.display.shading.cavity_type = 'BOTH'
scene.display.shading.show_shadows = True
scene.world = bpy.data.worlds.new('Background')
scene.world.color = (.22,.25,.29)
scene.view_settings.view_transform = 'Standard'
for obj in scene.objects:
    if obj.type!='MESH':continue
    mat=bpy.data.materials.new(obj.name)
    mat.diffuse_color=(.8,.82,.85,1) if obj.name.endswith('1') else (.3,.51,.65,1)
    obj.data.materials.clear();obj.data.materials.append(mat)
points=[obj.matrix_world@Vector(c) for obj in scene.objects if obj.type=='MESH' for c in obj.bound_box]
center=sum(points,Vector())/len(points)
for name,direction in [('reference-parts.png',(.18,-.24,.15)),('reference-inner.png',(-.18,-.24,.12)),('reference-side.png',(.3,0,0))]:
    bpy.ops.object.camera_add(location=center+Vector(direction))
    camera=bpy.context.object
    camera.rotation_euler=(center-camera.location).to_track_quat('-Z','Y').to_euler()
    camera.data.type='ORTHO';camera.data.ortho_scale=.275;camera.data.clip_start=.001
    scene.camera=camera;scene.render.resolution_x=1400;scene.render.resolution_y=1100
    scene.render.filepath=str(OUT/name);bpy.ops.render.render(write_still=True)
    bpy.data.objects.remove(camera,do_unlink=True)
