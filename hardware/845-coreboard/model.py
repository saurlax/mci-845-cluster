"""Generate the MCI 845 core board assembly in millimeters."""

from math import atan2, degrees, pi, sqrt
from pathlib import Path

import cadquery as cq
from cadquery.occ_impl.assembly import toCAF
from OCP.Message import Message_ProgressRange
from OCP.RWGltf import RWGltf_CafWriter
from OCP.RWMesh import RWMesh_CoordinateSystem_Zup
from OCP.TCollection import TCollection_AsciiString
from OCP.TColStd import TColStd_IndexedDataMapOfStringString
from OCP.XCAFDoc import XCAFDoc_DocumentTool


PCB_WIDTH = 48.0
PCB_LENGTH = 54.0
PCB_THICKNESS = 1.2
SATA_OVERHANG = 4.0
USB_EDGE_CLEARANCE = 13.0
SINK_WIDTH = 37.0
SINK_GAP = 4.5
SINK_TOP = 17.0
SINK_BASE_THICKNESS = 1.4
MOUNT_PITCH = 59.0
MOUNT_SPAN_X = 43.0
MOUNT_LOW = (2.5, 3.4)
MOUNT_HIGH = (
    MOUNT_LOW[0] + MOUNT_SPAN_X,
    MOUNT_LOW[1] + sqrt(MOUNT_PITCH**2 - MOUNT_SPAN_X**2),
)
SINK_X = (MOUNT_LOW[0] + MOUNT_HIGH[0]) / 2
SINK_Y = (MOUNT_LOW[1] + MOUNT_HIGH[1]) / 2

GREEN = cq.Color(0.093, 0.26, 0.125)
LAMINATE = cq.Color(0.55, 0.40, 0.18)
GOLD = cq.Color(0.83, 0.58, 0.22)
ALUMINUM = cq.Color(0.075, 0.09, 0.11)
PLASTIC = cq.Color(0.061, 0.066, 0.071)
CHIP = cq.Color(0.10, 0.10, 0.11)
STEEL = cq.Color(0.64, 0.68, 0.71)
CREAM = cq.Color(0.89, 0.88, 0.81)
CERAMIC = cq.Color(0.52, 0.42, 0.31)


def box(width, length, height, x, y, z, radius=0):
    part = cq.Workplane("XY").box(width, length, height, centered=(True, True, False))
    if radius:
        part = part.edges("|Z").fillet(radius)
    return part.translate((x, y, z)).val()


def cylinder(radius, height, x, y, z):
    return cq.Solid.makeCylinder(radius, height, cq.Vector(x, y, z))


def compound(parts):
    return cq.Compound.makeCompound(parts)


def board(assembly):
    mask = 0.055
    through_pads = [(46.6, 28.6 + 2.54 * i) for i in range(5)]
    through_pads += [(32.8 + 2.54 * i, 1.75) for i in range(3)]
    through_pads += [(1.5, 44.2 + 2.54 * i) for i in range(3)]
    drills = [cylinder(0.43, 1.8, x, y, -1.5) for x, y in through_pads]
    drills += [cylinder(1.53, 1.8, x, y, -1.5) for x, y in (MOUNT_LOW, MOUNT_HIGH)]

    def layer(thickness, z):
        return box(PCB_WIDTH, PCB_LENGTH, thickness, PCB_WIDTH / 2, PCB_LENGTH / 2, z, 1.35).cut(*drills)

    assembly.add(layer(PCB_THICKNESS - 2 * mask, -PCB_THICKNESS + mask), name="FR4", color=LAMINATE)
    assembly.add(layer(mask, -mask), name="Top solder mask", color=GREEN)
    assembly.add(layer(mask, -PCB_THICKNESS), name="Bottom solder mask", color=GREEN)

    pads = []
    for z in (0.0, -PCB_THICKNESS - 0.035):
        for x, y in through_pads:
            pads.append(cylinder(0.83, 0.035, x, y, z).cut(cylinder(0.43, 0.10, x, y, z - 0.02)))
    assembly.add(compound(pads), name="Plated pads", color=GOLD)


def heatsink(assembly):
    base_top = SINK_GAP + SINK_BASE_THICKNESS
    base = box(SINK_WIDTH, SINK_WIDTH, SINK_BASE_THICKNESS, SINK_X, SINK_Y, SINK_GAP, 0.45)
    ears = []
    holes = []
    for x, y in (MOUNT_LOW, MOUNT_HIGH):
        # Each ear bridges the square base to a mounting hole outside its perimeter.
        ear = cylinder(3.15, SINK_BASE_THICKNESS, x, y, SINK_GAP)
        angle = degrees(atan2(SINK_Y - y, SINK_X - x))
        neck = box(6.0, 4.65, SINK_BASE_THICKNESS, x + 3.0, y, SINK_GAP)
        ears.extend((ear, neck.rotate((x, y, 0), (x, y, 1), angle)))
        holes.append(cylinder(1.47, 2.0, x, y, SINK_GAP - 0.2))
    base = base.fuse(*ears).cut(*holes)

    pitch = 3.18
    pins = []
    for row in range(12):
        for column in range(12):
            x = SINK_X + (column - 5.5) * pitch
            y = SINK_Y + (row - 5.5) * pitch
            pin = (
                cq.Workplane("XY", origin=(x, y, base_top - 0.02))
                .rect(1.38, 1.18)
                .workplane(offset=SINK_TOP - base_top + 0.02)
                .rect(0.96, 0.85)
                .loft(ruled=True)
            )
            pins.append(pin.val())
    aluminum = base.fuse(*pins).clean()
    if len(aluminum.Solids()) != 1:
        raise ValueError("The heatsink base, ears, and fins must form one solid.")
    assembly.add(aluminum, name="Anodized aluminum heatsink", color=ALUMINUM)

    retainers = []
    springs = []
    spring_pitch = 0.81
    spring_radius = 1.85
    spring_top = 10.1
    for x, y in (MOUNT_LOW, MOUNT_HIGH):
        stem = cylinder(1.28, spring_top + PCB_THICKNESS, x, y, -PCB_THICKNESS)
        cap = cylinder(3.10, 1.25, x, y, spring_top)
        barb = cq.Solid.makeCone(0.64, 1.49, 2.05, cq.Vector(x, y, -PCB_THICKNESS - 2.05))
        barb = barb.cut(box(0.57, 3.2, 2.08, x, y, -PCB_THICKNESS - 2.06))
        retainers.append(stem.fuse(cap, barb).clean())

        spring_length = 4.5 * spring_pitch
        helix = cq.Wire.makeHelix(spring_pitch, spring_length, spring_radius)
        profile = cq.Plane(
            origin=(spring_radius, 0, 0),
            xDir=(1, 0, 0),
            normal=(0, 2 * pi * spring_radius / spring_pitch, 1),
        )
        spring = cq.Workplane(profile).circle(0.19).sweep(helix, isFrenet=True).val()
        springs.append(spring.translate((x, y, base_top + 0.22)))
    assembly.add(compound(retainers), name="White push pins", color=CREAM)
    assembly.add(compound(springs), name="Coil springs", color=STEEL)
    assembly.add(box(20, 19, 4.21, SINK_X, SINK_Y, 0.05, 0.5), name="Processor package", color=CHIP)
    assembly.add(box(19, 18, 0.24, SINK_X, SINK_Y, 4.26, 0.3), name="Thermal interface", color=STEEL)


def connectors(assembly):
    # The 7-contact section appears on the left from the heatsink side.
    sata_tip = PCB_LENGTH + SATA_OVERHANG
    bridge = box(43.2, 3.0, 4.0, 24, 52.5, 0, 0.38)
    tongues = []
    contacts = []
    tails = []
    for x, width, count in ((11.85, 10.0, 7), (30.95, 20.15, 15)):
        tongue = box(width, sata_tip - 53.4, 1.35, x, (sata_tip + 53.4) / 2, 1.55, 0.21)
        key = box(0.83, 4.6, 1.23, x + width / 2 - 0.46, (sata_tip + 53.4) / 2, 0.33, 0.10)
        tongues.extend((tongue, key))
        for index in range(count):
            pin_x = x - 0.15 + (index - (count - 1) / 2) * 1.27
            contacts.append(box(0.55, 3.57, 0.065, pin_x, 55.71, 1.485, 0.08))
            tails.append(box(0.46, 2.7, 0.13, pin_x, 49.65, 0.056, 0.065))
    for x in (3.55, 44.45):
        tongues.append(box(2.3, 4.4, 3.20, x, sata_tip - 2.2, 0.38, 0.25))
    assembly.add(bridge.fuse(*tongues).clean(), name="SATA 22-position housing", color=PLASTIC)
    assembly.add(compound(contacts + tails), name="SATA contacts and solder tails", color=GOLD)

    # In the mating view with the PCB above the port, +X is to the left.
    usb_width = 9.2
    usb_x = USB_EDGE_CLEARANCE + usb_width / 2
    usb_z = 1.65
    face = cq.Workplane("XZ", origin=(usb_x, -0.65, usb_z))
    shell = face.slot2D(usb_width, 3.12).extrude(-6.85).val()
    bore = cq.Workplane("XZ", origin=(usb_x, -0.82, usb_z)).slot2D(8.45, 2.48).extrude(-5.95).val()
    assembly.add(shell.cut(bore), name="USB-C shield", color=STEEL)
    assembly.add(box(6.6, 4.7, 0.64, usb_x, 2.77, 1.33, 0.15), name="USB-C tongue", color=PLASTIC)
    fingers = [box(0.20, 1.45, 0.04, usb_x + (i - 5.5) * 0.50, 1.60, 1.97) for i in range(12)]
    assembly.add(compound(fingers), name="USB-C contacts", color=GOLD)
    assembly.add(box(3.5, 3.1, 1.25, 46.15, 17.6, 0, 0.35), name="Side tactile switch", color=STEEL)
    assembly.add(box(0.42, 1.48, 0.78, 47.7, 17.6, 0.23, 0.13), name="Switch actuator", color=PLASTIC)


def components(assembly):
    # Representative component locations are taken from the underside photograph.
    bottom_ics = ((35.2, 26.7, 12.7, 14.0), (10.5, 33.0, 6.6, 6.6),
                  (8.7, 44.5, 4.6, 5.0), (23.8, 44.1, 5.1, 3.9),
                  (7.7, 12.2, 3.8, 4.0))
    packages = [box(w, l, 0.82, x, y, -PCB_THICKNESS - 0.82, 0.14) for x, y, w, l in bottom_ics]
    assembly.add(compound(packages), name="Underside IC packages", color=CHIP)

    bottom_passives = [(7.35 + i * 2.35, 39.15, 1.7, 2.45) for i in range(4)]
    bottom_passives += [(17.0, 28.2 + 2.18 * i, 2.2, 1.45) for i in range(5)]
    bottom_passives += [(7.3 + i * 2.3, 27.6, 1.6, 1.5) for i in range(4)]
    bottom_passives += [(7.1, 16.6, 1.85, 1.35), (9.5, 16.6, 1.85, 1.35), (11.2, 11.0, 1.6, 1.45)]
    for x, y in ((22.8, 23), (19.95, 30), (26.1, 17.2), (27.2, 35.8), (12.6, 44)):
        bottom_passives.extend((x + i * 1.37, y + j * 1.46, 0.9, 0.56) for i in range(4) for j in range(4))

    top_passives = [(9 + i * 2.3, 46.5, 1.1, 0.7) for i in range(15)]
    top_passives += [(27.8 + i * 1.2, 2.15, 0.65, 1.05) for i in range(3)]
    top_passives += [(45.2, 8.5 + i * 1.35, 0.9, 0.63) for i in range(5)]
    caps = []
    ends = []
    for parts, z in ((bottom_passives, -PCB_THICKNESS - 0.40), (top_passives, 0)):
        for x, y, w, l in parts:
            caps.append(box(w * 0.68, l, 0.36, x, y, z + 0.02))
            for side in (-1, 1):
                ends.append(box(w * 0.16, l, 0.4, x + side * w * 0.42, y, z))
    assembly.add(compound(caps), name="Ceramic passives", color=CERAMIC)
    assembly.add(compound(ends), name="Passive end caps", color=STEEL)

    underside = cq.Workplane("XY").transformed(rotate=(0, 180, 0))
    markings = underside.center(-34, 49.1).text("MCI", 4.2, 0.025, font="Arial", kind="bold", combine=False)
    version = underside.center(-34, 45.9).text("MCI_K001_V2_0", 1.05, 0.025, font="Arial", combine=False)
    label = box(6.9, 6.2, 0.09, 41.5, 5.2, -PCB_THICKNESS - 0.09, 0.22)
    ink = [part.translate((0, 0, -PCB_THICKNESS)) for part in markings.vals() + version.vals()]
    assembly.add(compound(ink + [label]), name="Board marking and label", color=CREAM)


def build():
    assembly = cq.Assembly(name="MCI 845 Core Board")
    board(assembly)
    heatsink(assembly)
    connectors(assembly)
    components(assembly)
    for part, name, _, _ in assembly:
        if not part.isValid():
            raise ValueError(f"Invalid CAD geometry in {name}")
    return assembly


def export_glb(model, path):
    _, document = toCAF(model, True, True, 0.06, 0.18)
    XCAFDoc_DocumentTool.SetLengthUnit_s(document, 0.001)
    writer = RWGltf_CafWriter(TCollection_AsciiString(str(path)), True)
    writer.ChangeCoordinateSystemConverter().SetInputCoordinateSystem(RWMesh_CoordinateSystem_Zup)
    if not writer.Perform(document, TColStd_IndexedDataMapOfStringString(), Message_ProgressRange()):
        raise RuntimeError(f"Could not export {path}")


def export_eda_models(model, directory):
    directory.mkdir(exist_ok=True)

    # The vertical device seats at the center of the SATA mating edge.
    translation = cq.Vector(-PCB_WIDTH / 2, 0, PCB_LENGTH + SATA_OVERHANG)
    mount = cq.Location(translation, cq.Vector(1, 0, 0), -90)
    vertical = cq.Assembly(name="MCI 845 Core Board Vertical")
    for part, name, location, color in model:
        vertical.add(part, name=name, loc=mount * location, color=color)
    vertical.export(str(directory / "mci-845-coreboard-vertical.step"))

    source = model.objects["Anodized aluminum heatsink"]
    sink = cq.Assembly(name="MCI 845 Heatsink")
    sink.add(source.obj, name=source.name, color=source.color,
             loc=cq.Location((-SINK_X, -SINK_Y, -SINK_GAP)))
    sink.export(str(directory / "mci-845-heatsink.step"))

    x, y = MOUNT_LOW
    fastener = cq.Assembly(name="MCI 845 Spring Push Pin")
    pin = model.objects["White push pins"]
    tip = pin.obj.BoundingBox().zmin
    for name in ("White push pins", "Coil springs"):
        part = model.objects[name]
        solid = min(part.obj.Solids(), key=lambda shape: shape.Center().x)
        fastener.add(solid, name=name, color=part.color, loc=cq.Location((-x, -y, -tip)))
    fastener.export(str(directory / "mci-845-spring-push-pin.step"))


if __name__ == "__main__":
    directory = Path(__file__).resolve().parent
    assembly_dir = directory / "assembly"
    assembly_dir.mkdir(exist_ok=True)
    model = build()
    model.export(str(assembly_dir / "mci-845-coreboard.step"))
    export_glb(model, assembly_dir / "mci-845-coreboard.glb")
    export_eda_models(model, directory / "eda-models")
