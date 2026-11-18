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

| Métrica | Linha de base | Depois do contrato `$00:9397` |
|---|---:|---:|
| Roots | 11 | 72 |
| Variantes exatas | 60 | 339 |
| Variantes AOT-eligible | 54 | 292 |
| Variantes LLE-only | 6 | 47 |
| Bancos emitidos | 8 | 10 |
| Entradas de dispatch | 51 | 279 |
| Entradas com AOT | 46 | 239 |
| Variantes AOT no dispatch | 54 | 292 |

No mesmo build, após carregar os save states de 8F/7F/batalha/level-up, o
`interp_stats` acumulado mostrou **~94,7% AOT / ~5,3% interpretado** (o boot
isolado fica mais baixo porque a inicialização de APU/PPU é dominada por
esperas de hardware). O `dispatch_total` ficou na casa dos 60 mil, com
`found1` em 100% e zero dispatch misses.

Antes do contrato de saída, o teste carregando `save4` (level-up) e `save9`
(pós-Basim) ficava em **98,8% AOT / 1,2% interpretado**. Os dois dispatchers
de HDMA (`$00:86C0`/`$00:88CE`) estão em LLE, então o
`unresolved_stub_get` retorna **zero**: o fallback AOT que registrava
`dispatch_oob` não é mais usado. O contrato abaixo levou o mesmo teste a
**99,4% AOT**.

### Contrato de saída de `$00:9397` (2026-11-18)

`$00:9397` é a primitiva de espera de frame. Ela empilha `PHP` na entrada e
restaura com `PLP` em `$93F0`; `PLX` restaura o X do chamador. Portanto a
largura de saída **espelha a largura de entrada**, embora o corpo use
`REP/SEP` internamente. O cfg agora declara:

```text
exit_mx_variant 009397 0 0 0 0
exit_mx_variant 009397 1 0 1 0
exit_mx_variant 009397 1 1 1 1
```

Isso prova o retorno para todos os chamadores e destrava a análise que antes
parava em `unproven_callee_exit`. O grafo saltou de **118 para 339 variantes
exatas** e de **105 para 292 variantes AOT**; o `$02:B0B6` (que chama
`$00:9397`) passou a AOT nas variantes M1X0/M1X1. O custo é que a análise
passou a seguir caminhos pós-chamada que antes ficavam truncados, expondo
**47 nós LLE-only** (a fronteira atual, descrita abaixo).

Validação de runtime com o build de debug:

- `save4` (level-up): **99,43% AOT / 0,57% interpretado**, zero stubs;
- `save9` (pós-Basim): **99,34% AOT / 0,66% interpretado**, zero stubs;
- título contra o `snesref`: mesmos **6 bytes** de WRAM, SRAM idêntica e
  framebuffer AE 2353 / RMSE 30,29;
- `$02:B0B6` agora tem variantes AOT M1X0 e M1X1 no manifesto.

Os próprios nós do ciclo de boot continuam LLE: `$00:9397`, `$00:8014` e
`$01:8EAB` (o `$00:820E` foi promovido). O caminho de inicialização
`$9397 → $8EAB → $8014` é terminal, então não há contrato de retorno a
inventar para ele.

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
`unresolved_stub_get` retorna **zero** e a rota save4/save9 fica em
**99,4% AOT / 0,6% interpretado**. O custo continua sendo duas funções em
LLE; o resto do grafo cresceu para 292 variantes AOT com o contrato de
`$00:9397`.

O próximo passo de decompilação é **modelar esse dispatch vivo no emitter**
(ou declarar `indirect_dispatch` de forma que o link-closure aceite os 8+4
alvos), comparar o caminho com `snesref`/MesenCE e então re-promover as duas
funções. Uma tentativa inicial de `indirect_dispatch ... ptrtail targets:...`
elevou a análise para 131 variantes, mas o link-closure rejeitou 28 variantes
chamadas e não definidas; as diretivas foram revertidas.

## Fronteira atual: 47 nós LLE-only

O contrato de `$00:9397` promoveu todos os seus chamadores, mas também
expôs o código pós-chamada que antes ficava truncado. Os 47 nós LLE-only
restantes se agrupam em poucas cadeias:

| Cadeia | Bloqueio | Observação |
|---|---|---|
| `$00:8014` → `$05:D6BF` → `$05:D731` → `$02:AFF9` | `unproven_callee_exit` | loop principal; `$05:DD6D` tem `brk_at_05E5DB` |
| `$00:9077` → `$00:9188` → `$30:8BF0`/`$30:95CA`/`$30:A20D`/`$30:DD34`/`$30:ECF4` | `unproven_callee_exit` | bloco do banco `$30` (provável motor de som/gráficos) |
| `$01:8613`/`$01:91DA` → `$03:983C` | `unproven_callee_exit` | `$03:983C` é chamado por vários bancos e é o maior gargalo único |
| `$03:983C` → `$03:9C66`/`$01:DF34`/`$03:A630` | `unproven_callee_exit` | `$03:A630` volta para `$00:9077` e `$30:D226` |
| `$02:AFF9` → `$02:DC53`/`$03:E91A`/`$01:91DA`/`$03:A2EA` | `unproven_callee_exit` | lógica do banco `$02`; variantes M0X1/M1X0/M1X1 |
| `$04:BE39`/`$05:DD6D` | `brk_at_*` / `structural_poison` | provável dados lidos como código; separar antes de promover |

Os nós do ciclo de boot continuam LLE: `$00:9397` (M0X0/M0X1/M1X0/M1X1),
`$00:8014` (M1X1) e `$01:8EAB` (M1X0). O caminho
`$9397 → $8EAB → $8014` é terminal (o `$8014` termina em `BRA $8113`), então
não há retorno para provar. O `$00:820E` foi promovido porque seu loop
`JSL $9397; BRA $8274` agora tem largura de retorno conhecida.

O próximo passo de maior alavancagem é declarar contratos de saída para os
chamados repetidos `$03:983C` e `$02:AFF9`, **um de cada vez**, validando
save4/save9 e a comparação com o `snesref` após cada contrato. Os caminhos
com `brk_at_*` devem ser tratados como separação código/dados, não como AOT.

## Sonda `v2_regen`: dispatches restantes

O pipeline `v2_regen.py` (com o fixpoint de auto-promote/reference-taint) é
rodado como sonda com `--tier-down-stubs`; ele não é o pipeline padrão do
projeto. O antigo overrun `max_insns=12000` em `$02:B0B6` **não era dados
lidos como código**: era uma variante fantasma **M0X1** promovida por um
caller de largura errada, que deslocava os imediatos e decodificava até
estourar. A correção no cfg é explícita:

```text
func Clamp_024E_TierWait b0b6 end:b0fa entry_mx:1,1
force_variant_at 02B0B0 1 1
force_variant_at 02BD87 1 1
```

Com isso o probe emite **7/7 bancos** e 797 entradas de dispatch. Ele ainda
lista 31 sites indiretos sem tabela declarada (o banco `$02` agora contribui
`$02:DC74`):

| Site | Forma | Ocorrências | Observação |
|---|---|---:|---|
| `$00:9B04` | JMP (abs) | 4 | banco `$00` |
| `$01:C72B` | JMP (abs) | 4 | banco `$01` |
| `$01:CD9C` | JMP (abs) | 4 | banco `$01` |
| `$01:EF15` | JMP (abs) | 4 | banco `$01` |
| `$02:DC74` | JMP (abs) | 4 | banco `$02`, dentro de `$02:DC53` |
| `$30:969C` | JMP [abs] | 2 | operand `$0080AE` |
| `$30:A33C` | JMP [abs] | 2 | operand `$0080AE` |
| `$30:C078` | JMP [abs] | 2 | operand `$0080AE` |
| `$30:C19B` | JMP [abs] | 2 | operand `$0080AE` |
| `$30:D266` | JMP [abs] | 2 | operand `$0080AE` |
| `$30:D6DB` | JMP [abs] | 1 | operand `$0080AE` |

Os sites `$30:*` compartilham o ponteiro `$0080AE`, provavelmente um
dispatcher comum do motor de som. O probe também rejeitou três alvos
JSR/JSL fora do LoROM (`$30:00A0`, `$30:00BD`, `$30:7EA9`) e registrou um
fold constante-Z em `$00:AA11` (BEQ → fall-through, alvo morto `$00:A998`).
Os dois sites de HDMA (`$00:86E9`/`$00:88E9`) não aparecem nessa lista porque
as diretivas `indirect_dispatch ... ptrtail` os resolvem no probe.

O build padrão (`v2_emit`) ainda usa o fallback LLE nesses 31 sites; eles são
os próximos candidatos a `indirect_dispatch`/tabela. Os caminhos com
`brk_at_*` (`$04:BE39`, `$05:DD6D`) são candidatos a separação código/dados,
não a promoção AOT.

## Próximos passos

1. Declarar contratos de saída para os gargalos repetidos `$03:983C` e
   `$02:AFF9`, um de cada vez, validando `save4`/`save9` e a comparação com
   o `snesref` depois de cada contrato.
2. Modelar o `JMP ($0100)` dos dispatchers de HDMA no emitter, reativar
   `indirect_dispatch` com link-closure limpo e re-promover
   `$00:86C0`/`$00:88CE`.
3. Declarar as tabelas dos sites `$00:9B04`, `$01:C72B`/`CD9C`/`EF15`,
   `$02:DC74` e `$30:*` (ponteiro `$0080AE`); separar os caminhos
   `brk_at_*` (`$04:BE39`, `$05:DD6D`) como código/dados.
4. Capturar uma rota mais longa (8F, 7F, 6F, menus, batalha, level-up),
   ingerir com `tier2_ingest.py` e adicionar os novos roots.
5. Nomear os placeholders `Coverage_*`, principalmente nos bancos `$30`,
   `$38` e `$3F`, e continuar a separação código/dados.
6. Manter gameplay, save states e comparação com emulador como regressão.
