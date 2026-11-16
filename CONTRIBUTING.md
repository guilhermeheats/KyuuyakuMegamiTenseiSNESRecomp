# Contributing

Thanks for helping with the Kyuuyaku Megami Tensei recompilation.

## Ground rules

- You must own a legally obtained copy of the Japanese game.
- Never commit the ROM, extracted assets, save files, save states, frame dumps
  or generated C. `src/gen/` is intentionally ignored.
- Use the supported revision only: CRC32 `c8d286c9`,
  SHA-1 `827f6e0534e2317e3348ce76bd47bec8691b3563`, 2 MiB, LoROM.
- Do not edit `src/gen/` by hand. Change `recomp/symbols.toml`,
  `recomp/bank*.cfg` or the host code, then regenerate.
- Do not invent behavior to get past an unresolved target. Leave it on the
  interpreter tier and document the gap.

## Build

```bash
git submodule update --init --recursive
cmake -S . -B build -G Ninja -DCMAKE_BUILD_TYPE=Release
cmake --build build --parallel
```

Linux build dependencies: `docs/linux-build-deps.md`.

## Test

The current input/save-state chain is documented in `tools/scripts/README.md`.
At minimum, verify that the build still reaches the title screen and the first
dungeon after a change that touches the host or analysis configuration.

```bash
./build/KyuuyakuMegamiTenseiSNESRecomp ~/roms/kyuuyaku.sfc
```

For frame comparisons:

```bash
SNESRECOMP_FRAMEDUMP_START=14861 \
SNESRECOMP_FRAMEDUMP_END=14861 \
SNESRECOMP_FRAMEDUMP_PIXELS=1 \
./build/KyuuyakuMegamiTenseiSNESRecomp \
  --script tools/scripts/load-game.txt \
  --framedump /tmp/kmt-frames \
  ~/roms/kyuuyaku.sfc
```

## Reporting a problem

Include:

- the ROM revision (CRC32/SHA-1);
- the commit or branch;
- the input script and frame number;
- the last working checkpoint (`CP-xxx` from `docs/checkpoints.md`);
- the host log and, if possible, the frame dump;
- whether the same scene works in an independent emulator.

## Style

- Keep changes small and focused.
- Match the surrounding C style (`snake_case` functions, existing types).
- Update `docs/checkpoints.md` and `docs/bring-up-log.md` when a milestone
  changes.
- Do not add new dependencies without documenting why.

## License

This project is source-available under the PolyForm Noncommercial License
1.0.0. The snesrecomp framework and its third-party components keep their own
terms; see `snesrecomp/LICENSE` and
`snesrecomp/THIRD_PARTY_ATTRIBUTION.md`.
