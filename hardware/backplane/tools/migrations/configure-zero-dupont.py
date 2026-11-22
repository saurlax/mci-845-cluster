"""Use four independent Zero mounting posts and remove the direct-mating socket."""
from copy import deepcopy
import csv
import json
from pathlib import Path
import shutil
import time
import uuid

ROOT = Path(__file__).resolve().parents[4]
PROJECTS = [ROOT/'hardware/backplane/mci-845-backplane']
INNER_HOLES = [('MH5','MECH11',106.5001,3.6001),('MH6','MECH12',106.5501,61.4001)]

def uid(): return uuid.uuid4().hex[:16]
def read(path):
    groups=[]
    for line in path.read_text(encoding='utf-8-sig').splitlines():
        h,v=line.split('||',1); h=json.loads(h); v=json.loads(v.removesuffix('|')) if v.removesuffix('|') else None
        if h['type']=='DOCHEAD': groups.append([])
        groups[-1].append((h,v))
    return groups

def main():
    backup=ROOT/'references'/('zero-before-dupont-'+str(int(time.time())))
    for project in PROJECTS:
        dest=backup/project.name; dest.mkdir(parents=True)
        shutil.copy2(project/'pcb/Backplane.epcb2',dest/'Backplane.epcb2')
        index=next(project.glob('*.eprj3'));shutil.copy2(index,dest/index.name)
        groups=read(project/'pcb/Backplane.epcb2'); board=groups[-1]
        refs={v['parentId']:v['value'] for h,v in board if h['type']=='ATTR' and v.get('key')=='Designator'}
        comps={refs[h['id']]:(h,v) for h,v in board if h['type']=='COMPONENT'}
        socket=comps['MECH11']; assert 'socket' in socket[1]['attrs']['3D Model']
        socket_device=json.loads(socket[1]['attrs']['DeviceName'])['uuid']
        socket_fp=next(v['value'] for h,v in board if h['type']=='ATTR' and v.get('parentId')==socket[0]['id'] and v['key']=='Footprint')
        device=next(g for g in groups if g[0][1]['uuid']==socket_device)
        attrs=next(v['attributes'] for h,v in device if h['type']=='META')
        remove_docs={socket_device,socket_fp,attrs['Symbol']}
        groups=[g for g in groups if g[0][1]['uuid'] not in remove_docs]
        net_before=sorted(json.dumps(v,sort_keys=True) for h,v in board if h['type']=='PAD_NET')
        board[:]=[(h,v) for h,v in board if h.get('id')!=socket[0]['id'] and not (h['type']=='ATTR' and v.get('parentId')==socket[0]['id']) and not (h['type']=='REGION' and v.get('name')=='ZERO 3W 40-PIN CORRIDOR')]
        pad=next((h,v) for h,v in board if h['type']=='PAD' and v.get('num')=='MH3')
        region=next((h,v) for h,v in board if h['type']=='REGION' and v.get('path') and v['path'][0][0]=='CIRCLE')
        post=comps['MECH9'];post_attrs=[(h,v) for h,v in board if h['type']=='ATTR' and v.get('parentId')==post[0]['id']]
        for hole,ref,x,y in INNER_HOLES:
            h,v=deepcopy(pad);h['id']=uid();v.update(num=hole,centerX=x/.0254,centerY=y/.0254);board.append((h,v))
            h,v=deepcopy(region);h['id']=uid();v['path']=[['CIRCLE',x/.0254,y/.0254,3/.0254]];board.append((h,v))
            h,v=deepcopy(post);h['id']=uid();comp_id=h['id'];v.update(x=x/.0254,y=y/.0254);v['attrs']['Description']='Independent Zero mounting post; Dupont wiring; height selected for cooler clearance';board.append((h,v))
            for ah,av in deepcopy(post_attrs):
                ah['id']=uid();av['parentId']=comp_id
                if av['key']=='Designator':av['value']=ref
                if av['key']=='Name':av['value']='Zero Inner Standoff '+('Lower' if hole=='MH5' else 'Upper')
                board.append((ah,av))
        net_after=sorted(json.dumps(v,sort_keys=True) for h,v in board if h['type']=='PAD_NET');assert net_before==net_after
        # New mounting keepouts must fit within the current routing.
        conflicts=[]
        for h,v in board:
            if h['type']=='LINE' and v.get('layerId') in [1,2,15,16]:
                ax,ay,bx,by=[v[k]*.0254 for k in ['startX','startY','endX','endY']]
                for _,_,x,y in INNER_HOLES:
                    dx,dy=bx-ax,by-ay;t=max(0,min(1,((x-ax)*dx+(y-ay)*dy)/(dx*dx+dy*dy))) if dx*dx+dy*dy else 0
                    if (ax+t*dx-x)**2+(ay+t*dy-y)**2<(3+v.get('width',0)*.0254/2)**2:conflicts.append(h['id'])
            elif h['type']=='VIA':
                for _,_,x,y in INNER_HOLES:
                    if (v['centerX']*.0254-x)**2+(v['centerY']*.0254-y)**2<3**2:conflicts.append(h['id'])
        assert not conflicts,('Routing intersects new mounting keepouts',conflicts)
        rev=int(time.time()*1000);board[0][1].update(version=str(rev),updateTime=rev)
        records=[r for g in groups for r in g]
        for i,(h,v) in enumerate(records):h['ticket']=i+1
        (project/'pcb/Backplane.epcb2').write_text('\n'.join(json.dumps(h,separators=(',',':'))+'||'+(json.dumps(v,ensure_ascii=False,separators=(',',':')) if v is not None else '')+'|' for h,v in records)+'\n',encoding='utf-8')
        index_data=json.loads(index.read_text(encoding='utf-8'));index_data['content']='140x65 backplane; four-post ZERO 3W mount; Dupont wiring; Delta 7020'
        for item in index_data['profile']['pcbs'].values():item.update(version=str(rev),updateTime=rev)
        index.write_text(json.dumps(index_data,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
        print(project.name, '211 components; 6 mounting holes; 847 pad nets preserved; new keepouts clear',flush=True)
    models=PROJECTS[0]/'models';report_path=models/'model-bindings.json';report=json.loads(report_path.read_text())
    template=deepcopy(next(a for a in report['bindings'] if a['designator']=='MECH9'))
    report['bindings']=[a for a in report['bindings'] if a['designator']!='MECH11']
    for _,ref,_,_ in INNER_HOLES:
        item=deepcopy(template);item['designator']=ref;report['bindings'].append(item)
    report['component_count']=211;report.pop('validation',None)
    report['mounting']={'connection':'User-configurable Dupont leads; no directly mating baseboard 40-pin socket','preview_post_height_mm':20,'zero_holes_mm':[[129.4001,3.6001],[129.4001,61.4501],[106.5001,3.6001],[106.5501,61.4001]],'baseboard_hole_diameter_mm':2.9,'copper_keepout_diameter_mm':6}
    report_path.write_text(json.dumps(report,indent=2)+'\n',encoding='utf-8')
    with (models/'model-bindings.csv').open('w',encoding='utf-8',newline='') as f:
        w=csv.DictWriter(f,fieldnames=['designator','model','binding','placement','status']);w.writeheader();w.writerows(report['bindings'])
    print('Backup:',backup)

if __name__=='__main__':main()
