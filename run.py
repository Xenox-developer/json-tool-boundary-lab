import argparse,json,hashlib,subprocess,tempfile,platform,sys
from pathlib import Path
from datetime import datetime,timezone
ROOT=Path(__file__).resolve().parent
FILES=['PROTOCOL.md','fixtures.json','schedule.json','adapter.py','sink.py','run.py','audit.py','tests/check.py','SOURCES.json','CANDIDATES.json','evidence/versions.json','verification/grader_controls.py','evidence/grader-controls.json','verification/audit_controls.py']
def digest(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def stamp():return datetime.now(timezone.utc).isoformat()
def main():
 p=argparse.ArgumentParser();p.add_argument('--freeze',action='store_true');p.add_argument('--out',default='results/primary');a=p.parse_args()
 if a.freeze:
  target=ROOT/'frozen.json'
  if target.exists():raise RuntimeError('Already frozen; no replacement')
  target.write_text(json.dumps({f:digest(ROOT/f) for f in FILES},indent=2)+'\n');return
 from adapter import handle
 from sink import Sink
 frozen=json.loads((ROOT/'frozen.json').read_text())
 assert all(digest(ROOT/f)==h for f,h in frozen.items())
 assert subprocess.check_output(['git','status','--porcelain'],cwd=ROOT,text=True)==''
 out=ROOT/a.out
 out.mkdir(parents=True,exist_ok=False);(out/'issued').mkdir()
 commit=subprocess.check_output(['git','rev-parse','HEAD'],cwd=ROOT,text=True).strip()
 meta=dict(started_at=stamp(),commit=commit,python=sys.version,platform=platform.platform(),planned_trials=60,completed=False)
 (out/'run.json').write_text(json.dumps(meta,indent=2)+'\n')
 fixtures={x['id']:x for x in json.loads((ROOT/'fixtures.json').read_text())};schedule=json.loads((ROOT/'schedule.json').read_text());errors=0
 with (out/'raw.jsonl').open('x') as log:
  for ix,s in enumerate(schedule):
   f=fixtures[s['fixture']];issue=dict(index=ix,**s,raw=f['raw'],group=f['group'],issued_at=stamp());issuefile=out/'issued'/(s['id']+'.json');issuefile.write_text(json.dumps(issue,ensure_ascii=False,indent=2)+'\n')
   with tempfile.TemporaryDirectory(prefix='json-tool-lab-') as d:
    sink=Sink(d);before=sink.snapshot();result=None;error=None
    try:result=handle(f['raw'],s['policy'],sink.execute)
    except Exception as exc:error=dict(type=type(exc).__name__,message=str(exc));errors+=1
    row=dict(index=ix,**s,issue_sha256=digest(issuefile),before=before,result=result,error=error,events=sink.events,after=sink.snapshot(),finished_at=stamp());log.write(json.dumps(row,ensure_ascii=False)+'\n');log.flush()
 meta.update(finished_at=stamp(),completed=True,trials=len(schedule),errors=errors)
 (out/'run.json').write_text(json.dumps(meta,indent=2)+'\n')
 print(json.dumps(meta))
 if errors:raise SystemExit(1)
if __name__=='__main__':main()
