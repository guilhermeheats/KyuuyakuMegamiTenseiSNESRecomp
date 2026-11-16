# Bring-up log

## 2026-11-16

### ROM

- Escolhida a ROM japonesa original (No-Intro), sem header: 2 MiB, LoROM, 8 KiB SRAM, sem coprocessador.
- CRC32 `c8d286c9`, SHA-1 `827f6e0534e2317e3348ce76bd47bec8691b3563`.
- A revisão 1 (`e257d574`) foi descartada para este projeto; é outra revisão.
- `probe_rom.py` confirmou `checksum_valid=True`.

### Projeto

- Repositório criado em `~/Projects/KyuuyakuMegamiTenseiSNESRecomp`.
- Scaffold do snesrecomp gerado com 1 jogador, sem netplay, sem GitHub.
- `tools/regen.sh` gerou 4 arquivos C em `src/gen/`, 1 banco e 4 roots.
- `I_RESET` (`$8000`) e `I_NMI` (`$827A`) vieram do scaffold.
- O vetor IRQ foi localizado em `$C672`. Uma tentativa de semeá-lo como `I_IRQ` (`emit = false`) zerou os roots da análise; a entrada foi revertida e o vetor ficou apenas documentado em `docs/rom-map.md`.
- `recomp/bank00.cfg` foi atualizado pelo regen com o bloco de símbolos.

### Build

- A primeira configuração parou por falta de bibliotecas de desenvolvimento do sistema (X11/Wayland/OpenGL/XTest).
- Instalados os pacotes de `docs/linux-build-deps.md`; o `libXtst-devel` foi o último necessário para o SDL habilitar XTest.
- Configuração e build concluídos:
  - binário: `build/KyuuyakuMegamiTenseiSNESRecomp` (8,0 MB)
  - 514 alvos compilados
  - SDL3 3.4.10 compilado do source, com X11, Wayland, OpenGL, ALSA e PipeWire.

### Runtime

- `./build/KyuuyakuMegamiTenseiSNESRecomp ~/roms/kyuuyaku.sfc`
- Janela 960x720, renderer OpenGL, áudio PipeWire a 32 kHz.
- ~60 fps; a ROM carrega e o jogo executa.
- Marcos observados com `--framedump`:
  - frame 600: tela preta (início do boot)
  - frame 1800: texto de introdução em japonês
  - frame 3600: tela de título “旧約・女神転生”
  - frame 3720: transição após pressionar Start
  - frame 4200: texto da introdução do MT1
- Nenhum screenshot do jogo foi commitado; os frames ficam em `/tmp`.

### Próximo passo

1. Entender a sequência de input do título/introdução e chegar ao primeiro menu jogável.
2. Mapear a seleção de save e a primeira sala da dungeon (`CP-002`/`CP-004`).
3. Comparar o boot com o MesenCE e registrar um checkpoint com hash de WRAM.
4. Começar a nomear as rotinas descobertas em `recomp/symbols.toml`.
