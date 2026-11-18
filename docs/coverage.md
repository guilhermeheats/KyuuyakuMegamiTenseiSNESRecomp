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
| Roots | 11 | 71 |
| Variantes exatas | 60 | 117 |
| Variantes AOT-eligible | 54 | 105 |
| Variantes LLE-only | 6 | 12 |
| Bancos emitidos | 8 | 10 |
| Entradas de dispatch | 51 | 95 |
| Entradas com AOT | 46 | 86 |
| Variantes AOT no dispatch | 54 | 105 |

No mesmo build, após carregar os save states de 8F/7F/batalha/level-up, o
`interp_stats` acumulado mostrou **~94,7% AOT / ~5,3% interpretado** (o boot
isolado fica mais baixo porque a inicialização de APU/PPU é dominada por
esperas de hardware). O `dispatch_total` ficou na casa dos 60 mil, com
`found1` em 100% e zero dispatch misses.

No teste final carregando `save4` (level-up) e `save9` (pós-Basim), o
acumulado ficou em **98,8% AOT / 1,2% interpretado**. Os dois dispatchers de
HDMA (`$00:86C0`/`$00:88CE`) estão em LLE nesse build, então o
`unresolved_stub_get` retorna **zero**: o fallback AOT que registrava
`dispatch_oob` não é mais usado.

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

## Dispatchers de HDMA (mitigados por LLE)

O build anterior registrava dois `dispatch_oob` no `unresolved_stub_get`:

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

O `dispatch_oob` era o **fallback estático** do emitter: o corpo AOT não
materializava o alvo vivo e caía no interpretador em `$86E9`/`$88E9`, com um
trace fixo em `$FFFF`. O ponteiro vivo podia ser válido; o aviso não era uma
prova de crash.

Para manter o build honesto e sem falso alarme, as duas funções foram
marcadas com `force_lle 0086C0`/`force_lle 0088CE` em `recomp/bank00.cfg`.
Agora o interpretador executa o `JMP ($0100)` com o ponteiro vivo,
`unresolved_stub_get` retorna **zero** e a rota save4/save9 fica em **98,8%
AOT / 1,2% interpretado**. O custo é duas variantes AOT a menos (105 em vez
de 107).

O próximo passo de decompilação é **modelar esse dispatch vivo no emitter**
(ou declarar `indirect_dispatch` de forma que o link-closure aceite os 8+4
alvos), comparar o caminho com `snesref`/MesenCE e então re-promover as duas
funções. Uma tentativa inicial de `indirect_dispatch ... ptrtail targets:...`
elevou a análise para 131 variantes, mas o link-closure rejeitou 28 variantes
chamadas e não definidas; as diretivas foram revertidas.

## LLEs restantes: o ciclo do frame wait

Os 12 nós LLE-only do build atual formam um **ciclo de recursão mútua** em
torno da espera de frame:

```text
$00:8014 --JSL $820E--> $00:820E --JSL $9397--> $00:9397
   ^                                                  |
   |                                                  JSL $018EAB ($93B4)
   +---------------------- JSL $008014 ($8EBE) <------ $01:8EAB
```

Nós LLE-only: `$00:8014` (M1X1), `$00:820E` (M1X0),
`$00:9397` (M0X0/M1X0/M1X1), `$00:93F2` (M0X0/M1X0),
`$01:8078` (M1X0), `$01:8EAB` (M1X0), `$01:B3C6` (M1X1),
`$02:EDE8` (M1X0) e `$02:F835` (M0X0).

O analyzer propaga `unproven_callee_exit` e
`truncated_call_continuation` por esse ciclo: `$00:9397` chama
`$01:8EAB` em `$93B4`, que chama `$00:8014` em `$8EBE`, que chama
`$00:820E`, que volta a `$00:9397`. O `LevelUp_Apply` (`$01:B3C6`) entra
no mesmo ciclo porque também chama `$00:9397`.

O cfg atual só oferece `noreturn_jsr`/`terminal_jsr` para JSR de 2 bytes;
o site `$8EBE` é um **JSL** de 3 bytes. O próximo passo de framework é
modelar esse JSL como transferência terminal/entrada (ou fornecer fatos de
saída para o ciclo) e então promover `$00:9397`, `$00:93F2`, `$01:8EAB` e
`LevelUp_Apply`.

## Próximos passos

1. Modelar o `JMP ($0100)` dos dispatchers de HDMA no emitter, reativar
   `indirect_dispatch` com link-closure limpo e re-promover
   `$00:86C0`/`$00:88CE`.
2. Capturar uma rota mais longa (8F, 7F, 6F, menus, batalha, level-up),
   ingerir com `tier2_ingest.py` e adicionar os novos roots.
3. Resolver o ciclo de frame wait (`$00:8014`/`$00:820E`/`$00:9397`/
   `$01:8EAB`) com suporte a JSL terminal/entrada; depois promover
   `$00:9397`, `$00:93F2`, `$01:8EAB` e `LevelUp_Apply`.
4. Nomear os placeholders `Coverage_*`, principalmente nos bancos `$30`,
   `$38` e `$3F`, e continuar a separação código/dados.
5. Manter gameplay, save states e comparação com emulador como regressão.
