# Compatibility validation

This document records the supported runtime boundary for the standalone CLI and the checks needed before claiming compatibility with another Linux system. A passing preflight or `--plan` run does not prove that a full extraction works on that system.

## Current scope

- Linux x86-64 only. The standalone contains x86-64 ELF tools and an x86-64 Wine runtime.
- Python 3 must be available to launch the standalone. The tested launch path uses Python 3.11 or newer; older Python versions have not been validated.
- The host must provide compatible glibc and libstdc++ versions for the bundled native tools. The current package needs at least `GLIBC_2.38` and `GLIBCXX_3.4.32` among the inspected symbol versions.
- By default, the runtime is prepared under `/mnt/SSD/Tools/dodi-cli`. Set `DODI_RUNTIME_ROOT` and, if needed, `DODI_RUNTIME_MOUNT` to use another mounted data disk. `DODI_DATA_MOUNTS` controls the mounted roots allowed for output; the runtime disk is included by default. `DODI_PREFLIGHT_TMP` can select the analysis temporary directory. Data mounts need executable permissions for unpacked tools; a `noexec` mount prevents them from starting.
- Compatibility of direct extraction is package-specific. The audited direct plan currently applies only to the exact Resident Evil 2 Setup hash documented in [PLAN_RE2.md](PLAN_RE2.md).

## Results so far

| Environment | Result | What was checked |
| --- | --- | --- |
| CachyOS rolling, x86-64, glibc 2.44, Python 3.14 | Pass on host | Native tools inspected; full package flow was validated separately on this computer. |
| Linux Mint 22.3 Cinnamon live VM, 6 vCPUs, 4 GiB RAM | Full extraction passed with a temporary mount adapter; rebuilt standalone passed fresh-launch smoke check | ISDone completed all three volumes; final output had 87 files and 26,087,258,415 bytes. The test ISO predated the current standalone bundle, so the VM copy also received the five Boost shared libraries from the current artifact. The rebuilt standalone then bootstrapped its runtime on the separate data disk, displayed the language menu, validated the embedded content table, and printed the `--plan` output without starting another extraction. |
| Debian 13, `python:3.12-slim-trixie`, glibc 2.41 | Pass in Docker | Standalone launched, parsed package volumes, checked embedded content table, and printed the direct extraction plan. No extraction was started in this container test. |
| Ubuntu 24.04, glibc 2.39 | Pass in Docker | Same `--plan` checks as Debian 13. No extraction was started in this container test. |
| Debian 12, `python:3.11-slim-bookworm`, glibc 2.36 | Fail | Initial probe reported missing `GLIBCXX_3.4.32` and `GLIBC_2.38`; the current launcher now detects and reports these before unpacking Wine. |
| Debian 12 slim without Python | Fail as expected | Launcher reported that `python3` is missing. |
| Debian 12, current standalone launcher | Rejected clearly | Native preflight identified missing `GLIBCXX_3.4.32` and `GLIBC_2.38` before unpacking the Wine runtime. |
| Python 3.9 | Rejected clearly | Launcher requires Python 3.11 or newer and reports the detected version. |
| Python missing | Rejected clearly | Shell launcher reports the missing `python3` command. |
| Simulated ARM64 architecture | Rejected clearly | Shell launcher reports that the bundle requires x86-64. |
| Executable SSD mount missing (`noexec`) | Rejected clearly | Launcher stops before preparing the runtime. |
| SSD space below the calculated runtime requirement | Rejected clearly | Launcher reports required and available byte counts before preparing the runtime. |
| Cached runtime with less than the initial preparation space | Pass | A second launch succeeded after the runtime was prepared and free space fell below the first-run threshold. |

The Docker checks used temporary executable mounts for `/mnt/SSD` and `/mnt/Eita`. A first run with a `noexec` temporary mount failed when starting the unpacked native tool; the standalone now detects this before preparing its runtime. The test destination was intentionally too small to extract the package, and the container runs did not perform a full extraction. The launcher computes the runtime space requirement from the bundled archives and adds a 512 MiB margin.

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
