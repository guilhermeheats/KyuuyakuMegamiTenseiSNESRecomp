# Cobertura estática e decompilação

Este documento registra a virada do foco para a **decompilação estática**:
aumentar o grafo que o `snesrecomp` descobre e emite em `src/gen/*.c`, em vez
de continuar validando cenas de gameplay. Gameplay e save states continuam
úteis, mas como **regressão**, não como objetivo.

## Linha de base (2026-11-18, antes)

- 9 funções nomeadas em `recomp/symbols.toml`; 7 pedidos AOT.
- 51 entradas no dispatch principal; 54 variantes AOT.
- 8 bancos emitidos; `src/gen` com ~1,3 MB.
- No boot, `interp_stats` mostrava **99,43%** dos ciclos no interpretador
  (LLE) e 0,57% em AOT.

## Captura de cobertura

Build de debug com captura de cobertura:

```bash
SNESRECOMP_TIER2_MANIFEST=/tmp/opencode/coverage/kyuuyaku-tier2.json \
SNESRECOMP_TIER2_JOURNAL=/tmp/opencode/coverage/kyuuyaku-tier2.jsonl \
./build-debug/KyuuyakuTen --no-launcher --coverage-capture=on \
  "$HOME/roms/kyuuyaku.sfc"
```

Foi capturado o boot/título e depois carregados os save states de 8F, 7F,
batalha de Basim e tela de level-up. O `tier2_ingest.py` foi usado para
auditar a captura contra `src/gen/program_manifest.json`:

```bash
python3 snesrecomp/tools/tier2_ingest.py \
  /tmp/opencode/coverage/kyuuyaku-tier2.json \
  --cfg-dir recomp \
  --program-manifest src/gen/program_manifest.json \
  --json > /tmp/opencode/coverage/report.json
```

O relatório do boot mostrou 67 descobertas e 2.270 PCs de instrução
interpretada, com destaque para:

| PC | Interpretações | Uso |
|---|---:|---|
| `$00:93C2/93C5` | 6,3M cada | espera de frame |
| `$3F:C41A/C41D` | 1,64M cada | loop de VBlank/joypad |
| `$38:8145/8148` | 255K cada | espera de acknowledge da APU |
| `$01:D5B3` | 4.557 | helper de texto/menu |
| `$01:D419` | 2.110 | helper de texto/menu |
| `$01:D581` | 2.156 | helper de texto/menu |

## Roots permanentes

Foram adicionadas ao `recomp/symbols.toml` (com `emit = true`) as rotinas
identificadas no caminho quente:

- `MainFrameWait` (`$3F:C411`), `FrameUpdate` (`$3F:C4AA`),
  `PPUUpdate` (`$3F:C4C7`), `APUUpdate` (`$3F:C5B8`);
- `CopyBlock` (`$01:D61B`);
- `TextHelperD419` (`$01:D419`), `TextHelperD581` (`$01:D581`),
  `TextHelperD5B3` (`$01:D5B3`);
- `ScreenOff` (`$01:8066`), `InitPPU` (`$01:80C9`);
- `AddLongCounter` (`$01:8E92`), `ApuCommand` (`$01:EBA5`);
- `FrameWaitWrapper` (`$01:8EAB`), `FrameWait` (`$00:9397`).

Além disso, os roots descobertos pela captura foram gravados como diretivas
`func Coverage_<bank>_<addr>_V<mx>` nos `recomp/bank*.cfg` (fora do bloco
gerado). Eles são placeholders até a função ser nomeada; a lista está nos
bancos `$00`, `$01`, `$02`, `$03`, `$30`, `$38` e `$3F`.

## Resultado

Com `tools/regen.sh` (agora com `--cfg-roots` por padrão):

| Métrica | Antes | Depois |
|---|---:|---:|
| Roots | 11 | 73 |
| Variantes exatas | 60 | 119 |
| Variantes AOT-eligible | 54 | 107 |
| Variantes LLE-only | 6 | 12 |
| Bancos emitidos | 8 | 10 |
| Entradas de dispatch | 51 | 97 |
| Entradas com AOT | 46 | 88 |
| Variantes AOT no dispatch | 54 | 107 |

No mesmo build, após carregar os save states de 8F/7F/batalha/level-up, o
`interp_stats` acumulado mostrou **94,7% AOT / 5,3% interpretado** (o boot
isolado fica mais baixo porque a inicialização de APU/PPU é dominada por
esperas de hardware). O `dispatch_total` ficou em 60.643, com `found1` em
100% e zero dispatch misses.

No teste final carregando apenas `save4` (level-up) e `save9` (pós-Basim), o
acumulado ficou em **99,14% AOT / 0,86% interpretado**. Nesse caminho o stub
`$0086E9` reapareceu durante o desenho do texto de level-up, com o histórico
`$01:D581 → $01:D5B3 → ... → $00:86C0`; ou seja, o ponteiro de HDMA também
passa por `$FFFF` fora do boot.

## Correções no `tools/regen.sh`

O ganho depende de o regen realmente semear os `func` dos cfgs:

- `--cfg-roots` passou a ser o padrão;
- `--profile-manifest <path>` foi adicionado para semear roots a partir de
  uma captura tier-2;
- `--no-host-root-scan` evita que o `recomp/funcs.h` antigo vire fonte de
  roots duplicados;
- o `funcs.h` é gerado em um caminho temporário **fora** da raiz do projeto
  e só é copiado para `recomp/funcs.h` após o generate. Sem isso, o scanner
  de roots readicionava as declarações antigas e o link-closure falhava com
  28 variantes pendentes.

## Stubs de dispatch pendentes

O boot/título ainda registra dois `dispatch_oob` no `unresolved_stub_get`:

| Site | Alvo | Frame | Stack top |
|---|---|---:|---|
| `$00:86E9` | `$00:FFFF` | 2689 | `Coverage_00_86C0_V10_M1X0` |
| `$00:88E9` | `$00:FFFF` | 3470 | `Coverage_00_88CE_V10_M1X0` |

Os dois sites são `JMP ($0100)` através de um ponteiro em WRAM:

- `$00:86C0` é o parser de tabela de HDMA; lê um índice em `$1800/Y` e uma
  tabela em `$86FE` (`$870E`, `$8721`, `$8760`, `$8782`, `$8791`, `$87B8`,
  `$87F3`, `$883E`);
- `$00:88CE` é o dispatcher de modo de HDMA; lê `$0901` e a tabela `$88EC`
  (`$8916`, `$8908`, `$8910`, `$88F4`).

O ponteiro vivo em `$0100` chega a `$FFFF` nesses caminhos de boot. É o
próximo alvo de decompilação: comparar com o `snesref`/MesenCE, confirmar se
o `$FFFF` é um sentinela intencional ou um ponteiro ainda não inicializado,
e então declarar `indirect_dispatch`/tabela ou corrigir o emitter. Uma
tentativa inicial de `indirect_dispatch ... ptrtail targets:...` elevou a
análise para 131 variantes, mas o link-closure rejeitou 28 variantes
chamadas e não definidas; as diretivas foram revertidas até o caso ser
entendido.

## Próximos passos

1. Resolver `$00:86E9` e `$00:88E9` (ponteiro/HDMA) e reativar os hints de
   dispatch com link-closure limpo.
2. Capturar uma rota mais longa (8F, 7F, 6F, menus, batalha, level-up),
   ingerir e adicionar os novos roots.
3. Investigar os 12 variantes LLE-only, começando por `$00:9397`
   (`truncated_call_continuation`, `unproven_call_at_0093B4_to_018EAB_m1x0`,
   `unproven_callee_exit`) e `$01:8EAB`.
4. Nomear os placeholders `Coverage_*`, principalmente nos bancos `$30`,
   `$38` e `$3F`.
5. Manter gameplay, save states e comparação com emulador como regressão.
