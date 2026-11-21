"""Keep the Zero mounting holes while removing optional board and post models."""
from copy import deepcopy
import csv
import importlib.util
import json
from pathlib import Path
import shutil
import time

ROOT=Path(__file__).resolve().parents[4]
spec=importlib.util.spec_from_file_location('dupont_mount',Path(__file__).with_name('configure-zero-dupont.py'))
mount=importlib.util.module_from_spec(spec);spec.loader.exec_module(mount)
REMOVE={'MECH7','MECH9','MECH10','MECH11','MECH12'}

def main():
    backup=ROOT/'references'/('before-mounting-holes-only-'+str(int(time.time())))
    for project in mount.PROJECTS:
        dest=backup/project.name;dest.mkdir(parents=True)
        pcb=project/'pcb/Backplane.epcb2';index=next(project.glob('*.eprj3'))
        for p in [pcb,index]:shutil.copy2(p,dest/p.name)
        groups=mount.read(pcb);board=groups[-1]
        refs={v['parentId']:v['value'] for h,v in board if h['type']=='ATTR' and v.get('key')=='Designator'}
        removed={h['id'] for h,v in board if h['type']=='COMPONENT' and refs[h['id']] in REMOVE}
        assert len(removed)==5
        device_ids={json.loads(v['attrs']['DeviceName'])['uuid'] for h,v in board if h['type']=='COMPONENT' and h['id'] in removed}
        footprint_ids={v['value'] for h,v in board if h['type']=='ATTR' and v.get('parentId') in removed and v['key']=='Footprint'}
        net_before=[deepcopy(v) for h,v in board if h['type']=='PAD_NET']
        holes_before=[deepcopy(v) for h,v in board if h['type']=='PAD']
        board[:]=[(h,v) for h,v in board if h.get('id') not in removed and not(h['type']=='ATTR' and v.get('parentId') in removed)]
        live_devices={json.loads(v['attrs']['DeviceName'])['uuid'] for h,v in board if h['type']=='COMPONENT' and v.get('attrs',{}).get('DeviceName')}
        live_fps={v['value'] for h,v in board if h['type']=='ATTR' and v.get('key')=='Footprint'}
        delete_docs=(device_ids-live_devices)|(footprint_ids-live_fps)
        symbols=set()
        for g in groups:
            if g[0][1]['uuid'] in device_ids-live_devices:
                symbols.add(next(v['attributes']['Symbol'] for h,v in g if h['type']=='META'))
        other_symbols={v['attributes'].get('Symbol') for g in groups if g[0][1]['docType']=='DEVICE' and g[0][1]['uuid'] not in delete_docs for h,v in g if h['type']=='META'}
        delete_docs|=symbols-other_symbols
        groups=[g for g in groups if g[0][1]['uuid'] not in delete_docs]
        assert net_before==[v for h,v in board if h['type']=='PAD_NET']
        assert holes_before==[v for h,v in board if h['type']=='PAD']
        rev=int(time.time()*1000);board[0][1].update(version=str(rev),updateTime=rev)
        records=[r for g in groups for r in g]
        for i,(h,v) in enumerate(records):h['ticket']=i+1
        pcb.write_text('\n'.join(json.dumps(h,separators=(',',':'))+'||'+(json.dumps(v,ensure_ascii=False,separators=(',',':')) if v is not None else '')+'|' for h,v in records)+'\n',encoding='utf-8')
        d=json.loads(index.read_text(encoding='utf-8'));d['content']='140x65 backplane; optional Zero mounting holes only; Delta 7020'
        for a in d['profile']['pcbs'].values():a.update(version=str(rev),updateTime=rev)
        index.write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
        print(project.name,': 206 components; 6 holes and 847 pad nets unchanged')
    models=mount.PROJECTS[0]/'models';p=models/'model-bindings.json';shutil.copy2(p,backup/'model-bindings.json');report=json.loads(p.read_text())
    report['bindings']=[a for a in report['bindings'] if a['designator'] not in REMOVE];report['component_count']=206
    report['mounting'].pop('preview_post_height_mm',None);report['mounting']['model_scope']='Zero and all four posts removed; six mounting holes and their keepouts retained'
    report.pop('validation',None);p.write_text(json.dumps(report,indent=2)+'\n',encoding='utf-8')
    with p.with_suffix('.csv').open('w',encoding='utf-8',newline='') as f:
        w=csv.DictWriter(f,fieldnames=['designator','model','binding','placement','status']);w.writeheader();w.writerows(report['bindings'])
    print('Backup:',backup)

if __name__=='__main__':main()
