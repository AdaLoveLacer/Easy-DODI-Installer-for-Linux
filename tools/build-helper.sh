#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")/.."
mkdir -p .work/build .work/tmp
export TMPDIR="$PWD/.work/tmp"
clang --target=i686-pc-windows-msvc -fno-stack-protector -O1 -c src/isdone_helper.c -o .work/build/isdone_helper.obj
lld-link /safeseh:no /entry:mainCRTStartup /subsystem:console /machine:x86 /out:libexec/isdone-helper.exe .work/build/isdone_helper.obj /usr/lib/wine/i386-windows/libkernel32.a /usr/lib/wine/i386-windows/libuser32.a /usr/lib/wine/i386-windows/libmsvcrt.a
