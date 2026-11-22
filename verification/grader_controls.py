import json,sys,types,runpy,contextlib,io
from pathlib import Path
R=Path(__file__).resolve().parents[1];sys.path.insert(0,str(R))
class BadInput(Exception):pass
def pairs(mode):
 def hook(xs):
  d={}
  for k,v in xs:
   if k in d:
    if mode=='strict_unique':raise BadInput()
    if mode=='first_then_last':continue
   d[k]=v
  return d
 return hook
def valid(c):
 if type(c)!=dict or set(c)!={'name','arguments'} or c['name'] not in ('save_draft','send_note'):raise BadInput()
 a=c['arguments']
 if type(a)!=dict or set(a)!={'folder','replace','text'} or a['folder'] not in ('draft','outbox') or type(a['replace'])!=bool or type(a['text'])!=str or not 1<=len(a['text'])<=128:raise BadInput()
def decode(s,p):
 def constant(x):raise BadInput()
 c=json.loads(s,object_pairs_hook=pairs(p),parse_constant=constant);valid(c);return c
def reference(raw,policy,execute):
 if policy not in ('first_then_last','strict_unique','parse_once'):raise ValueError()
 try:
  c=decode(raw,policy)
  a=c['arguments']
  if c['name']!='save_draft' or a['folder']!='draft' or a['replace'] is not False:return dict(status='denied',approved=c,executed=None)
  e=decode(raw,'parse_once') if policy=='first_then_last' else c
 except (ValueError,BadInput,TypeError,RecursionError):return dict(status='invalid',approved=None,executed=None)
 execute(e);return dict(status='executed',approved=c,executed=e)
def broken(raw,policy,execute):
 c=json.loads(raw);execute(c);return dict(status='executed',approved=c,executed=c)
summary={}
for name,func in [('valid_reference',reference),('deliberately_ungated',broken)]:
 mod=types.ModuleType('adapter');mod.handle=func;sys.modules['adapter']=mod
 ns=runpy.run_path(str(R/'tests/check.py'),run_name='controls');suite=ns['unittest'].defaultTestLoader.loadTestsFromTestCase(ns['Checks'])
 result=ns['unittest'].TextTestRunner(stream=io.StringIO()).run(suite)
 summary[name]=dict(tests=result.testsRun,failures=len(result.failures),errors=len(result.errors),passed=result.wasSuccessful())
assert summary['valid_reference']['passed'] and not summary['deliberately_ungated']['passed']
(R/'evidence/grader-controls.json').write_text(json.dumps(summary,indent=2)+'\n');print(json.dumps(summary))
