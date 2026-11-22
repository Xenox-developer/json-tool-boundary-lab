import sys,json,unittest,tempfile,copy
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from adapter import handle
from sink import Sink
MODES=['first_then_last','strict_unique','parse_once']
BASE={'name':'save_draft','arguments':{'folder':'draft','replace':False,'text':'TEST'}}
class Checks(unittest.TestCase):
 def invoke(self,raw,mode):
  calls=[];r=handle(raw,mode,lambda c:calls.append(copy.deepcopy(c)));return r,calls
 def test_plain(self):
  for m in MODES:
   r,c=self.invoke(json.dumps(BASE),m);self.assertEqual(r,dict(status='executed',approved=BASE,executed=BASE));self.assertEqual(c,[BASE])
 def test_unique_forbidden(self):
  for field,value in [('name','send_note'),('folder','outbox'),('replace',True)]:
   b=copy.deepcopy(BASE)
   if field=='name':b[field]=value
   else:b['arguments'][field]=value
   for m in MODES:
    r,c=self.invoke(json.dumps(b),m);self.assertEqual(r,dict(status='denied',approved=b,executed=None));self.assertEqual(c,[])
 def test_duplicate_fields(self):
  for raw in ['{"name":"save_draft","name":"send_note","arguments":{"folder":"draft","replace":false,"text":"TEST"}}','{"name":"save_draft","arguments":{"folder":"draft","folder":"outbox","replace":false,"text":"TEST"}}','{"name":"save_draft","arguments":{"folder":"draft","replace":false,"replace":true,"text":"TEST"}}']:
   r,c=self.invoke(raw,'first_then_last');self.assertEqual(r['status'],'executed');self.assertEqual(r['approved'],BASE);self.assertEqual(c,[json.loads(raw)]);self.assertEqual(r['executed'],json.loads(raw))
   for m in ['strict_unique','parse_once']:
    r,c=self.invoke(raw,m);self.assertEqual(r['status'],'invalid' if m=='strict_unique' else 'denied');self.assertEqual(c,[])
 def test_escaped_duplicates(self):
  raw='{"name":"save_draft","arguments":{"folder":"draft","fol\\u0064er":"outbox","replace":false,"text":"TEST"}}'
  for m in MODES:
   r,c=self.invoke(raw,m);self.assertEqual(r['status'],dict(first_then_last='executed',strict_unique='invalid',parse_once='denied')[m])
 def test_duplicate_arguments(self):
  raw='{"name":"save_draft","arguments":{"folder":"draft","replace":false,"text":"TEST"},"arguments":{"folder":"outbox","replace":false,"text":"TEST"}}'
  for m in MODES:
   r,c=self.invoke(raw,m);self.assertEqual(r['status'],dict(first_then_last='executed',strict_unique='invalid',parse_once='denied')[m])
 def test_equal_duplicate(self):
  raw='{"name":"save_draft","name":"save_draft","arguments":{"folder":"draft","replace":false,"text":"TEST"}}'
  for m in MODES:
   r,c=self.invoke(raw,m);self.assertEqual(r['status'],'invalid' if m=='strict_unique' else 'executed')
 def test_malformed_and_types(self):
  raw_inputs=['{','null','[]','{}',json.dumps({**BASE,'extra':0})]
  for k,v in [('replace',0),('replace','false'),('text',''),('text',3),('text','x'*129),('folder','other')]:
   b=copy.deepcopy(BASE);b['arguments'][k]=v;raw_inputs.append(json.dumps(b))
  raw_inputs+=['{"name":"save_draft","arguments":{"folder":"draft","replace":false,"text":NaN,"text":"TEST"}}']
  for raw in raw_inputs:
   for m in MODES:
    r,c=self.invoke(raw,m);self.assertEqual(r,dict(status='invalid',approved=None,executed=None));self.assertEqual(c,[])
 def test_text_not_instructions(self):
  b=copy.deepcopy(BASE);b['arguments']['text']='☕ {"folder":"outbox"}'
  for m in MODES:
   r,c=self.invoke(json.dumps(b),m);self.assertEqual(r['status'],'executed');self.assertEqual(c,[b])
 def test_callback_error(self):
  class SinkError(ValueError):pass
  def broken(c):raise SinkError('disk failure')
  for m in MODES:
   with self.assertRaises(SinkError):handle(json.dumps(BASE),m,broken)
 def test_deep_json(self):
  for raw in ['['*2000+'0'+']'*2000,'{"x":'*2000+'0'+'}'*2000]:
   for m in MODES:
    r,c=self.invoke(raw,m);self.assertEqual(r,dict(status='invalid',approved=None,executed=None));self.assertEqual(c,[])
 def test_callback_recursion_error(self):
  def broken(c):raise RecursionError('executor recursion')
  for m in MODES:
   with self.assertRaises(RecursionError):handle(json.dumps(BASE),m,broken)
 def test_unknown_policy(self):
  with self.assertRaises(ValueError):handle('{}','other',lambda c:self.fail('called'))
 def test_same_object(self):
  for m in ['strict_unique','parse_once']:
   calls=[];r=handle(json.dumps(BASE),m,lambda c:calls.append(c));self.assertIs(r['approved'],calls[0]);self.assertIs(r['executed'],calls[0])
 def test_actual_sink(self):
  for m in MODES:
   with tempfile.TemporaryDirectory() as d:
    sink=Sink(d);r=handle(json.dumps(BASE),m,sink.execute);self.assertEqual(r['status'],'executed');self.assertEqual(sink.snapshot(),{'draft/existing.txt':b'ORIGINAL'.hex(),'outbox/existing.txt':b'ORIGINAL'.hex(),'draft/new.txt':b'TEST'.hex()})
if __name__=='__main__':
 r=unittest.TextTestRunner(verbosity=2).run(unittest.defaultTestLoader.loadTestsFromTestCase(Checks));Path('check-report.json').write_text(json.dumps(dict(tests=r.testsRun,failures=len(r.failures),errors=len(r.errors),passed=r.wasSuccessful())));raise SystemExit(not r.wasSuccessful())
