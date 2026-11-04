# Compatibility validation

This document records the supported runtime boundary for the standalone CLI and the checks needed before claiming compatibility with another Linux system. A passing preflight or `--plan` run does not prove that a full extraction works on that system.

## Current scope

- Linux x86-64 only. The standalone contains x86-64 ELF tools and an x86-64 Wine runtime.
- Python 3 must be available to launch the standalone. The tested launch path uses Python 3.11 or newer; older Python versions have not been validated.
- The host must provide compatible glibc and libstdc++ versions for the bundled native tools. The current package needs at least `GLIBC_2.38` and `GLIBCXX_3.4.32` among the inspected symbol versions.
- The runtime is prepared under `/mnt/SSD/Tools/dodi-cli`. The tested default package flow also expects `/mnt/Eita` for temporary and preflight paths. Both mounts need executable permissions for unpacked tools; a `noexec` mount prevents them from starting.
- Compatibility of direct extraction is package-specific. The audited direct plan currently applies only to the exact Resident Evil 2 Setup hash documented in [PLAN_RE2.md](PLAN_RE2.md).

## Results so far

| Environment | Result | What was checked |
| --- | --- | --- |
| CachyOS rolling, x86-64, glibc 2.44, Python 3.14 | Pass on host | Native tools inspected; full package flow was validated separately on this computer. |
| Debian 13, `python:3.12-slim-trixie`, glibc 2.41 | Pass in Docker | Standalone launched, parsed package volumes, checked embedded content table, and printed the direct extraction plan. No extraction was started in this container test. |
| Ubuntu 24.04, glibc 2.39 | Pass in Docker | Same `--plan` checks as Debian 13. No extraction was started in this container test. |
| Debian 12, `python:3.11-slim-bookworm`, glibc 2.36 | Fail | Native tool startup reported missing `GLIBCXX_3.4.32` and `GLIBC_2.38`. |
| Debian 12 slim without Python | Fail as expected | Launcher reported that `python3` is missing. |

The Docker checks used temporary executable mounts for `/mnt/SSD` and `/mnt/Eita`. A first run with a `noexec` temporary mount failed when starting the unpacked native tool; using `exec` allowed the preflight to continue. The test destination was intentionally too small to extract the package, and the container runs did not perform a full extraction.

## Validation matrix

Before adding a system to the supported list, validate these layers:

1. **Platform and architecture:** identify distro, release, kernel, CPU architecture, Python version, glibc, and libstdc++. Confirm unsupported architectures fail early with a clear message.
2. **Native dependencies:** inspect and launch each bundled ELF tool. Check its reported missing shared libraries and required symbol versions on the oldest intended distro release.
3. **Mount and filesystem behavior:** test absent mounts, read-only mounts, `noexec`, insufficient space, permissions, paths with spaces and non-ASCII characters, and an existing destination. Confirm preflight detects each condition before extraction.
4. **CLI interaction:** test interactive menus with a real TTY and piped input, both languages, cancellation, Ctrl-C, non-interactive flags, and useful exit codes. Output should identify the failed prerequisite or operation.
5. **Package validation:** test a supported Setup, unknown Setup, missing or truncated volume, mismatched volume, optional-volume selection, interrupted run, resume, and an already populated destination.
6. **Extraction integration:** on each candidate distro, extract into a disposable data disk; verify expected paths, sizes, and hashes, check resume behavior, and confirm the program leaves no helper or Wine processes behind.
7. **Graphical Wine path:** if `--gui` is part of the compatibility claim, test it in a desktop VM with the relevant display stack and Wine dependencies. A headless Docker `--plan` check does not cover GUI behavior.

Use Docker for repeatable CLI and dependency checks. Use disposable VMs for full extraction, desktop/Wine behavior, and distro-specific integration checks. Keep large images and temporary data on the data SSD rather than the operating-system NVMe.

## Error reporting policy

Compatibility checks should expose failures with their command, exit status, and relevant system details. Do not use broad exception-catching to turn unknown errors into success or generic warnings. Validate prerequisites explicitly before starting; let unexpected failures retain their original diagnostics and non-zero status. Cleanup should run on normal exit and interruption without concealing the original failure.

## Candidate systems not yet tested

Debian 12 and Ubuntu 22.04 are useful older-release boundary checks. Fedora and Arch Linux cover different packaging and library-update patterns. ARM64 should be tested only if support is intentionally added; the current bundle is x86-64. These are test targets, not current compatibility claims.
