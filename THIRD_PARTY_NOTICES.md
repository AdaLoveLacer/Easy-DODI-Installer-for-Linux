# Third-party components

The non-commercial project license applies only to original project code. The standalone bundles the components below; each remains under its own license, including any rights those licenses grant for commercial use.

| Component | License | Source / license information |
| --- | --- | --- |
| Wine runtime | LGPL and other component-specific licenses | [Wine source](https://gitlab.winehq.org/wine/wine); the bundled local build is Wine 11.14 from `/mnt/Eita/Tools/fitgirl-wine`. Its exact patch/source provenance must accompany redistribution of that build. |
| innoextract | zlib | [Upstream project and license](https://github.com/dscharrer/innoextract) |
| FreeArc `unarc` | GPL-2.0 | [FreeArc project](https://sourceforge.net/projects/freearc/). Corresponding source for the exact bundled binary has not yet been verified. |
| Boost, LZMA, bzip2, and Zstandard shared libraries | Their respective upstream licenses | These libraries are bundled to support innoextract; see their license files and source packages before redistributing the standalone. |

The DODI package's own files and codecs are supplied by the person running the tool and are not included in this project distribution.
