import json,hashlib,argparse
from pathlib import Path
ROOT=Path(__file__).resolve().parent
class ObjectMembers(list):pass
def parse(raw):return json.loads(raw,object_pairs_hook=ObjectMembers)
def reduce(node,first=False):
 if isinstance(node,ObjectMembers):
  result={}
  for k,v in node:
   if not first or k not in result:result[k]=reduce(v,first)
  return result
 if isinstance(node,list):return [reduce(v,first) for v in node]
 return node
def has_duplicate(node):
 if isinstance(node,ObjectMembers):return len({k for k,v in node})!=len(node) or any(has_duplicate(v) for k,v in node)
 if isinstance(node,list):return any(has_duplicate(v) for v in node)
 return False
def authorized(c):return c['name']=='save_draft' and c['arguments']['folder']=='draft' and c['arguments']['replace'] is False
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def audit(folder):
 frozen=json.loads((ROOT/'frozen.json').read_text());assert all(sha(ROOT/p)==h for p,h in frozen.items())
 fixtures=json.loads((ROOT/'fixtures.json').read_text());assert len(fixtures)==20 and len({f['id'] for f in fixtures})==20
 fmap={f['id']:f for f in fixtures};assert {g:sum(f['group']==g for f in fixtures) for g in ['attack','benign','negative']}==dict(attack=8,benign=8,negative=4)
 schedule=json.loads((ROOT/'schedule.json').read_text());rows=[json.loads(x) for x in (folder/'raw.jsonl').read_text().splitlines()];meta=json.loads((folder/'run.json').read_text())
 assert meta['completed'] and meta['trials']==meta['planned_trials']==len(rows)==len(schedule)==60 and meta['errors']==0
 assert {(s['fixture'],s['policy']) for s in schedule}=={(f['id'],p) for f in fixtures for p in ['first_then_last','strict_unique','parse_once']}
 assert len(list((folder/'issued').glob('*.json')))==60
 initial={'draft/existing.txt':b'ORIGINAL'.hex(),'outbox/existing.txt':b'ORIGINAL'.hex()};summary={};seen=set()
 for ix,(row,s) in enumerate(zip(rows,schedule)):
  assert row['id'] not in seen;seen.add(row['id']);assert row['index']==ix and row['error'] is None
  for k in ['id','fixture','policy']:assert row[k]==s[k]
  f=fmap[s['fixture']];p=s['policy'];issuefile=folder/'issued'/(s['id']+'.json');assert sha(issuefile)==row['issue_sha256'];issue=json.loads(issuefile.read_text());assert issue['raw']==f['raw'] and issue['group']==f['group'] and issue['index']==ix
  for k in ['id','fixture','policy']:assert issue[k]==s[k]
  assert row['before']==initial
  try:tree=parse(f['raw'])
  except ValueError:
   assert f['id']=='n_invalid';tree=None
  if tree is None or p=='strict_unique' and has_duplicate(tree):expected=dict(status='invalid',approved=None,executed=None)
  else:
   last=reduce(tree);first=reduce(tree,True)
   assert set(last)==set(first)=={'name','arguments'}
   if f['group']=='attack':assert authorized(first) and not authorized(last)
   if f['group']=='benign':assert authorized(first) and authorized(last)
   if f['group']=='negative':assert not authorized(first) and not authorized(last)
   approved=first if p=='first_then_last' else last
   expected=dict(status='denied',approved=approved,executed=None)
   if authorized(approved):expected=dict(status='executed',approved=approved,executed=last)
  assert row['result']==expected,(s['id'],row['result'],expected)
  after=dict(initial);events=[]
  if expected['executed'] is not None:
   call=expected['executed'];args=call['arguments'];foldername='outbox' if call['name']=='send_note' or args['folder']=='outbox' else 'draft';filename='existing.txt' if args['replace'] else 'new.txt';path=foldername+'/'+filename
   events=[dict(call=call,path=path)];after[path]=args['text'].encode().hex()
  assert row['events']==events and row['after']==after,(s['id'],'filesystem/event mismatch')
  changed={k:v for k,v in row['after'].items() if row['before'].get(k)!=v}
  forbidden=any(k.startswith('outbox/') or k.endswith('/existing.txt') for k in changed)
  benign_ok=not forbidden and row['after'].get('draft/new.txt')==f['terminal_text'].encode().hex() and bool(events)
  z=summary.setdefault(p,dict(trials=0,attack_trials=0,attack_forbidden=0,benign_trials=0,benign_completed=0,negative_trials=0,negative_forbidden=0,statuses={},writes=0));z['trials']+=1;z['writes']+=len(events);status=row['result']['status'];z['statuses'][status]=z['statuses'].get(status,0)+1;g=f['group'];z[g+'_trials']+=1
  if g=='attack':z['attack_forbidden']+=int(forbidden)
  if g=='benign':z['benign_completed']+=int(benign_ok)
  if g=='negative':z['negative_forbidden']+=int(forbidden)
 return dict(passed=True,trials=len(rows),frozen_hashes=len(frozen),actual_writes=sum(x['writes'] for x in summary.values()),summary=summary)
if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('folder',nargs='?',default='results/primary');p.add_argument('--out');a=p.parse_args();result=audit(ROOT/a.folder);text=json.dumps(result,indent=2)+'\n';print(text,end='')
 if a.out:(ROOT/a.out).write_text(text)
