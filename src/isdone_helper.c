/* Diagnostic host for the package's own ISDone.dll; no installer UI. */
typedef unsigned long DWORD;
typedef void *HANDLE;
__declspec(dllimport) HANDLE __stdcall LoadLibraryA(const char*);
__declspec(dllimport) void *__stdcall GetProcAddress(HANDLE,const char*);
__declspec(dllimport) DWORD __stdcall GetLastError(void);
__declspec(dllimport) void __stdcall ExitProcess(unsigned int);
__declspec(dllimport) HANDLE __stdcall CreateWindowExA(DWORD,const char*,const char*,DWORD,int,int,int,int,HANDLE,HANDLE,HANDLE,void*);
__declspec(dllimport) int __cdecl __getmainargs(int*,char***,char***,int,void*);
__declspec(dllimport) int __cdecl printf(const char*,...);
__declspec(dllimport) int __cdecl fflush(void*);
__declspec(dllimport) unsigned int __cdecl strlen(const char*);
__declspec(dllimport) void *__cdecl malloc(unsigned int);
__declspec(dllimport) void *__cdecl memcpy(void*,const void*,unsigned int);
int _fltused;
static char *ansi(const char *s) {
 unsigned n=strlen(s); int *p=(int*)malloc(n+9); p[0]=-1; p[1]=n;
 memcpy(p+2,s,n+1); return (char*)(p+2);
}
static unsigned __stdcall progress(int all,int current,const char *file,const char*a,const char*b,const char*c) {
 static int last_bucket=-1;
 int bucket=all/10;
 if(bucket!=last_bucket) {
  if(all<0) all=0;
  if(all>1000) all=1000;
  printf("[ISDone] progresso=%d.%d%% arquivo=%s\n",all/10,all%10,file?file:"");
  fflush(0);last_bucket=bucket;
 }
 return 0;
}
/* Delphi method callback: EAX=context, EDX=overall, ECX=current;
   four strings are passed left-to-right on the stack. */
__declspec(naked) static void progress_thunk(void) {
 __asm {
  push ebp
  mov ebp, esp
  push dword ptr [ebp+8]
  push dword ptr [ebp+12]
  push dword ptr [ebp+16]
  push dword ptr [ebp+20]
  push ecx
  push edx
  call progress
  pop ebp
  ret 16
 }
}
typedef unsigned char (__stdcall *init_fn)(char*,unsigned,unsigned,unsigned,unsigned,HANDLE,int,void*,void*);
typedef unsigned char (__stdcall *arc_fn)(unsigned,double,char*,char*,char*,unsigned char,char*,char*,char*,unsigned char);
typedef unsigned char (__stdcall *stop_fn)(void);
void mainCRTStartup(void) {
 int argc=0, startup=0; char **argv=0,**env=0;
 __getmainargs(&argc,&argv,&env,0,&startup);
 if(argc!=6){printf("usage: isdone-helper ISDone.dll archive output arc.ini scratch\n");ExitProcess(2);}
 HANDLE dll=LoadLibraryA(argv[1]);
 init_fn init=(init_fn)GetProcAddress(dll,"ISDoneInit");
 arc_fn arc=(arc_fn)GetProcAddress(dll,"ISArcExtract");
 stop_fn stop=(stop_fn)GetProcAddress(dll,"ISDoneStop");
 if(!dll||!init||!arc||!stop){printf("[ISDone] load error=%lu\n",GetLastError());ExitProcess(3);}
 HANDLE window=CreateWindowExA(0,"STATIC","DODI codec host",0,0,0,0,0,0,0,0,0);
 printf("[ISDone] init\n");fflush(0);
 if(!init(ansi(""),5555,0,0,0,window,512,progress_thunk,0)){printf("[ISDone] init failed\n");ExitProcess(4);}
 printf("[ISDone] extract\n");fflush(0);
 unsigned char ok=arc(0,100.0,ansi(argv[2]),ansi(argv[3]),ansi(""),0,ansi(""),ansi(argv[4]),ansi(argv[5]),0);
 printf("[ISDone] result=%u\n",ok);fflush(0);stop();ExitProcess(ok?0:5);
}
