#!/usr/bin/env python3
from pathlib import Path
import tarfile,io,hashlib,subprocess,re
root=Path(__file__).resolve().parents[1]
buf=io.BytesIO()
with tarfile.open(fileobj=buf,mode='w:gz') as t:
 for name in ['dodi','LICENSE','THIRD_PARTY_NOTICES.md','libexec/innoextract','libexec/unarc','libexec/isdone-helper.exe']:
  t.add(root/name,arcname=name)
 libs=set()
 for binary in ['innoextract','unarc']:
  out=subprocess.run(['ldd',str(root/'libexec'/binary)],capture_output=True,text=True).stdout
  for path in re.findall(r'=> (/\S+)',out):
   if any(x in Path(path).name for x in ['boost','lzma','zstd','bz2']): libs.add(path)
 for path in libs: t.add(Path(path).resolve(),arcname='libexec/'+Path(path).name)
 t.add('/mnt/Eita/Tools/fitgirl-wine/wine-11.14-fitgirl-amd64.tar.xz',arcname='wine.tar.xz')
payload=buf.getvalue();tag=hashlib.sha256(payload).hexdigest()[:16]
header='''#!/usr/bin/env python3
import os,sys,tarfile,io,fcntl,tempfile,shutil
from pathlib import Path
self=Path(__file__).resolve()
base=Path('/mnt/SSD/Tools/dodi-cli')
if not Path('/mnt/SSD').is_mount():
 sys.exit('Monte o SSD de dados em /mnt/SSD para preparar o runtime.')
base.mkdir(parents=True,exist_ok=True)
(base/'NAO_APAGAR.txt').write_text('Runtime do instalador DODI CLI. Necessário para executar o arquivo standalone.\\n')
runtime=base/'TAG'
with (base/'runtime.lock').open('w') as lock:
 fcntl.flock(lock,fcntl.LOCK_EX)
 if not (runtime/'ready').exists():
  print('Preparando os componentes do DODI CLI no SSD...',flush=True)
  stage=Path(tempfile.mkdtemp(prefix='.prepare-',dir=base))
  try:
   data=self.read_bytes().split(b'\\n__DODI_PAYLOAD__\\n',1)[1]
   with tarfile.open(fileobj=io.BytesIO(data)) as t: t.extractall(stage,filter='data')
   with tarfile.open(stage/'wine.tar.xz') as t: t.extractall(stage/'libexec',filter='data')
   (stage/'wine.tar.xz').unlink()
   (stage/'ready').touch()
   stage.rename(runtime)
  except BaseException:
   shutil.rmtree(stage)
   raise
os.environ['DODI_LAUNCHER_DIR']=str(self.parent)
os.environ['LD_LIBRARY_PATH']=str(runtime/'libexec')+':'+os.environ.get('LD_LIBRARY_PATH','')
os.execv(sys.executable,[sys.executable,'-u',str(runtime/'dodi'),*sys.argv[1:]])
'''.replace('TAG',tag)
# Shell skips the binary payload; Python receives only the launcher source.
shell="#!/bin/sh\nexec python3 -c '"+header.replace("'","'\\''")+"' \"$0\" \"$@\"\n"
# Python -c shifts argv: use argv[1] as the artifact and argv[2:] as arguments.
shell=shell.replace('self=Path(__file__).resolve()','self=Path(sys.argv[1]).resolve()').replace('*sys.argv[1:]','*sys.argv[2:]')
out=root/'dist/dodi';out.parent.mkdir(exist_ok=True)
out.write_bytes(shell.encode()+b'\n__DODI_PAYLOAD__\n'+payload);out.chmod(0o755)
print(out, out.stat().st_size)
