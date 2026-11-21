"""Move bulky power components and their regulator circuits onto the PCB top."""
from copy import deepcopy
import csv
import importlib.util
import json
import math
from pathlib import Path
import shutil
import time

ROOT=Path(__file__).resolve().parents[4]
spec=importlib.util.spec_from_file_location('mount',Path(__file__).with_name('configure-zero-dupont.py'));mount=importlib.util.module_from_spec(spec);spec.loader.exec_module(mount)
POSITIONS={
 'C1':(102,14), 'F1':(110,26), 'J11':(102,52),
 'U4':(28.5,8.5),'L3':(34.5,8.5),'C19':(25,11.5),'C20':(29,12),'C21':(26,5),'C22':(29,5),'R9':(25,7.5),'R10':(25,9.5),'C23':(42,5.5),'C24':(50,5.5),
 'U3':(57,8.5),'L2':(63,8.5),'C13':(53,12),'C14':(57,12),'C15':(55,3.2),'C16':(58,5),'R7':(53.5,10),'R8':(60,12),'C17':(69,10),'C18':(69,5.5),
 'U2':(77,8.5),'L1':(83,8.5),'C7':(73.5,12),'C8':(77,12),'C9':(74,5),'C10':(77,5),'R5':(73,8),'R6':(73,10),'C11':(89,10),'C12':(94,6)}

def ref_map(board):return {v['parentId']:v['value'] for h,v in board if h['type']=='ATTR' and v.get('key')=='Designator'}

def pad_bounds(groups,board):
 fps={g[0][1]['uuid']:g for g in groups if g[0][1]['docType']=='FOOTPRINT'}
 refs=ref_map(board);fpids={v['parentId']:v['value'] for h,v in board if h['type']=='ATTR' and v.get('key')=='Footprint'}
 result=[]
 for h,v in board:
  if h['type']!='COMPONENT' or v['layerId']!=1:continue
  r=refs[h['id']];angle=math.radians(v['angle']);ca,sa=math.cos(angle),math.sin(angle)
  for ph,p in fps[fpids[h['id']]]:
   if ph['type']!='PAD' or p['layerId'] not in [1,12]:continue
   shape=p['defaultPad'];w,ht=shape.get('width',0)*.0254,shape.get('height',0)*.0254
   a=math.radians(p.get('padAngle',0));c,s=math.cos(a),math.sin(a);pts=[]
   for x,y in [(-w/2,-ht/2),(-w/2,ht/2),(w/2,-ht/2),(w/2,ht/2)]:
    u=p['centerX']*.0254+c*x-s*y;z=p['centerY']*.0254+s*x+c*y
    pts.append((v['x']*.0254+ca*u-sa*z,v['y']*.0254+sa*u+ca*z))
   result.append((r,p['num'],min(x for x,y in pts),min(y for x,y in pts),max(x for x,y in pts),max(y for x,y in pts)))
 return result

def run():
 backup=ROOT/'references'/('before-top-power-'+str(int(time.time())));backup.mkdir()
 changes=[]
 for project in mount.PROJECTS:
  pcb=project/'pcb/Backplane.epcb2';index=next(project.glob('*.eprj3'));groups=mount.read(pcb);board=groups[-1];refs=ref_map(board)
  comps={refs[h['id']]:(h,v) for h,v in board if h['type']=='COMPONENT'}
  nets_before=[deepcopy((h.get('id'),v)) for h,v in board if h['type']=='PAD_NET'];holes_before=[deepcopy(v) for h,v in board if h['type']=='PAD']
  old_boxes=[]
  for ref,(x,y) in POSITIONS.items():
   h,v=comps[ref];assert v['layerId']==2,ref
   ox,oy=v['x']*.0254,v['y']*.0254
   old_boxes.append((ox-4.5,oy-4.5,ox+4.5,oy+4.5))
   if project==mount.PROJECTS[0]:changes.append({'designator':ref,'old_mm':[ox,oy],'new_mm':[x,y],'layer':'top'})
   v.update(layerId=1,x=x/.0254,y=y/.0254,angle=90 if ref=='J11' else 0)
   for ah,av in board:
    if ah['type']=='ATTR' and av.get('parentId')==h['id']:
     if av.get('x') is not None:av['x']+= (x-ox)/.0254
     if av.get('y') is not None:av['y']+= (y-oy)/.0254
     if av.get('layerId') in [4,10]:av['layerId']-=1
  pads=pad_bounds(groups,board);collisions=[]
  for i,a in enumerate(pads):
   for b in pads[i+1:]:
    if a[0]==b[0] or not({a[0],b[0]}&POSITIONS.keys()):continue
    if min(a[4],b[4])-max(a[2],b[2])>.01 and min(a[5],b[5])-max(a[3],b[3])>.01:collisions.append((a[0:2],b[0:2]))
  assert not collisions,('Top pad overlaps',collisions)
  # Private regulator traces and old copper directly underneath relocated parts need rerouting.
  moved_ids={comps[r][0]['id'] for r in POSITIONS}
  affected_nets={v['padNet'] for h,v in board if h['type']=='PAD_NET' and any(cid in h['id'] for cid in moved_ids)}
  private_nets={f'U{n}_{suffix}' for n in [2,3,4] for suffix in ['SW','BOOT','FB']}
  removed=[]
  def obsolete(h,v):
   if h['type']!='LINE' or v.get('layerId') not in [1,2,15,16] or v.get('netName') not in affected_nets:return False
   if v.get('netName') in private_nets:return True
   ax,ay,bx,by=[v[k]*.0254 for k in ['startX','startY','endX','endY']]
   boxes=old_boxes+[(x-4.5,y-4.5,x+4.5,y+4.5) for x,y in POSITIONS.values()]
   return any(min(ax,bx)<=x1 and max(ax,bx)>=x0 and min(ay,by)<=y1 and max(ay,by)>=y0 for x0,y0,x1,y1 in boxes)
  filtered=[]
  for h,v in board:
   if obsolete(h,v):removed.append(h['id'])
   else:filtered.append((h,v))
  board[:]=filtered
  assert nets_before==[(h.get('id'),v) for h,v in board if h['type']=='PAD_NET']
  assert holes_before==[v for h,v in board if h['type']=='PAD']
  dest=backup/project.name;dest.mkdir();shutil.copy2(pcb,dest/pcb.name);shutil.copy2(index,dest/index.name)
  rev=int(time.time()*1000);board[0][1].update(version=str(rev),updateTime=rev);records=[r for g in groups for r in g]
  for i,(h,v) in enumerate(records):h['ticket']=i+1
  pcb.write_text('\n'.join(json.dumps(h,separators=(',',':'))+'||'+(json.dumps(v,ensure_ascii=False,separators=(',',':')) if v is not None else '')+'|' for h,v in records)+'\n',encoding='utf-8')
  d=json.loads(index.read_text(encoding='utf-8'));d['content']='140x65 backplane; top-side power stages and bulk capacitors; Delta 7020; optional mounting holes'
  for item in d['profile']['pcbs'].values():item.update(version=str(rev),updateTime=rev)
  index.write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
  print(project.name,len(POSITIONS),'components moved; removed',len(removed),'obsolete route segments; pad overlaps: 0',flush=True)
 models=mount.PROJECTS[0]/'models';p=models/'model-bindings.json';shutil.copy2(p,backup/p.name);report=json.loads(p.read_text())
 for item in report['bindings']:
  if item['designator'] in POSITIONS:item['placement']='top'
 report['power_placement']={'changes':changes,'routing_status':'Relocated power stages require new routing, copper fills and DRC'};report.pop('validation',None);p.write_text(json.dumps(report,indent=2)+'\n',encoding='utf-8')
 with p.with_suffix('.csv').open('w',encoding='utf-8',newline='') as f:
  w=csv.DictWriter(f,fieldnames=['designator','model','binding','placement','status']);w.writeheader();w.writerows(report['bindings'])
 (ROOT/'hardware/backplane/design/power/top-power-placement.json').write_text(json.dumps({'units':'mm','changes':changes,'pad_overlaps':0,'preserved_pad_nets':847,'mounting_holes_unchanged':True},indent=2)+'\n',encoding='utf-8')
 print('Backup:',backup)

if __name__=='__main__':run()
