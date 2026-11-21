"""Build the two-piece printable base for the current 140 x 65 mm assembly."""

from pathlib import Path
import json

import cadquery as cq
import numpy as np
import trimesh

OUT = Path(__file__).resolve().parents[1]
HOLES = [(-3.5, 3.5), (5.5, 47), (129.4001, 3.6001),
         (129.4001, 61.4501), (106.5001, 3.6001), (106.5501, 61.4001)]
FAN_HOLES = [(y, z) for y in (1.75, 63.25) for z in (4.25, 65.75)]


def box(x, y, z, dx, dy, dz):
    return cq.Solid.makeBox(dx, dy, dz, cq.Vector(x, y, z))


def cylinder(radius, length, origin, axis=(0, 0, 1)):
    return cq.Solid.makeCylinder(radius, length, cq.Vector(*origin), cq.Vector(*axis))


# PCB top is Z=0; PCB bottom is Z=-1.6. Bottom components reach Z=-4.
tray = box(-35, -6, -13, 172, 77, 3)
for y in (-6, 68.5):
    tray = tray.fuse(box(-29, y, -10, 166, 2.5, 13))
for x, y in HOLES:
    post = cylinder(3, 8.4, (x, y, -10))
    # Blind pilot for M2.5 plastic-thread screws; tune to the printed coupon.
    post = post.cut(cylinder(1.05, 7, (x, y, -8.6)))
    tray = tray.fuse(post)

# Bottom ventilation slots stay below the PCB, clear of the support posts.
for x in range(18, 94, 12):
    for y in (14, 35):
        tray = tray.cut(box(x, y, -14, 5, 16, 5))

# The panel tongues locate in the base; two M3 screws secure the lower ears.
for y in (13, 52):
    tray = tray.cut(box(-32.2, y-5.2, -14, 3.4, 10.4, 5))
    ear = box(-29, y-5, -10, 6, 10, 8)
    ear = ear.cut(cylinder(1.25, 6, (-29, y, -6), (1, 0, 0)))
    tray = tray.fuse(ear)

panel = box(-32, -5.5, -10, 3, 76, 83)
panel = panel.cut(cylinder(34, 5, (-33, 32.5, 35), (1, 0, 0)))
for y, z in FAN_HOLES:
    panel = panel.cut(cylinder(2.75, 5, (-33, y, z), (1, 0, 0)))
for y in (13, 52):
    panel = panel.fuse(box(-32, y-5, -13, 3, 10, 3))
    panel = panel.cut(cylinder(1.65, 5, (-33, y, -6), (1, 0, 0)))

tray = tray.clean()
panel = panel.clean()
assert tray.isValid() and panel.isValid()
assert len(tray.Solids()) == len(panel.Solids()) == 1
assert tray.intersect(panel).Volume() < 1e-5

parts = {'tray': tray, 'fan-panel': panel}
scene = trimesh.load(OUT.parent / 'assembly/preview/mci-845-eda-assembly-140x65-7020.glb', force='scene')
native = scene.copy()
native.apply_transform(np.array([[1000, 0, 0, 0], [0, 0, -1000, 0],
                                 [0, 1000, 0, 0], [0, 0, 0, 1]]))
native_bottom = float(native.bounds[0, 2])
assert native_bottom > -4.01
fan_envelope = box(-27, -2.5, 0, 20, 70, 70)
assert tray.intersect(fan_envelope).Volume() < 1e-5
assert panel.intersect(fan_envelope).Volume() < 1e-5
transform = np.array([[.001, 0, 0, 0], [0, 0, .001, 0],
                      [0, -.001, 0, 0], [0, 0, 0, 1]])
assembly = cq.Assembly(name='MCI 845 Cluster Printed Base')
checks = {}
for name, shape in parts.items():
    cq.exporters.export(shape, str(OUT / f'cad/printed-base-{name}.step'))
    # Export separate STL files in the print orientation, millimetres, bottom Z=0.
    printable = shape
    if name == 'fan-panel':
        printable = printable.rotate((0, 0, 0), (0, 1, 0), 90)
    b = printable.BoundingBox()
    printable = printable.translate((-b.xmin, -b.ymin, -b.zmin))
    cq.exporters.export(printable, str(OUT / f'print/printed-base-{name}.stl'),
                       tolerance=.08, angularTolerance=.12)
    vertices, triangles = shape.tessellate(.1)
    mesh = trimesh.Trimesh(vertices=[v.toTuple() for v in vertices], faces=triangles,
                           process=True)
    assert mesh.is_watertight
    mesh.visual = trimesh.visual.ColorVisuals(mesh, face_colors=[80, 123, 153, 255])
    mesh.apply_transform(transform)
    scene.add_geometry(mesh, geom_name=f'printed-base-{name}')
    assembly.add(shape, name=name, color=cq.Color(.31, .48, .60))
    checks[name] = {'valid': shape.isValid(), 'solids': len(shape.Solids()),
                    'watertight': bool(mesh.is_watertight),
                    'volume_mm3': shape.Volume(),
                    'print_size_mm': [b.xlen, b.ylen, b.zlen]}

assembly.save(str(OUT / 'cad/printed-base-assembly.step'))
# Hardware is schematic, with smooth shanks; no threaded CAD geometry.
for index, (y, z) in enumerate(FAN_HOLES):
    screw = cylinder(4.5, 2.5, (-34.5, y, z), (1, 0, 0)).fuse(
        cylinder(2.5, 10, (-32, y, z), (1, 0, 0)))
    spacer = cylinder(4.5, 2, (-29, y, z), (1, 0, 0)).cut(
        cylinder(2.75, 2, (-29, y, z), (1, 0, 0)))
    for label, shape, color in [('screw', screw, [165, 169, 175, 255]),
                                 ('spacer', spacer, [65, 68, 73, 255])]:
        vertices, triangles = shape.tessellate(.1)
        mesh = trimesh.Trimesh(vertices=[v.toTuple() for v in vertices], faces=triangles)
        mesh.visual.face_colors = color
        mesh.apply_transform(transform)
        scene.add_geometry(mesh, geom_name=f'fan-{label}-{index+1}')
scene.export(OUT / 'preview/printed-base-140x65-7020.glb')
checks.update({'units': 'mm', 'pcb_top_z': 0, 'pcb_support_z': -1.6,
               'floor_top_z': -10, 'bottom_component_min_z': native_bottom,
               'bottom_component_floor_gap': native_bottom+10,
               'fan_envelope_intersection_mm3': 0,
               'fan_panel_to_frame_gap': 2,
               'fan_side_wall_gap': 1,
               'pcb_mount_holes': HOLES, 'fan_mount_yz': FAN_HOLES,
               'panel_tray_intersection_mm3': tray.intersect(panel).Volume(),
               'fan_screw_tip_x': -22,
               'fan_screw_tip_recess_from_inner_face': 15,
               'fasteners': {'fan': '4 x 5x10 fan self-tapping screws, 2 mm spacers',
                             'panel': '2 x M3x10 plastic-thread screws',
                             'pcb': '6 x M2.5x6 plastic-thread screws'}})
(OUT / 'checks/printed-base-check.json').write_text(json.dumps(checks, indent=2)+'\n', encoding='utf-8')
print(json.dumps(checks, indent=2))
