# Desenvolvimento

Este documento reúne o ambiente usado, o estado atual, as ferramentas e o
fluxo de teste. Para o diário cronológico, veja `docs/bring-up-log.md`.

## Estado atual

Atualizado em 2026-11-16.

| Etapa | Estado |
|---|---|
| ROM japonesa limpa verificada | OK — CRC32 `c8d286c9` |
| Scaffold do snesrecomp | OK — 4 roots, 1 banco |
| Build nativo | OK — 514 alvos, binário de 8,0 MB |
| Boot / tela de título | OK |
| Introdução do MT1 | OK |
| Nome do protagonista e da Yumiko | OK |
| Distribuição de status | OK |
| Primeira dungeon | OK |
| Movimento | OK |
| Interação com baú | OK — loot `500` + `宝玉` |
| Menu de status | OK — COMP/MAGIC/ITEM/STATUS e ficha |
| Auto-mapping | OK — mapa da dungeon pelo menu COMP |
| Primeira batalha | pendente |
| Save/load via SRAM do jogo | pendente |

Marcos de frame observados com `--framedump`:

| Frame | Cena |
|---:|---|
| 600 | boot, tela preta |
| 1800 | texto de abertura |
| 3600 | tela de título |
| 4200 | introdução do MT1 |
| 11299 | nome do protagonista |
| 11883 | nome da Yumiko |
| 12667 | status do protagonista |
| 14861 | primeira dungeon |
| 15100 | diálogo do baú |
| 15500 | loot do baú (`500` + `宝玉`) |
| 16400 | menu principal (COMP/MAGIC/ITEM/STATUS) |
| 16600 | submenu COMP (aliados, auto-mapping, config) |
| 16800 | ficha de status; auto-mapping |

## Ambiente

- openSUSE Leap 16.0
- GCC 15.3.0
- CMake 4.4.5 (instalado via `pip --user`)
- Ninja 1.13.2 (instalado via `pip --user`)
- Rust 1.100.0 (rustup)
- Python 3.13
- SDL3 3.4.10 compilado do source pelo CMake
- snesrecomp pinado em `80a41241e39bfffd384506fbe7ca65b386e03050`
- recomp-ui pinado em `a760b2714b882f22ae4124073583dfc5b147b1c6`

Dependências de sistema no openSUSE: `docs/linux-build-deps.md`.

## Build

```bash
cd ~/Projects/KyuuyakuMegamiTenseiSNESRecomp
cmake -S . -B build -G Ninja -DCMAKE_BUILD_TYPE=Release
cmake --build build --parallel
```

O binário fica em `build/KyuuyakuMegamiTenseiSNESRecomp`.

## Execução

```bash
./build/KyuuyakuMegamiTenseiSNESRecomp ~/roms/kyuuyaku.sfc
```

Para abrir direto na primeira dungeon usando o save state local:

```bash
./build/KyuuyakuMegamiTenseiSNESRecomp \
  --script tools/scripts/load-game.txt \
  ~/roms/kyuuyaku.sfc
```

Os save states ficam em `build/saves/` e não entram no Git.

## Fluxo de teste

O host aceita scripts de input (`--script`) e despejo de frames
(`--framedump`). A cadeia documentada em `tools/scripts/README.md` cobre:

1. título;
2. introdução;
3. nome do protagonista;
4. nome da Yumiko;
5. status;
6. primeira dungeon;
7. baú.

Exemplo de captura:

```bash
SNESRECOMP_FRAMEDUMP_START=14861 \
SNESRECOMP_FRAMEDUMP_END=14861 \
SNESRECOMP_FRAMEDUMP_PIXELS=1 \
./build/KyuuyakuMegamiTenseiSNESRecomp \
  --script tools/scripts/load-game.txt \
  --framedump /tmp/kmt-frames \
  ~/roms/kyuuyaku.sfc
```

## Ferramentas recomendadas

| Ferramenta | Uso |
|---|---|
| snesrecomp | Recompilador, runner, launcher e save states |
| MesenCE / Mesen2 | Debugger, trace logger, PPU/APU viewer e comparação |
| Ghidra + ghidra-snes | Análise estática e desmontagem 65816 |
| ImageMagick | Converter e montar frames de teste |
| `gh` | Publicação e manutenção do repositório |
| Python | Scripts de análise, hashes e automação |

O MesenCE ainda não foi usado neste projeto; a comparação com um emulador
independente é o próximo passo de validação.

## Limitações conhecidas

- A primeira batalha e o menu de status ainda não foram validados.
- O save real do jogo (SRAM de 8 KiB) ainda não foi testado; os save states do
  host são apenas para desenvolvimento.
- O state `save2` tem o nome `ナカジマあああ` por causa do avanço automático
  com A. É artefato de teste, não bug do recomp.
- Os scripts de input dependem do timing atual; ajustes de `wait` podem ser
  necessários se o build mudar.
- Apenas a ROM japonesa original (`c8d286c9`) é suportada.
- Não há widescreen, tradução ou MSU-1; o foco é a fidelidade do jogo original.

## Próximos passos

1. Andar até um encontro e validar a primeira batalha.
2. Abrir o menu de status e conferir os valores dos personagens.
3. Salvar via SRAM, reiniciar e carregar.
4. Comparar o boot com o MesenCE usando frames e WRAM.
5. Nomear as rotinas descobertas em `recomp/symbols.toml`.
6. Expandir a cobertura para o restante do MT1.
