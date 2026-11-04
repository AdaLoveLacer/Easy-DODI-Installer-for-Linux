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
with tarfile.open(fileobj=io.BytesIO(payload),mode='r:gz') as outer:
 outer_bytes=sum(member.size for member in outer.getmembers() if member.isfile())
 wine_member=outer.extractfile('wine.tar.xz')
 with tarfile.open(fileobj=wine_member,mode='r:xz') as wine:
  wine_bytes=sum(member.size for member in wine.getmembers() if member.isfile())
minimum_free_bytes=outer_bytes+wine_bytes+512*1024**2
header='''#!/usr/bin/env python3
import os,sys,tarfile,io,fcntl,tempfile,shutil,platform,subprocess
from pathlib import Path
self=Path(sys.argv[1]).resolve()
if not sys.platform.startswith('linux'):
 sys.exit('Este standalone requer Linux; sistema encontrado: '+sys.platform)
if sys.version_info < (3,11):
 sys.exit('Python 3.11 ou mais recente é necessário; versão encontrada: '+sys.version.split()[0])
if platform.machine().lower() not in ('x86_64','amd64'):
 sys.exit('Este standalone requer Linux x86-64; arquitetura encontrada: '+platform.machine())
base=Path('/mnt/SSD/Tools/dodi-cli')
ssd=Path('/mnt/SSD')
if not ssd.is_mount():
 sys.exit('Monte o SSD de dados em /mnt/SSD para preparar o runtime.')
if os.statvfs(ssd).f_flag & os.ST_NOEXEC:
 sys.exit('O SSD em /mnt/SSD está montado com noexec; o runtime precisa executar ferramentas.')
minimum_free_bytes=MINIMUM_FREE_BYTES
base.mkdir(parents=True,exist_ok=True)
(base/'NAO_APAGAR.txt').write_text('Runtime do instalador DODI CLI. Necessário para executar o arquivo standalone.\\n')
runtime=base/'TAG'
with (base/'runtime.lock').open('w') as lock:
 fcntl.flock(lock,fcntl.LOCK_EX)
 if not (runtime/'ready').exists():
  free_bytes=shutil.disk_usage(ssd).free
  if free_bytes < minimum_free_bytes:
   sys.exit('Espaço insuficiente em /mnt/SSD para preparar o runtime: são necessários pelo menos '+str(minimum_free_bytes)+' bytes; disponíveis: '+str(free_bytes)+'.')
  print('Preparando os componentes do DODI CLI no SSD...',flush=True)
  stage=Path(tempfile.mkdtemp(prefix='.prepare-',dir=base))
  try:
   data=self.read_bytes().split(b'\\n__DODI_PAYLOAD__\\n',1)[1]
   with tarfile.open(fileobj=io.BytesIO(data)) as t: t.extractall(stage,filter='data')
   native_env=os.environ.copy()
   native_env['LD_LIBRARY_PATH']=str(stage/'libexec')+':'+native_env.get('LD_LIBRARY_PATH','')
   checks=[([str(stage/'libexec/innoextract'),'--version'],0),([str(stage/'libexec/unarc')],2)]
   for command,expected_status in checks:
    result=subprocess.run(command,text=True,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,env=native_env,check=False)
    if result.returncode != expected_status:
     detail=result.stdout.strip()[-1600:]
     sys.exit('As bibliotecas do sistema não são compatíveis com as ferramentas incluídas. Comando: '+command[0]+'; código: '+str(result.returncode)+'\\n'+detail)
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
shell="""#!/bin/sh
if ! command -v python3 >/dev/null 2>&1; then
    printf '%s\\n' 'Python 3.11 ou mais recente é necessário (comando python3 não encontrado).' >&2
    exit 127
fi
case "$(uname -m)" in
    x86_64|amd64) ;;
    *) printf 'Este standalone requer Linux x86-64; arquitetura encontrada: %s\\n' "$(uname -m)" >&2; exit 1 ;;
esac
exec python3 -c '"""+header.replace("'","'\\''")+"' \"$0\" \"$@\"\n"
shell=shell.replace('MINIMUM_FREE_BYTES',str(minimum_free_bytes))
# Python -c shifts argv: use argv[1] as the artifact and argv[2:] as arguments.
shell=shell.replace('self=Path(__file__).resolve()','self=Path(sys.argv[1]).resolve()').replace('*sys.argv[1:]','*sys.argv[2:]')
out=root/'dist/dodi';out.parent.mkdir(exist_ok=True)
out.write_bytes(shell.encode()+b'\n__DODI_PAYLOAD__\n'+payload);out.chmod(0o755)
print(out, out.stat().st_size)
