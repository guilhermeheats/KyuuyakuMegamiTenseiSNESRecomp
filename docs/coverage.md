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

| Métrica | Linha de base | Depois dos contratos |
|---|---:|---:|
| Roots | 11 | 72 |
| Variantes exatas | 60 | 1081 |
| Variantes AOT-eligible | 54 | 1031 |
| Variantes LLE-only | 6 | 50 |
| Bancos emitidos | 8 | 12 |
| Entradas de dispatch | 51 | 816 |
| Entradas com AOT | 46 | 769 |
| Variantes AOT no dispatch | 54 | 1031 |

No mesmo build, após carregar os save states de 8F/7F/batalha/level-up, o
`interp_stats` acumulado mostrou **~94,7% AOT / ~5,3% interpretado** (o boot
isolado fica mais baixo porque a inicialização de APU/PPU é dominada por
esperas de hardware). O `dispatch_total` ficou na casa dos 60 mil, com
`found1` em 100% e zero dispatch misses.

Antes dos contratos de saída, o teste carregando `save4` (level-up) e `save9`
(pós-Basim) ficava em **98,8% AOT / 1,2% interpretado**. Os dois dispatchers
de HDMA (`$00:86C0`/`$00:88CE`) estão em LLE, então o
`unresolved_stub_get` retorna **zero**: o fallback AOT que registrava
`dispatch_oob` não é mais usado. Os dois destravamentos abaixo levaram o
mesmo teste a **99,4–99,9% AOT**.

### Destravamento 1: contrato de saída de `$00:9397`

`$00:9397` é a primitiva de espera de frame. Ela empilha `PHP` na entrada e
restaura com `PLP` em `$93F0`; `PLX` restaura o X do chamador. Portanto a
largura de saída **espelha a largura de entrada**, embora o corpo use
`REP/SEP` internamente. O cfg declara as quatro variantes:

```text
exit_mx_variant 009397 0 0 0 0
exit_mx_variant 009397 0 1 0 1
exit_mx_variant 009397 1 0 1 0
exit_mx_variant 009397 1 1 1 1
```

Isso prova o retorno para todos os chamadores e destrava a análise que antes
parava em `unproven_callee_exit`. O `$02:B0B6` (que chama `$00:9397`) passou
a AOT nas variantes M1X0/M1X1, e o `LevelUp_Apply` (`$01:B3C6`, que chama
`$9397` em M0X1) também foi promovido. O grafo passou de **118 para 339
variantes exatas** e de **105 para 292 AOT**.

### Destravamento 2: `$02:AFF9` e a fronteira de `$05:E5DB`

`$02:AFF9` também começa com `PHP` e seus RTLs em `$B1A7`/`$B1AB` restauram
com `PLP`; `PLX` restaura X. As três variantes de entrada (M0X1/M1X0/M1X1)
retornam com a mesma largura. O contrato:

```text
exit_mx_variant 02AFF9 0 0 0 0
exit_mx_variant 02AFF9 0 1 0 1
exit_mx_variant 02AFF9 1 0 1 0
exit_mx_variant 02AFF9 1 1 1 1
```

Isso permitiu ao decoder continuar depois do `JSL $02AFF9` em `$05:D731`.
A continuação chega a `$05:E556 JMP $E5D9`: no caminho M=1, o terceiro byte
do imediato `LDA #$0001` em `$E5D9` é lido como `BRK` em `$05:E5DB`. O
analyzer trata qualquer `BRK` como `structural_poison` e **descarta todas as
demandas do nó**, o que derrubava o SCC inteiro de 590 para 153 nós.

A correção é uma fronteira de decode de 1 byte em `recomp/bank05.cfg`:

```text
data_region 05 e5db e5dc
```

Ela marca só o byte do `BRK` como não-código. O caminho M=0 válido em
`$E5D9` (`LDA #$0001`, continuação em `$E5DC`) permanece; o caminho M=1 de
erro não contamina o resto do nó. Não é HLE: o runtime AOT/LLE continua
executando os bytes reais; só a análise estática deixa de seguir o caminho
de erro.

Validação de runtime com o build de debug:

- `save4` (level-up): **99,40% AOT / 0,60% interpretado**, zero stubs;
- `save9` (pós-Basim): **99,75% AOT / 0,25% interpretado**, zero stubs;
- título contra o `snesref`: mesmos **6 bytes** de WRAM, SRAM idêntica e
  framebuffer AE 2353 / RMSE 30,29;
- level-up completo + retorno à dungeon: zero stubs;
- `$02:B0B6` tem variantes AOT M1X0/M1X1 no manifesto.

Os nós do ciclo de boot continuam LLE: `$00:9397`, `$00:8014` e `$01:8EAB`
(o `$00:820E` foi promovido). O caminho `$9397 → $8EAB → $8014` é terminal
(o `$8014` termina em `BRA $8113`), então não há contrato de retorno a
inventar para ele.

### Destravamento 3: `$01:8613` (`018613`)

`$01:8613` salva/restaura P e X; o `RTL` em `$8702` restaura ambos. As três
variantes de entrada (M0X1/M1X0/M1X1) retornam com a largura de entrada:

```text
exit_mx_variant 018613 0 1 0 1
exit_mx_variant 018613 1 0 1 0
exit_mx_variant 018613 1 1 1 1
```

O contrato promoveu `$02:D13B` (M1X0/M1X1) e outros chamadores, sem tocar no
caminho de menu do 983C. O A/B com `save9`/`step 60` mostrou **529 AOT / 614
nós / 85 LLE**, AOT **99,89%** e `step 60` em **1,03–1,04s** — o mesmo tempo
do baseline 511. Zero stubs; `save4` em 99,80% AOT e título com os mesmos
6 bytes/SRAM/AE 2353/RMSE 30,29.

### Destravamento 4: cluster `$03:E91A`/`$03:E9B1`

Contratos de saída para `$03:E91A` (M1X0), `$03:E9B1` (M1X1) e para os
callees de folha `$03:EAEE`/`$03:EAFA`/`$03:F415` (M0X0). O cluster promoveu
`$03:E91A` e `$03:E9B1`; `$03:EAEE`/`$03:EAFA`/`$03:F415` continuam LLE
porque ainda chamam `$03:EB06`/`$03:80CA`, mas as larguras de retorno estão
documentadas. O grafo ficou em **615 nós / 532 AOT / 83 LLE**. O A/B de
`step 60` no save9 ficou em **1,03–1,04s**, 99,89% AOT, zero stubs; `save4`
em 99,79% e título com os mesmos 6 bytes/SRAM/AE 2353/RMSE 30,29.

### Destravamento 5: cluster `$03:EB06`/`$03:EEE4` e `$02:AFF9 M0X0`

Contratos para `$03:EB06` (M1X1), `$03:EEE4` (M0X0) e `$03:80CA`
(M1X0/M1X1), mais a variante que faltava no bloco de `$02:AFF9`:
`exit_mx_variant 02AFF9 0 0 0 0`. Sem essa linha, `$03:EEE4` continuava
bloqueado em `unproven_call_at_03EF25_to_02AFF9_m0x0`; com ela, `$03:EEE4`
foi promovido e abriu **71 novos nós**.

Resultado: **690 nós / 603 AOT / 87 LLE**. O A/B de `step 60` no save9 ficou
em **99,90–99,91% AOT**, **1,06–1,09s** (cerca de 3–5% acima do baseline,
não os 12,4x do 983C), zero stubs. `save4` em 99,80% AOT; título com os
mesmos 6 bytes/SRAM/AE 2353/RMSE 30,29.

### Destravamento 6: `$03:8834` e helpers `$00:90EB`/`$00:F160`

Contratos para `$03:8834` (M1X0/M1X1), `$00:90EB` (M1X0/M1X1) e
`$00:F160` (M1X1). Eles promoveram `$03:80CA` (2 variantes) e `$03:F415`,
que eram os dois últimos bloqueios daquele subcluster. Os próprios
`$03:8834`/`$00:90EB`/`$00:F160` continuam LLE com apenas
`truncated_call_continuation`, mas seus chamadores ficaram AOT.

Resultado: **700 nós / 616 AOT / 84 LLE**. A/B de `step 60` no save9:
**99,91% AOT**, **1,05–1,06s**, zero stubs. `save4` em 99,80% AOT; título
com os mesmos 6 bytes/SRAM/AE 2353/RMSE 30,29.

### Destravamento 7: `noreturn_jsl` e o frame wait AOT

`$01:8EAB` tem um `JSL $00:8014` em `$8EBE`; `$00:8014` é o main loop e
**nunca retorna**. O cfg agora declara `noreturn_jsl 8ebe` (bank01) e
`noreturn_jsl 93b4` (bank00, o call site do `JSL $01:8EAB`). A ferramenta
ganhou suporte a `terminal_jsl`/`noreturn_jsl` no cfg_loader, decoder e
emissor Python e no cfg/analyzer/decoder Rust; o delta está em
`patches/snesrecomp-noreturn-jsl.patch` e é aplicado por
`tools/apply-snesrecomp-patch.sh`.

Um atalho anterior (`exit_mx_variant 018EAB 1 0 1 1`) promoveu `$9397`, mas
**quebrou o boot**: o jogo parava em ~795 frames e o título não aparecia. O
`noreturn_jsl` correto mantém o caminho de init terminal e o boot passa.

Resultado: `$00:9397` AOT nas quatro variantes, `$01:8EAB` AOT e `$02:DBB7`
AOT. Com o frame wait AOT, o contrato `$03:983C` deixou de ser lento e foi
adotado: **849 nós / 784 AOT / 65 LLE**. A/B save9: **99,91% AOT**,
`step 60` **1,04–1,06s**; save4 fresco **99,80% AOT**; boot até o título sem
off-rails; título idêntico ao `snesref` (6 bytes/SRAM/AE 2353/RMSE 30,29);
zero stubs.

### Destravamento 8: dispatch `$00:9B04`

Um soak longo no título (frame 666.606) bateu em
`dispatch_oob_$009B04[00FFFF]`, com stack top `bank_00_9A85_M1X1`; o
fallback abandonou a execução e o processo abortou no frame 681.188. O site
é um `JMP ($0000)` com tabela de **32 palavras** em `$9B08`, indexada por
`($0875 & $1F) * 2`. O cfg agora autoriza a tabela:

```text
indirect_dispatch 9b04 32 ptrtail targets:9c59,9b97,...,9c59
```

O `dispatch_oob` nesse site desapareceu do C gerado. O grafo ficou **856
nós / 771 AOT / 85 LLE**; o AOT caiu de 784 porque os 32 destinos incluem
handlers LLE — a prioridade foi eliminar o trap, não inflar o número. O A/B
save9 ficou em **99,91% AOT** e **1,03–1,09s**; boot/título/save4/save9
passaram, zero stubs. O soak de 666k frames não foi repetido (leva horas); a
autorização estática remove o trap e o interpretador executa o dispatch real.

### Destravamento 9: contrato de `$03:A630`

`$03:A630` retorna **M1X0 nas duas variantes** (RTL em `$A7DC`, X limpo).
Contratos:

```text
exit_mx_variant 03A630 1 0 1 0
exit_mx_variant 03A630 1 1 1 0
```

Isso provou o retorno para `$03:983C`, que passou a AOT nas três variantes
(M0X1/M1X0/M1X1). O próprio `$03:A630` continua LLE porque chama
`$00:9077` e `$30:D226`. O grafo ficou **860 nós / 782 AOT / 78 LLE**; A/B
save9 em **99,91% AOT** e **1,02–1,03s**, zero stubs. Boot/título/save4/save9
passaram; título com os mesmos 6 bytes/SRAM/AE 2353/RMSE 30,29.

### Destravamento 10: bloco `$30` e a ponte `$00:9077`

Contratos de saída para `$00:9188`, `$00:947D`, `$00:9077`,
`$30:D226`/`D237`/`D4BF`/`8BF0`/`95CA`/`A20D`/`DD34`/`ECF4` (M1X0),
`$30:D586`/`$30:AFA0` (M0X0), `$05:96A0`, `$01:91DA` e `$02:AFB6`
(M0X0/M1X0), mais `noreturn_jsl b10e` para o `$02:DC53` terminal.

Resultado: `$00:9188`, `$00:947D`, `$00:9077` e `$30:D226` viraram AOT; o
grafo foi para **952 nós / 876 AOT / 76 LLE**. A/B save9 em **99,91% AOT** e
**~1,08s** (um trial inicial 1,27s), zero stubs; boot/título/save4/save9
válidos.

Ainda restam `$03:A630`, `$02:AFF9` e `$02:AFB6` com apenas
`truncated_call_continuation`: o analyzer não trata como terminal uma chamada
a um callee sem saída (por exemplo `$02:DC53` e o JSL `$03:A754`), mesmo com
`noreturn_jsl`. É um falso positivo de ferramenta; o próximo passo é corrigir
esse critério no analyzer.

### Destravamento 11: diagnóstico de chamada truncada

O analyzer passou a emitir a razão detalhada
`truncated_call_at_<site>_to_<alvo>`. Isso revelou dois bloqueios reais:

- `$03:A630` → `$03:A6BE` JSL `$01:8EAB`, que nunca retorna; adicionado
  `noreturn_jsl a6be`.
- `$02:AFF9`/`$02:AFB6` → `$02:B66A` JSL `$04:BE39`; o BRK em `$04:BEC6`
  era o terceiro byte de `LDA #$000B` no caminho M=0. Um
  `data_region 04 bec6 bec7` removeu o falso poison.

Resultado: `$03:A630`, `$02:AFF9`, `$02:AFB6` e `$04:BE39` viraram AOT. O
grafo foi para **1020 nós / 954 AOT / 66 LLE**. A/B save9 em **99,92% AOT** e
**1,05–1,11s** (trial 1 1,64s), zero stubs; boot/título/save4/save9 válidos.

### Destravamento 12: hub `$9A85` e `$94C3`

O `$00:9A85` é o hub de dispatch chamado por `$00:94C3` em três sites M1X1.
O contrato `exit_mx_variant 009A85 1 1 1 1` destravou os chamadores e elevou
o grafo para **1081 nós / 1019 AOT / 62 LLE**. Depois, o `$00:BF53`
(`exit_mx_set 00BF53 M0X0 M0X0,M1X1`) e o `noreturn_jsl 98b5` (`$00:80FB`
entra no main loop e não tem saída local) promoveram o `$00:94C3`, a função
de 616 instruções que o main loop chama.

Resultado final: **1081 nós / 1029 AOT / 52 LLE**. A/B save9 em **99,91%
AOT** e **1,03–1,12s**, zero stubs; boot/título/save4/save9 válidos; título
com os mesmos 6 bytes/SRAM/AE 2353/RMSE 30,29.

### Destravamento 13: handlers `$9A85`/`$A1D8`

`$00:A29D` é um `JSL $05:A718`; o `$05:A718` não tem **nenhuma** saída local
(é terminal). O `noreturn_jsl a29d` removeu o último truncamento dos handlers
`$9A85`/`$A1D8`, que passaram a AOT.

Resultado: **1081 nós / 1031 AOT / 50 LLE**. A/B save9 em **99,91% AOT** e
**1,03–1,04s**, zero stubs; boot/título/save4/save9 válidos.

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
**99,4–99,9% AOT / 0,1–0,6% interpretado**. O custo continua sendo duas
funções em LLE; o resto do grafo cresceu para 1031 variantes AOT com os
contratos de saída, as fronteiras `$04:BEC6`/`$05:E5DB`, o frame wait AOT,
o dispatch `$00:9B04` e os lotes do bloco `$30`/`$00:9077`, do hub
`$9A85`/`$94C3` e dos handlers `$9A85`/`$A1D8`.

O próximo passo de decompilação é **modelar esse dispatch vivo no emitter**
(ou declarar `indirect_dispatch` de forma que o link-closure aceite os 8+4
alvos), comparar o caminho com `snesref`/MesenCE e então re-promover as duas
funções. Uma tentativa inicial de `indirect_dispatch ... ptrtail targets:...`
elevou a análise para 131 variantes, mas o link-closure rejeitou 28 variantes
chamadas e não definidas; as diretivas foram revertidas.

## Fronteira atual: 50 nós LLE-only

Os 50 nós LLE-only (47 bases) restantes se distribuem em poucos clusters.
As razões são 58 `unproven_call`, 50 `truncated_call_continuation`, 50
`unproven_callee_exit` (mais 61 razões detalhadas `truncated_call_at_*`) e uma
aresta indireta:

| Cluster | Bases/variantes | Bloqueio |
|---|---|---|
| Main loop | `$00:8014`, `$00:80FB`, `$00:80FF` | nunca retornam; chamam `$05:8CB1`/`$00:94C3` |
| Texto/menus banco `$03` | `$03:9DBD`, `$03:AD87`, `$03:B3AB`, `$03:B43B` | chamadas não provadas |
| Helpers `$00`/`$01` | `$00:BF53`; `$01:91DA`, `$01:979C`, `$01:97C6`, `$01:986D`, `$01:99B8`, `$01:AE08`, `$01:EE96` | texto/input; maioria `unproven_call` |
| Banco `$05` | `$05:8CB1`, `$05:931F`, `$05:962D` | chamadas não provadas |
| Bloco `$30` | ~30 bases, incl. `$30:8BF0`, `$30:95CA`, `$30:A20D`, `$30:DD34`, `$30:ECF4`, `$30:D4BF`, `$30:D809`, `$30:BA74`–`$30:C15A` | som/gráficos; dispatcher `$0080AE` |

O main loop `$00:8014`/`$00:80FB`/`$00:80FF` continua LLE (nunca retorna). O
frame wait `$00:9397`, `$01:8EAB`, `$02:DBB7`, `$03:983C`, `$00:9077`,
`$00:9188`, `$00:947D`, `$03:A630`, `$02:AFF9`, `$02:AFB6`, `$04:BE39`,
`$00:94C3`, `$9A85` e `$A1D8` agora são AOT. O próximo foco é o bloco `$30`,
o cluster `$01:97C6`/`$01:986D` e o restante do banco `$03`; depois os sites
indiretos e a rota até o 6F.

### Histórico: o gargalo do `$03:983C`

Antes do frame wait AOT, o contrato `$03:983C` subia o grafo para **596 AOT**,
mas o `step 60` ia de 1,03s para **12,79s** (12,4x); o `interp_profile`
mostrava 35M ciclos em `$00:9300` e 5 `tier_hits`. Isso motivou o
`noreturn_jsl` e a promoção de `$00:9397`. Depois do frame wait AOT, o mesmo
contrato foi adotado: **784 AOT** e `step 60` em **1,04–1,06s**. A lição:
AOT% sozinho não basta; o harness de parede e o perfil interpretado dizem
onde está o gargalo.

O próximo passo de maior alavancagem é `$03:A630` (promove `$03:983C`),
depois `$02:DC53`/`$01:91DA` (promovem `$02:AFF9`/`$02:AFB6`) e o bloco
`$30`. Cada contrato passa por `save4`/`save9`/`snesref`/tempo de parede;
BRKs de caminho de erro pedem uma fronteira `data_region`, como `$05:E5DB`.

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

Na última execução antes dos contratos de saída, o probe emitiu **7/7
bancos** e 797 entradas de dispatch. Ele lista 31 sites indiretos sem tabela
declarada (o banco `$02` contribui `$02:DC74`):

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

1. Resolver o bloqueio `$05:A718` para promover `$9A85`/`$A1D8`, depois o
   bloco `$30` e o cluster `$01:97C6`/`$01:986D`. Cada mudança precisa de
   `save4`/`save9`, `snesref` e **tempo de parede**. Se a análise expuser
   outro `BRK` de caminho de erro, usar uma fronteira `data_region` como
   `$04:BEC6` ou `$05:E5DB`.
2. Modelar o `JMP ($0100)` dos dispatchers de HDMA no emitter, reativar
   `indirect_dispatch` com link-closure limpo e re-promover
   `$00:86C0`/`$00:88CE`.
3. Declarar as tabelas dos sites restantes `$01:C72B`/`CD9C`/`EF15`,
   `$02:DC74` e `$30:*` (ponteiro `$0080AE`); separar o caminho
   `brk_at_04BEC6` (`$04:BE39`) como código/dados.
4. Capturar uma rota mais longa (8F, 7F, 6F, menus, batalha, level-up),
   ingerir com `tier2_ingest.py` e adicionar os novos roots.
5. Nomear os placeholders `Coverage_*`, principalmente nos bancos `$30`,
   `$38` e `$3F`, e continuar a separação código/dados.
6. Manter gameplay, save states e comparação com emulador como regressão.
