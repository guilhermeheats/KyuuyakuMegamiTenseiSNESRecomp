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

- A configuração do CMake parou porque faltam bibliotecas de desenvolvimento do sistema:
  - X11/Wayland: SDL não encontra backend de janela;
  - OpenGL: o host desktop exige `OpenGL::GL`;
  - ALSA/Pulse: áudio opcional, mas necessário para uma experiência completa.
- Solução: instalar os pacotes de `docs/linux-build-deps.md` e reconfigurar.

### Próximo passo

1. Instalar as dependências de build.
2. Configurar e compilar `build/`.
3. Executar o binário com a ROM e registrar o primeiro frame de boot no `docs/checkpoints.md`.
4. Se o boot não chegar ao logo/título, capturar o log e comparar com o MesenCE.
