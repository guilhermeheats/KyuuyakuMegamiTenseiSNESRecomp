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
cd ~/Projects/KyuuyakuTen
cmake -S . -B build -G Ninja -DCMAKE_BUILD_TYPE=Release
cmake --build build --parallel
```

O binário fica em `build/KyuuyakuTen`.

## GCC ou Clang?

O build validado usa **GCC 15.3.0**, e ele é suficiente para o projeto. O
snesrecomp e o SDL3 também suportam Clang; não há requisito de “matching” de
compilador, porque o objetivo é fidelidade de execução, não gerar o mesmo
binário da ROM.

Recomendação prática:

- **GCC** para o build de release: é o padrão do openSUSE, já está validado e
  não exige instalação extra.
- **Clang** para desenvolvimento e diagnóstico: mensagens melhores,
  `clang-tidy`, `-fsanitize=address,undefined` e builds às vezes mais rápidos.
- Se um bug aparecer em um compilador e não no outro, isso é sinal de
  comportamento indefinido no código do host; vale investigar, mas não é
  motivo para trocar o compilador de release.

Build alternativo com Clang (não substitui o `build/` validado):

```bash
cmake -S . -B build-clang -G Ninja -DCMAKE_BUILD_TYPE=Release \
  -DCMAKE_C_COMPILER=clang \
  -DCMAKE_CXX_COMPILER=clang++ \
  -DCMAKE_CXX_FLAGS="--gcc-install-dir=/usr/lib64/gcc/x86_64-suse-linux/15"
cmake --build build-clang --parallel
```

No openSUSE Leap 16, o Clang 19 não encontra o `libstdc++` e os headers C++ do
GCC sozinho; o `--gcc-install-dir` resolve isso. Em outras distros, remova a
flag se o Clang já encontra o `libstdc++` ou use `-stdlib=libc++` com o
`libc++-devel` instalado.

`build-*` já está no `.gitignore`. O build Clang foi validado com o mesmo save
state da dungeon; a única diferença observada foi um warning no
`recomp-ui` (submódulo), não no código do jogo.

## Execução

```bash
./build/KyuuyakuTen ~/roms/kyuuyaku.sfc
```

Para abrir direto na primeira dungeon usando o save state local:

```bash
./build/KyuuyakuTen \
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
./build/KyuuyakuTen \
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

- O menu de status, o auto-mapping e a primeira batalha já foram validados.
- A rota do 8F está confirmada em `docs/route-8f.md`: Gate Keeper em `(2,2)`,
  escada em `(2,3)` e chegada ao 7F em `(10,2)`.
- O servidor de debug funciona e `0x877`/`0x878`/`0x865` dão a posição; a
  grade do mapa ainda não está totalmente mapeada para o 7F.
- A gravação/flush do save real (SRAM de 8 KiB) foi validada; o carregamento
  pelo título ainda falha (CP-013). Os save states do host são apenas para
  desenvolvimento.
- O state `save2` tem o nome `ナカジマあああ` por causa do avanço automático
  com A. É artefato de teste, não bug do recomp.
- Os scripts de input dependem do timing atual; ajustes de `wait` podem ser
  necessários se o build mudar.
- Apenas a ROM japonesa original (`c8d286c9`) é suportada.
- Não há widescreen, tradução ou MSU-1; o foco é a fidelidade do jogo original.

### AOT

As primeiras rotinas de jogo promovidas para AOT são as de SRAM em bank `$03`:
`Sram_SaveSlot` (`$A35B`), `Sram_LoadSlot` (`$A3BF`), `Sram_CheckHeader`
(`$A397`), `Sram_Checksum` (`$ACFB`) e `Sram_ValidateChecksums` (`$AD20`), com
`entry_m = 1` e `entry_x = 0`. O analyzer gerou 14 variantes AOT e 0 LLE-only.
O save AOT produziu o mesmo hash de SRAM do save LLE; o load pelo título ainda
está bloqueado.

## Próximos passos

1. Fechar CP-013: achar por que o `CONTINUE` do título rejeita o save e zera a
   SRAM; comparar com um save válido de emulador e instrumentar as leituras de
   SRAM do caminho de load.
2. Completar a validação de batalha: vitória/derrota/recrutamento, recompensas
   e level-up, além do `TALK` já validado.
3. Comparar boot/dungeon/batalha com o MesenCE usando frames e WRAM.
4. Nomear as rotinas descobertas em `recomp/symbols.toml` — começando pelo
   caminho da batalha — e promover as seguras para AOT (`emit = true`).
5. Expandir a cobertura para o restante do MT1 (7F, 6F, ...).
