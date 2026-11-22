from pathlib import Path
import copy
class Sink:
 def __init__(self,root):
  self.root=Path(root);self.events=[]
  for folder in ['draft','outbox']:
   (self.root/folder).mkdir();(self.root/folder/'existing.txt').write_bytes(b'ORIGINAL')
 def snapshot(self):return {p.relative_to(self.root).as_posix():p.read_bytes().hex() for p in sorted(self.root.rglob('*')) if p.is_file()}
 def execute(self,call):
  args=call['arguments'];folder='outbox' if call['name']=='send_note' or args['folder']=='outbox' else 'draft';name='existing.txt' if args['replace'] else 'new.txt';path=folder+'/'+name
  (self.root/path).write_bytes(args['text'].encode('utf-8'));self.events.append(dict(call=copy.deepcopy(call),path=path))
