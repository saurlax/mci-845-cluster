"""Bind all package models and promote the confirmed assembly to the main EDA project."""

import argparse
from copy import deepcopy
import csv
import hashlib
import json
from pathlib import Path
import shutil
import time
import uuid

import cadquery as cq


ROOT = Path(__file__).resolve().parents[4]
MAIN = ROOT / "hardware/backplane/mci-845-backplane"
MODELS = MAIN / "models"
LIBRARY = Path.home() / "Documents/LCEDA-Pro/libraries"
SYSTEM_LIBRARY = "0819f05c4eef4c71ace90d822a990e87"


def uid():
    return uuid.uuid4().hex[:16]


def read_records(path):
    result = []
    for line in path.read_text(encoding="utf-8-sig").splitlines():
        h, v = line.split("||", 1)
        result.append((json.loads(h), json.loads(v[:-1]) if v[:-1] else None))
    return result


def write_records(path, records):
    path.write_text("\n".join(json.dumps(h, separators=(",", ":")) + "||" +
                    (json.dumps(v, ensure_ascii=False, separators=(",", ":")) if v is not None else "") + "|"
                    for h, v in records) + "\n", encoding="utf-8")


def groups_of(records):
    groups = []
    for record in records:
        if record[0]["type"] == "DOCHEAD":
            groups.append([])
        groups[-1].append(record)
    return groups


def box(w, l, h, x=0, y=0, z=0):
    return cq.Workplane("XY").box(w, l, h, centered=(True, True, False)).translate((x, y, z)).val()


def export_model(name, shape_or_assembly):
    path = MODELS / ("mci-845-" + name + ".step")
    if isinstance(shape_or_assembly, cq.Assembly):
        shape_or_assembly.export(str(path))
        shape = cq.Compound.makeCompound([s.moved(loc) for s, n, loc, color in shape_or_assembly if s])
    else:
        cq.exporters.export(shape_or_assembly, str(path))
        shape = shape_or_assembly
    shutil.copy2(path, LIBRARY / path.name)
    b = shape.BoundingBox()
    values = [b.xlen / .0254, b.ylen / .0254, 0, 0, 0, 0,
              (b.xmin + b.xmax) / 2 / .0254,
              (b.ymin + b.ymax) / 2 / .0254, b.zmin / .0254]
    return {"3D Model": path.name + "|" + str(LIBRARY),
            "3D Model Title": path.stem,
            "3D Model Transform": ",".join(f"{v:.6f}" for v in values)}


def models():
    MODELS.mkdir(exist_ok=True)
    LIBRARY.mkdir(exist_ok=True, parents=True)
    cache = ROOT / "references/radxa-zero-3w/1eac96aa8804f7270e08610ebd99bf0eccfd26d39d859fae76d119406694ded3.brep"
    zero = (cq.Shape.importBrep(str(cache)) if cache.exists() else
            cq.importers.importStep(str(ROOT / "hardware/reference-models/radxa-zero-3w/radxa-zero-3w-v1.11.step")).val())
    b = zero.BoundingBox()
    raw_name = "mci-845-zero3w-stock.step"
    shutil.copy2(ROOT / "hardware/reference-models/radxa-zero-3w/radxa-zero-3w-v1.11.step", LIBRARY / raw_name)
    values = [b.xlen/.0254, b.ylen/.0254, 0, 90, 180, 0,
              (15-(b.ymin+b.ymax)/2)/.0254, (32.5-(b.xmin+b.xmax)/2)/.0254,
              (20-b.zmin)/.0254]
    result = {"zero": {"3D Model": raw_name + "|" + str(LIBRARY),
                       "3D Model Title": "Radxa ZERO 3W Stock Inverted",
                       "3D Model Transform": ",".join(map(str, values))}}
    print("Prepared stock-header Zero STEP", flush=True)
    fan = cq.importers.importStep(str(ROOT / "hardware/reference-models/delta-7020/delta-afc0712dd-tp10.step")).val()
    fan = fan.rotate((0, 0, 0), (1, 1, 0), 180).translate((-10, 0, 35))
    result["fan"] = export_model("delta-7020", fan)
    post = cq.Solid.makeCylinder(2.5, 20).cut(cq.Solid.makeCylinder(1.25, 20))
    assembly = cq.Assembly(name="M2.5 20mm standoff")
    assembly.add(post, name="Brass", color=cq.Color(.72, .55, .23))
    result["post"] = export_model("standoff-m2p5-h20", assembly)
    socket = box(5.08, 50.8, 17.5)
    openings = [box(.85, .85, 6.1, x, (i - 9.5) * 2.54, 11.5)
                for x in [-1.27, 1.27] for i in range(20)]
    socket = socket.cut(*openings)
    assembly = cq.Assembly(name="2x20 elevated socket reference")
    assembly.add(socket, name="Insulator", color=cq.Color(.09, .10, .11))
    result["socket"] = export_model("socket-2x20-h17p5-reference", assembly)
    for count, pitch in [(2, 2.5), (3, 2.54)]:
        assembly = cq.Assembly(name=f"{count} pin header reference")
        assembly.add(box(count * pitch, 2.5, 2.5), name="Insulator", color=cq.Color(.08, .08, .09))
        pins = [box(.64, .64, 11.5, (i - (count - 1) / 2) * pitch, 0, -3) for i in range(count)]
        assembly.add(cq.Compound.makeCompound(pins), name="Pins", color=cq.Color(.78, .65, .32))
        result[f"hdr{count}"] = export_model(f"header-{count}p-reference", assembly)
    # Bundle the existing core-board model with the project as well.
    source = ROOT / "hardware/845-coreboard/eda-models/mci-845-coreboard-vertical.step"
    shutil.copy2(source, MODELS / source.name)
    shutil.copy2(source, LIBRARY / source.name)
    print("Prepared 7020, socket, standoffs and utility headers", flush=True)
    return result


def bind_cloud(model_uuid, name, x_mm, y_mm, rotation=0):
    return {"3D Model": model_uuid + "|" + SYSTEM_LIBRARY, "3D Model Title": name,
            "3D Model Transform": f"{x_mm/.0254:.6f},{y_mm/.0254:.6f},0,{rotation},0,0,0,0,0"}


def main(trial):
    if trial.resolve() == MAIN.resolve():
        raise ValueError("The trial project must be separate from the main project")
    trial_index = next(trial.glob("*.eprj3"))
    path = trial / "pcb/Backplane.epcb2"
    groups = groups_of(read_records(path))
    backup = ROOT / "references/eda-before-full-models"
    if backup.exists():
        raise FileExistsError("Integration backup already exists; inspect before rerunning")
    shutil.copytree(MAIN, backup / "main", ignore=shutil.ignore_patterns("debug.log"))
    shutil.copytree(trial, backup / "trial", ignore=shutil.ignore_patterns("debug.log"))
    local = models()
    board = groups[-1]
    refs = {v["parentId"]: v["value"] for h, v in board
            if h["type"] == "ATTR" and v and v.get("key") == "Designator"}
    live = json.loads((ROOT / "references/live-components-only.json").read_text(encoding="utf-8-sig"))["value"]
    lookup = {c["ref"]: c for c in live}
    bindings = {}
    # Preserve explicitly bound or inherited catalog models, including CH348L.
    for ref, item in lookup.items():
        if item["model"].get("uuid"):
            bindings[ref] = {k: item["other"][k] for k in
                             ["3D Model", "3D Model Title", "3D Model Transform"] if k in item["other"]}
    choices = [
        (["U1"], "97e59798435a404f940acb24f78a13ce", "QFN-24_L4.0-W4.0-H0.9-P0.50", 4, 4, 0),
        (["U2", "U3", "U4"], "3fae3a1420384b2b8b15a88610f8b219", "TSOT-23-6_L2.9-W1.6-H1.1-LS2.8-P0.95", 2.9, 2.8, 90),
        (["U9"], "18da8f6c14a34920b3e136b5c401a119", "SOT-23-6_L2.9-W1.6-H1.5-LS2.8-P0.95", 2.9, 2.8, 90),
        (["U7", "U8"], "25b054d4db3343b88aee285a0a719589", "SOT-23-5_L2.9-W1.6-LS2.8-P0.95", 2.9, 2.8, 90),
        (["U10"], "79d73b47911b4bd5936cf94fb8ee3c25", "SOT-9X3-3_L1.0-W0.8-H0.5-LD1.0-P0.35", 1, 1, 90),
        (["Q1", "Q2"], "ac658f5d71f14f53ab59ffa88c0b695d", "SOP-8_L4.9-W3.9-LS6.0-P1.27", 4.9, 6, 90),
        (["D1"], "0be9a10c06a74ab7b6b40ad1b5d71adc", "SMB_L4.3-W3.6-LS5.4", 5.4, 3.6, 0),
        (["D2"], "01f4e49c15374c35a281576162868eba", "SOD-123_L2.7-W1.8-LS3.7", 3.7, 1.8, 0),
        (["F1"], "929e3e6a172d42b39a921533dce49079", "FUSE-SMD_L7.3-W4.3-reference", 7.3, 4.3, 0),
        ([f"F{i}" for i in range(2, 9)], "be76f212bbea4dba990f93e8149b533a", "FUSE-SMD_L3.2-W1.6-reference", 3.2, 1.6, 0),
        (["L1", "L2", "L3"], "21c28650900a45ea9c2aba0b58e0dfe9", "IND-SMD_L6.0-W6.0-H4.5-reference", 6, 6, 0),
        (["L4", "L5"], "dabddd86e8204879a6801252ad3585a5", "IND-SMD_L2.0-W1.2-reference", 2, 1.2, 0),
        (["Y1", "Y2"], "d7c39c66443246ff83c2003c1e1eb6f1", "CRYSTAL-SMD_L5.0-W3.2-reference", 5, 3.2, 0),
    ]
    for names, model_uuid, title, x, y, angle in choices:
        for ref in names:
            bindings[ref] = bind_cloud(model_uuid, title, x, y, angle)
    bindings["J8"] = local["hdr2"]
    bindings["J11"] = local["hdr3"]
    # DNP remains an assembly attribute; bind the same 0603 package for inspection.
    for ref, item in lookup.items():
        if ref not in bindings and ref.startswith("R"):
            bindings[ref] = deepcopy(bindings["R1"])
        if ref not in bindings and ref.startswith("C"):
            bindings[ref] = deepcopy(bindings["C2"])
    log = []
    for h, v in board:
        if h["type"] != "COMPONENT":
            continue
        ref = refs[h["id"]]
        if ref.startswith("MECH"):
            continue
        assert ref in bindings and bindings[ref].get("3D Model"), ref
        v["attrs"].update(bindings[ref])
        log.append({"designator": ref, "model": bindings[ref]["3D Model Title"],
                    "binding": bindings[ref]["3D Model"], "placement": "bottom" if v["layerId"] == 2 else "top",
                    "status": "DNP" if "DNP" in (lookup[ref].get("name") or "") else "fitted"})
    # Keep the fan power connector's existing two electrical pins.
    for h, v in board:
        if h["type"] == "ATTR" and v and refs.get(v.get("parentId")) == "J8" and v.get("key") == "Name":
            v["value"] = "7020 Fan Power"

    template_symbol = next(g for g in groups if g[0][1]["uuid"] == "2000952d793b51ea")
    template_fp = next(g for g in groups if g[0][1]["uuid"] == "61d0b5875b7d90ff")
    template_device = next(g for g in groups if g[0][1]["uuid"] == "2f67018a80f41d64")
    core_comp = next((h, v) for h, v in board if h["type"] == "COMPONENT" and refs.get(h["id"]) == "MECH1")
    core_attrs = [(h, v) for h, v in board if h["type"] == "ATTR" and v and v.get("parentId") == core_comp[0]["id"]]
    specs = [("MECH7", "Radxa ZERO 3W Inverted", "zero", 118, 32.5, 30, 65),
             ("MECH8", "Delta AFC0712DD-TP10 7020", "fan", -17, 32.5, 20, 70),
             ("MECH9", "Zero Outer Standoff Lower", "post", 129.4001, 3.6001, 5, 5),
             ("MECH10", "Zero Outer Standoff Upper", "post", 129.4001, 61.4501, 5, 5),
             ("MECH11", "40-Pin Elevated Socket Reference", "socket", 106.325, 32.55, 5.08, 50.8)]
    for ref, title, key, x, y, width, height in specs:
        symbol_id, fp_id, device_id = uid(), uid(), uid()
        ids = {"2000952d793b51ea": symbol_id, "61d0b5875b7d90ff": fp_id,
               "2f67018a80f41d64": device_id}
        docs = []
        for template in [template_symbol, template_fp, template_device]:
            text = json.dumps(template)
            for old, new in ids.items():
                text = text.replace(old, new)
            doc = json.loads(text)
            for hh, vv in doc:
                if hh["type"] == "META":
                    vv["title"] = title
                    if doc[0][1]["docType"] == "DEVICE":
                        vv["attributes"].update(local[key])
                        vv["attributes"].update({"Name": title, "Footprint": fp_id, "Symbol": symbol_id,
                                                   "Add into BOM": "no", "Convert to PCB": "yes"})
            docs.append(doc)
        fp = [record for record in docs[1] if record[0]["type"] in ("DOCHEAD", "META", "CANVAS", "LAYER")]
        fp.extend([({"type": "LINE", "id": uid()}, {"groupId": 0, "layerId": 9, "netName": "",
                   "startX": a/.0254, "startY": b/.0254, "endX": c/.0254, "endY": d/.0254,
                   "width": 5, "locked": False, "zIndex": -1}) for a,b,c,d in
                   [(-width/2,-height/2,width/2,-height/2),(width/2,-height/2,width/2,height/2),
                    (width/2,height/2,-width/2,height/2),(-width/2,height/2,-width/2,-height/2)]])
        docs[1] = fp
        groups[-1:-1] = docs
        hh, vv = deepcopy(core_comp)
        component_id = uid()
        hh["id"] = component_id
        vv.update(x=x/.0254, y=y/.0254, angle=0, pinSwapInfo={})
        vv["attrs"] = {"Add into BOM": "no", "Unique ID": "", "DeviceName": json.dumps({"name": title, "source": "", "uuid": device_id}), **local[key]}
        board.append((hh, vv))
        for ah, av in deepcopy(core_attrs):
            ah["id"] = uid()
            av.update(parentId=component_id, x=None, y=None, keyVisible=False, valueVisible=False)
            if av["key"] == "Designator": av["value"] = ref
            elif av["key"] == "Footprint": av["value"] = fp_id
            elif av["key"] == "Name": av["value"] = title
            board.append((ah, av))
        log.append({"designator": ref, "model": local[key]["3D Model Title"], "binding": local[key]["3D Model"],
                    "placement": "top", "status": "mechanical"})
    revision = int(time.time()*1000)
    for g in groups:
        if g[0][1]["docType"] == "PCB":
            g[0][1].update(version=str(revision), updateTime=revision)
    records = [record for group in groups for record in group]
    for i, (h, v) in enumerate(records): h["ticket"] = i + 1
    write_records(path, records)
    trial_data = json.loads(trial_index.read_text(encoding="utf-8"))
    for item in trial_data["profile"]["pcbs"].values(): item.update(version=str(revision), updateTime=revision)
    trial_index.write_text(json.dumps(trial_data, indent=2, ensure_ascii=False)+"\n", encoding="utf-8")

    # Promote the confirmed layout while retaining the main project's identities.
    main_index = next(MAIN.glob("*.eprj3"))
    main_data = json.loads(main_index.read_text(encoding="utf-8"))
    replacement = {}
    for group_name in ["boards", "schematics", "sheets", "pcbs"]:
        old_items = main_data["profile"][group_name]
        for trial_id, item in trial_data["profile"][group_name].items():
            title = item.get("title", item.get("name"))
            main_id = next(k for k,v in old_items.items() if v.get("title",v.get("name")) == title)
            replacement[trial_id] = main_id
    text = path.read_text(encoding="utf-8")
    for old,new in replacement.items(): text=text.replace(old,new)
    (MAIN/"pcb/Backplane.epcb2").write_text(text,encoding="utf-8")
    for item in main_data["profile"]["pcbs"].values(): item.update(version=str(revision),updateTime=revision)
    main_data["name"] = "MCI 845 Cluster"
    main_data["content"] = "140x65 backplane; inverted ZERO 3W; Delta 7020; complete component model bindings"
    main_index.write_text(json.dumps(main_data,indent=2,ensure_ascii=False)+"\n",encoding="utf-8")
    report = {"component_count": len(log)+6, "bindings": log,
              "local_models": {p.name:hashlib.sha256(p.read_bytes()).hexdigest() for p in MODELS.glob("*.step")},
              "main_project":main_index.relative_to(ROOT).as_posix(),
              "scope":"3D package and assembly integration; electrical nets preserved; routing remains in progress"}
    (MODELS/"model-bindings.json").write_text(json.dumps(report,indent=2)+"\n",encoding="utf-8")
    with (MODELS/"model-bindings.csv").open("w",encoding="utf-8",newline="") as f:
        writer=csv.DictWriter(f,fieldnames=["designator","model","binding","placement","status"])
        writer.writeheader();writer.writerows(log)
    print("Integrated",len(log)+6,"components into",main_index,flush=True)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("trial", type=Path, help="Path to the pre-migration trial project folder")
    main(parser.parse_args().trial)
