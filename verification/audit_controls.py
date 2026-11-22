import sys,tempfile,shutil,json,copy
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT))
from audit import audit
source=ROOT/'results/primary';results={}
for mode in ['intact','missing_cell','changed_filesystem','changed_approved_object']:
 with tempfile.TemporaryDirectory() as d:
  target=Path(d)/'primary';shutil.copytree(source,target);rows=[json.loads(s) for s in (target/'raw.jsonl').read_text().splitlines()]
  if mode=='missing_cell':rows.pop()
  if mode=='changed_filesystem':rows[0]['after']['outbox/unrecorded.txt']='41'
  if mode=='changed_approved_object':
   row=next(r for r in rows if r['result']['approved'] is not None);row['result']['approved']['name']='tampered'
  (target/'raw.jsonl').write_text(''.join(json.dumps(r,ensure_ascii=False)+'\n' for r in rows))
  try:audit(target);accepted=True
  except AssertionError:accepted=False
  results[mode]={'accepted':accepted};assert accepted==(mode=='intact'),(mode,accepted)
print(json.dumps(results,indent=2))
