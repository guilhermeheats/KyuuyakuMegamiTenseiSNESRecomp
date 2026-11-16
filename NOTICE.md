# Notices and licensing

## Project code

The original code and documentation specific to **KyuuyakuTen** are licensed
under the **PolyForm Noncommercial License 1.0.0**; the full text is in
[`LICENSE`](LICENSE). Project-specific additions are Copyright © 2026
Guilherme Teixeira, except scaffolded framework code and third-party
components, which retain their upstream copyrights and terms.

This is a **source-available** license, not an OSI open-source license. It
permits noncommercial use, modification and distribution under its terms.
Commercial use requires separate permission from the relevant rights holders.
The project is free to download, build and play; no payment is required.

## SNESRecomp

This project is built on [SNESRecomp](https://github.com/RetroPortingToolKit/snesrecomp),
which is licensed under the **PolyForm Noncommercial License 1.0.0**,
Copyright (c) 2026 Matthew Stanley.

- Additional permissions (donations, advertising and free access):
  [`snesrecomp/PERMISSIONS.md`](snesrecomp/PERMISSIONS.md)
- Third-party notices and license texts:
  [`snesrecomp/THIRD_PARTY_ATTRIBUTION.md`](snesrecomp/THIRD_PARTY_ATTRIBUTION.md)
- A repository-root mirror of the third-party notices is kept in
  [`THIRD_PARTY_ATTRIBUTION.md`](THIRD_PARTY_ATTRIBUTION.md) so a source
  snapshot without submodule contents still carries the required notices.

SNESRecomp's runner includes MIT-licensed material from snesrev (zelda3/smw)
and LakeSnes, plus ISC-licensed ares-derived coprocessor code. The full notices
are in the files above and are also present in the submodule.

## Recomp UI

The launcher uses [recomp-ui](https://github.com/mstan/recomp-ui), licensed
under the **MIT License**, Copyright (c) 2026 Matthew Stanley. See
[`recomp-ui/LICENSE`](recomp-ui/LICENSE).

## Game data

**Kyuuyaku Megami Tensei** and all related names, characters, graphics, audio,
text and other assets are trademarks or copyrights of their respective owners,
including Atlus and Namco.

No ROM, BIOS, game assets, extracted data, save files or recompiled C is
distributed in this repository. Each user must supply their own legally
obtained cartridge dump. The build verifies the supported revision by CRC32
and SHA-256 before generating code.

## No affiliation

This is an unofficial, noncommercial preservation and reverse-engineering
project. It is not affiliated with, endorsed by, or sponsored by Atlus, Namco,
Nintendo, Opera House, or any of their subsidiaries.
