"""Render the printable base assembled and as separate printable parts."""
from pathlib import Path
import bpy
from mathutils import Vector

ROOT = Path(__file__).resolve().parents[1] / "preview"
bpy.ops.wm.read_factory_settings(use_empty=True)
bpy.ops.import_scene.gltf(filepath=str(ROOT / 'printed-base-140x65-7020.glb'))
scene = bpy.context.scene
scene.render.engine = 'BLENDER_WORKBENCH'
scene.display.shading.light = 'STUDIO'
scene.display.shading.color_type = 'MATERIAL'
scene.display.shading.show_cavity = True
scene.display.shading.cavity_type = 'BOTH'
scene.display.shading.show_shadows = True
scene.world = bpy.data.worlds.new('Background')
scene.world.color = (.22, .25, .29)
scene.view_settings.view_transform = 'Standard'
for obj in scene.objects:
    if obj.type != 'MESH' or not obj.data.color_attributes:
        continue
    attribute = obj.data.color_attributes.active_color
    palette = {}
    for face in obj.data.polygons:
        index = face.loop_start if attribute.domain == 'CORNER' else face.vertices[0]
        color = tuple(round(v, 3) for v in attribute.data[index].color)
        if color not in palette:
            mat = bpy.data.materials.new(obj.name + str(len(palette)))
            mat.diffuse_color = color
            obj.data.materials.append(mat)
            palette[color] = len(obj.data.materials)-1
        face.material_index = palette[color]


def render(name, target, direction, scale=.29):
    target = Vector(target)
    bpy.ops.object.camera_add(location=target+Vector(direction))
    camera = bpy.context.object
    camera.rotation_euler = (target-camera.location).to_track_quat('-Z', 'Y').to_euler()
    camera.data.type = 'ORTHO'
    camera.data.ortho_scale = scale
    camera.data.clip_start = .001
    scene.camera = camera
    scene.render.resolution_x = 1600
    scene.render.resolution_y = 1000
    scene.render.resolution_percentage = 100
    scene.render.filepath = str(ROOT / name)
    bpy.ops.render.render(write_still=True)
    bpy.data.objects.remove(camera, do_unlink=True)


render('printed-base-assembly.png', (.05, .0325, .025), (.19, -.24, .16))
render('printed-base-fan-side.png', (.04, .0325, .026), (-.23, -.26, .15))
for obj in scene.objects:
    if obj.type == 'MESH' and not obj.name.startswith('printed-base-'):
        obj.hide_render = True
render('printed-base-parts.png', (.05, .0325, .012), (.19, -.24, .20))
