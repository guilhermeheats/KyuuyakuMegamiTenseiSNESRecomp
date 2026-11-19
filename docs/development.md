# Desenvolvimento

Este documento reúne o ambiente usado, o estado atual, as ferramentas e o
fluxo de teste. Para o diário cronológico, veja `docs/bring-up-log.md`.

## Estado atual

Atualizado em 2026-11-18.

| Etapa | Estado |
|---|---|
| ROM japonesa limpa verificada | OK — CRC32 `c8d286c9` |
| Scaffold do snesrecomp | OK — 4 roots iniciais |
| Cobertura estática atual | OK — 72 roots, 12 bancos |
| Build nativo | OK — build-debug e release |
| Boot / tela de título | OK |
| Introdução do MT1 | OK |
| Nome do protagonista e da Yumiko | OK |
| Distribuição de status | OK |
| Primeira dungeon | OK |
| Movimento | OK |
| Interação com baú | OK — loot `500` + `宝玉` |
| Menu de status | OK — COMP/MAGIC/ITEM/STATUS e ficha |
| Auto-mapping | OK — mapa da dungeon pelo menu COMP |
| Primeira batalha | OK — Heket, Mad Slug, Basim fixo, negociação, game over, vitória/EXP/level-up |
| Save/load via SRAM do jogo | OK — gravação, flush, boot e reload |
| Cobertura estática | 1229 variantes AOT, 12 bancos; 99,4–99,9% AOT no save4/save9 |
| Comparação de referência | OK no título via snesref; MesenCE pendente |

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

A primeira comparação com referência externa foi feita com o **snesref**
(Snes9x libretro): no frame 3660, a WRAM do título difere em apenas 6 bytes
(animação/stack) e a SRAM é idêntica. O MesenCE 2.2.1 Linux foi baixado, mas
o binário não reconheceu `--testRunner` (abriu a GUI e falhou em
`XOpenDisplay`); a comparação com MesenCE fica pendente de um build com test
runner funcional. Detalhes e comandos em `docs/reference-comparison.md`.

## Limitações conhecidas

- O menu de status, o auto-mapping, os encontros de batalha, a negociação, o
  game over, a vitória/EXP/level-up e a alocação de `BONUS` já foram
  validados. A vitória/level-up foi obtida com boost de debug e também em
  **dificuldade normal** contra `妖魔ヘケット` (64 EXP, 20 Macca, 1 `宝玉`,
  Nakajima LV3), usando Jack Knife + Combat Suits. A tela de bônus limita os
  atributos a 35 (0x23); com o boost em 99, era preciso reduzir o atributo
  para 0x20 para alocar. Yumiko morreu na luta normal (0/9, `DEAD`) e o
  `宝玉` não a revive. O HUD de batalha exibiu `997/997`/`999/999` sem
  correspondência na WRAM — candidato a bug de exibição.
- O **Basim fixo** do 7F foi confirmado em `(9,3)` → leste: `何かが潜んで
  いた！` → `怪獣バシムが現れた！`. A batalha foi vencida com stats de debug
  no build AOT (30 EXP, 18 Macca, 6 MAG, 1 `宝玉`; Nakajima e Yumiko LV3).
  O tile não dá loot extra (`が、何もなかった`) e a rota do 6F a partir
  desse lado ainda não está mapeada. Gnome/Dryad continuam pendentes.
- A rota do 8F está confirmada em `docs/route-8f.md`: Gate Keeper em `(2,2)`,
  escada em `(2,3)` e chegada ao 7F em `(10,2)`.
- O servidor de debug funciona e `0x877`/`0x878`/`0x865` dão a posição; a
  grade do mapa ainda não está totalmente mapeada para o 7F.
- O save real (SRAM de 8 KiB) foi validado de ponta a ponta (CP-013):
  gravação, flush, boot e load pelo título. Save states antigos podem
  restaurar SRAM zerada; o `save1` foi regenerado com a SRAM válida.
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
O save AOT produziu o mesmo hash de SRAM do save LLE e o load pelo título foi
validado no boot natural. O antigo `save1` restaurava SRAM zerada e mascarava
o load; ele foi regenerado com a SRAM válida.

Na segunda rodada foram nomeadas as rotinas da tela de level-up:
`LevelUp_Apply` (`$01:B3C6`) e `LevelUp_PrintStat` (`$01:B5D5`), ambas com
`entry_m = 1`, `entry_x = 1`. O analyzer gerou 11 roots, 54 variantes
AOT-eligible e 6 LLE-only. `LevelUp_Apply` ficou **LLE-only** (todas as
variantes continuam no interpretador), enquanto `LevelUp_PrintStat_M1X1` foi
emitida em AOT. O fluxo completo foi testado a partir do `save11` no build
AOT: alocação de Nakajima e Yumiko, `YES`/`NO`, `ユミコは魔法を憶えた` e
retorno à dungeon (HP 26/26 e 27/27), sem crash. O estado resultante está no
`save2`.

### Cobertura estática (2026-11-18)

A captura tier-2 do boot/título e dos save states de 8F/7F/batalha/level-up
foi ingerida com `tier2_ingest.py`; os PCs quentes foram promovidos a roots
permanentes. Com `tools/regen.sh` usando `--cfg-roots` por padrão, o grafo
passou de **11 roots / 54 variantes AOT / 8 bancos** para **72 roots / 1229
variantes AOT / 12 bancos** (1229 variantes exatas, 0 LLE-only). Na rota
longa, o build ficou em **~94,7% AOT / 5,3% interpretado**, com zero dispatch
misses; nos testes frescos, **save4 99,80% AOT** e **save9 99,91% AOT**, com
zero stubs. O relatório completo, comandos e a lista de roots está em
`docs/coverage.md`.

O primeiro salto veio do contrato de saída de `$00:9397`: a rotina empilha
`PHP` e restaura com `PLP`/`PLX`, então a largura de saída espelha a de
entrada. As quatro diretivas `exit_mx_variant 009397 ...` provaram o retorno
para todos os chamadores e destravaram a análise pós-chamada que antes parava
em `unproven_callee_exit`; isso promoveu `$02:B0B6` e `LevelUp_Apply`. O
`$02:B0B6` também ganhou uma fronteira explícita
(`func Clamp_024E_TierWait b0b6 end:b0fa entry_mx:1,1`) e `force_variant_at`
nos dois call sites; o overrun do `v2_regen` era uma variante fantasma M0X1,
não dados lidos como código.

O segundo salto veio do contrato de `$02:AFF9`, que também preserva M/X. Ao
continuar a análise depois do `JSL $02AFF9` em `$05:D731`, o decoder chegou
ao caminho M=1 de erro em `$05:E556 JMP $E5D9` e leu o terceiro byte do
imediato `LDA #$0001` como `BRK` em `$05:E5DB`. Como o analyzer trata
qualquer BRK como `structural_poison` e descarta todas as demandas do nó, o
SCC inteiro caía de 590 para 153 nós. A fronteira
`data_region 05 e5db e5dc` em `recomp/bank05.cfg` marca só esse byte como
não-código e preserva o caminho M=0 válido em `$E5DC`. O resultado foi o
grafo de 511 variantes AOT.

O terceiro contrato foi `$01:8613` (`018613`), que também preserva P/X. Ele
destravou `$02:D13B` e outros chamadores sem tocar no caminho de menu do
983C. O A/B de `step 60` no save9 ficou em **1,03–1,04s** (o mesmo tempo do
baseline 511) e 99,89% AOT; o grafo subiu para **614 nós / 529 AOT / 85
LLE**. O contrato de `$03:983C` foi testado e **rejeitado**: sobe para 596
AOT, mas o `step 60` passa de 1,03s para 12,79s porque o frame wait
`$00:9300` vira o gargalo interpretado (detalhes em `docs/coverage.md`).

O quarto lote foi o cluster `$03:E91A`/`$03:E9B1`: contratos para E91A (M1X0),
E9B1 (M1X1) e as folhas EAEE/EAFA/F415 (M0X0). O grafo ficou em **615 nós /
532 AOT / 83 LLE**; o `step 60` continuou em 1,03–1,04s, com zero stubs.

O quinto lote fechou o cluster `$03:EB06`/`$03:EEE4`/`$03:80CA` e adicionou a
variante que faltava em `$02:AFF9`: `exit_mx_variant 02AFF9 0 0 0 0`. Essa
linha promoveu `$03:EEE4` e abriu 71 nós; o grafo foi para **690 nós / 603
AOT / 87 LLE**. O A/B ficou em 99,90–99,91% AOT e 1,06–1,09s (3–5% acima do
baseline), zero stubs; `save4` em 99,80% e título idêntico.

O sexto lote fechou `$03:8834` e os helpers `$00:90EB`/`$00:F160`, promovendo
`$03:80CA` e `$03:F415`: **700 nós / 616 AOT / 84 LLE**, A/B em 99,91% AOT
e 1,05–1,06s, zero stubs. Os próprios helpers continuam LLE com apenas
`truncated_call_continuation`.

O sétimo lote atacou o frame wait. O `$01:8EAB` tem um `JSL $00:8014` em
`$8EBE`; `$00:8014` é o main loop e nunca retorna. A ferramenta ganhou
`terminal_jsl`/`noreturn_jsl` e o cfg declara `noreturn_jsl 8ebe` (bank01) e
`noreturn_jsl 93b4` (bank00). Um atalho anterior com
`exit_mx_variant 018EAB` promoveu `$9397`, mas quebrou o boot; o
`noreturn_jsl` correto manteve o caminho de init terminal e o boot passou.
Com `$9397` AOT, o `$03:983C` deixou de ser lento e foi adotado: **849 nós /
784 AOT / 65 LLE**, save9 99,91%, save4 99,80%, boot/título/save4/save9
validados, zero stubs.

O oitavo lote corrigiu um crash de soak longo: no frame 666.606 o título
entrou no dispatch `$00:9B04` (`JMP ($0000)` com tabela de 32 palavras em
`$9B08`), o `dispatch_oob` disparou e o processo abortou. O cfg agora declara
`indirect_dispatch 9b04 32 ptrtail targets:...`; o trap sumiu do C gerado. O
grafo ficou **856 nós / 771 AOT / 85 LLE** (o AOT caiu porque os handlers
novos incluem LLE), A/B 99,91% e 1,03–1,09s, boot/título/save4/save9 válidos,
zero stubs.

O nono lote declarou a saída de `$03:A630`: ambas as variantes retornam M1X0,
o que provou o retorno do `$03:983C` e o promoveu nas três variantes. O grafo
foi para **860 nós / 782 AOT / 78 LLE**; A/B em 99,91% e 1,02–1,03s, zero
stubs; boot/título/save4/save9 válidos.

O décimo lote atacou o bloco `$30` e a ponte `$00:9077`: contratos para
`$00:9188`/`$00:947D`/`$00:9077`, as folhas do banco `$30`,
`$05:96A0`, `$01:91DA` e `$02:AFB6` (M0X0/M1X0), mais `noreturn_jsl b10e`
para o `$02:DC53` terminal. Isso promoveu `$00:9188`, `$00:947D`,
`$00:9077` e `$30:D226`: **952 nós / 876 AOT / 76 LLE**, A/B 99,91% e
~1,08s (um trial 1,27s), zero stubs. `$03:A630`, `$02:AFF9` e `$02:AFB6`
ficaram com apenas `truncated_call_continuation` — um falso positivo do
analyzer para chamadas a callees sem saída.

O décimo primeiro lote adicionou a razão detalhada
`truncated_call_at_<site>_to_<alvo>` ao analyzer. Isso revelou que
`$03:A630` chamava `$01:8EAB` em `$A6BE` (sem retorno) e que
`$02:AFF9`/`$02:AFB6` chamavam `$04:BE39` em `$B66A`; o BRK em `$04:BEC6`
era o terceiro byte de `LDA #$000B` no caminho M=0. Com
`noreturn_jsl a6be` e `data_region 04 bec6 bec7`, `$03:A630`, `$02:AFF9`,
`$02:AFB6` e `$04:BE39` viraram AOT: **1020 nós / 954 AOT / 66 LLE**, A/B
99,92%, zero stubs, boot/título/save4/save9 válidos.

O décimo segundo lote atacou o hub `$00:9A85` e o `$00:94C3`. O contrato
`exit_mx_variant 009A85 1 1 1 1` elevou o grafo para 1081/1019/62; depois
`exit_mx_set 00BF53 M0X0 M0X0,M1X1` e `noreturn_jsl 98b5` (o `$00:80FB`
entra no main loop e não tem saída local) promoveram o `$00:94C3`.
Resultado: **1081 nós / 1029 AOT / 52 LLE**, A/B 99,91% e 1,03–1,12s, zero
stubs, boot/título/save4/save9 válidos.

O décimo terceiro lote fechou os handlers `$9A85`/`$A1D8`: o `$00:A29D` é
um `JSL $05:A718`, que não tem nenhuma saída local (terminal). O
`noreturn_jsl a29d` removeu o último truncamento e os dois handlers viraram
AOT: **1081 nós / 1031 AOT / 50 LLE**, A/B 99,91% e 1,03–1,04s, zero stubs.

O décimo quarto lote atacou o bloco `$30` (som/gráficos). A cadeia converge
em três hubs: `$30:8770` (M0X0→M0X0) e `$30:C13B`/`$30:F424` (M1X1→M1X1).
Com `exit_mx_variant 308770 0 0 0 0`, `30C13B 1 1 1 1` e `30F424 1 1 1 1`,
os handlers foram promovidos em cascata: **1219 nós / 1197 AOT / 22 LLE**,
A/B 99,91% e 1,03s. Depois, `exit_mx_variant 30877B 1 0 1 0` fechou o
`$30:8770` e o bloco `$30` ficou 100% AOT: **1219 nós / 1198 AOT / 21 LLE**,
A/B 99,90–99,91% e 1,03–1,06s, zero stubs.

O décimo quinto lote fechou a cadeia do banco `$03`. O detalhe que faltava
era a entrada **M0X1** do frame wait `$03:983C`, usada por `$03:B43B` e
`$01:AE08`: `exit_mx_variant 03983C 0 1 0 1`. Com os contratos de
`$03:9DBD` (M0X0/M1X0), `$03:AD87`, `$03:B3AB` e `$03:B43B`, a cadeia
inteira foi promovida e destravou de cascata o cluster `$01` e o
`$00:BF53`: **1228 nós / 1222 AOT / 6 LLE**, A/B 99,90–99,91% e
1,03–1,04s, zero stubs.

O décimo sexto lote fechou a fase 1. O `$01:91DA` M1X1 tem duas saídas
reais: RTL `$01:9797` em M1X1 e o caminho de cauda `$01:9582`/`$01:9677`
→ `$01:9798` → RTS `$01:97C5` em M1X0. O contrato
`exit_mx_set 0191DA M1X1 M1X0,M1X1` promoveu `$05:931F`, `$05:962D` e
`$05:8CB1`; depois, `exit_mx_variant 0094C3 1 0 1 1` fechou o `$00:94C3`
M1X0 e o main loop. Resultado: **1229 nós / 1229 AOT / 0 LLE-only**, A/B
99,91% e 1,033–1,036s, zero stubs; campo (`save2`) com 12 mil frames e zero
off-rails/stubs. Restam 4 `force_lle` intencionais (reset, NMI e dois HDMA).
O mapa de bytes do ROM está em `docs/rom-coverage.md`.

O regen também recebeu `--profile-manifest`, `--no-host-root-scan` e um
`funcs.h` temporário fora da raiz do projeto; sem isso o scanner readicionava
declarações antigas e o link-closure falhava com 28 variantes pendentes.

O suporte a `terminal_jsl`/`noreturn_jsl` é um patch local do submódulo
`snesrecomp`, porque ele aponta para o upstream público. O delta está em
`patches/snesrecomp-noreturn-jsl.patch` e é aplicado por
`tools/apply-snesrecomp-patch.sh`; o regen precisa de `~/.cargo/bin` no
`PATH` para reconstruir o analisador nativo.

Os dois dispatchers de HDMA (`$00:86C0`/`$00:88CE`) foram mantidos em
**LLE** (`force_lle 0086C0`/`force_lle 0088CE`) porque o emitter ainda não
materializa o `JMP ($0100)` com alvo vivo; o `unresolved_stub_get` fica zero
e o custo é duas funções em LLE. O próximo passo de decompilação é modelar
esse dispatch no emitter, reativar `indirect_dispatch` com link-closure
limpo e re-promover as duas funções.

## Próximos passos

1. Declarar as tabelas indiretas `$01:C72B`→`$C74E`,
   `$01:CD9C`→`$CDB6`, `$01:EF15`→`$ED47` e `$02:DC74`→`$DC35`; validar
   counts/alvos e remover a borda LLE do `$01:EE96`.
2. Resolver os HDMA `$00:86C0`/`$00:88CE` com as tabelas `$86FE`/`$88EC`
   via `ptrtail targets:` e remover `force_lle`; validar título/framebuffer.
3. Confirmar o ponteiro `$0080AE` dos sites `$30:*`; se for `$00:A220`,
   declarar o alvo único e validar o som.
4. Investigar o caminho LLE quente `$00:9300` no campo e reduzir o
   `force_lle`/interpretação da NMI/PPU/APU.
5. Capturar uma rota mais longa (8F, 7F, 6F, menus, batalha, level-up),
   ingerir com `tier2_ingest.py` e adicionar os novos roots.
6. Nomear os placeholders `Coverage_*`, principalmente nos bancos `$30`,
   `$38` e `$3F`, e continuar a separação código/dados.
7. Manter gameplay, save states e comparação com emulador como regressão.
