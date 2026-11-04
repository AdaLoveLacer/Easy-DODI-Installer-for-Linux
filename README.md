# Easy-DODI-Installer-for-Linux

A standalone Linux CLI for extracting local DODI repacks. The interactive menu lets you choose optional content and an installation destination.

## Quick start

Copy [`dist/dodi`](dist/dodi) into the repack folder, then run:

```sh
./dodi
```

The menu asks which language to use, then offers the package options. You can also pass the package directly:

```sh
./dodi /path/to/Setup.exe
```

The standalone includes the extraction tools and Wine runtime. On first launch, it prepares the runtime under `/mnt/SSD/Tools/dodi-cli`; keep that folder. It requires Linux x86-64, Python 3, and standard system libraries. The runtime is bundled, but the program is not a static binary.

The default CLI extracts the package's selected volumes without running the original graphical Setup. It validates extracted paths and file sizes after each volume, records progress for resuming, and publishes the final folder after validation. `--gui` opens the original Setup instead; `--scan` searches for packages only when requested.

## Compatibility

Direct extraction is currently audited for the Resident Evil 2 package used during development. Other repacks may require their own extraction plan; use `--gui` for those. The local Resident Evil 2 test validated all three volumes by path and size and matched SHA-256 hashes for all 87 extracted files against the existing installation. See [the test plan](docs/PLAN_RE2.md) and [technical references](docs/REFERENCES.md).

## Build

Run `python3 tools/build-standalone.py` to produce `dist/dodi`. The build currently expects the bundled Wine archive at `/mnt/Eita/Tools/fitgirl-wine/wine-11.14-fitgirl-amd64.tar.xz`.

The project's non-commercial license applies only to original project code. Bundled third-party components retain their own terms; see [LICENSE](LICENSE) and [third-party notices](THIRD_PARTY_NOTICES.md).

Português: [README.pt-BR.md](README.pt-BR.md).
