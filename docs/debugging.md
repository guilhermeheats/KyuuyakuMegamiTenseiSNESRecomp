# Debugging e rastreamento de WRAM

Este projeto pode ser compilado com o servidor TCP de debug do snesrecomp. É
um build separado, apenas para investigação; o build de release não o inclui.

## Build

```bash
cmake -S . -B build-debug -G Ninja \
  -DCMAKE_BUILD_TYPE=RelWithDebInfo \
  -DSNESRECOMP_ENABLE_TRACE=ON
cmake --build build-debug --parallel
```

`build-debug/` é ignorado pelo Git.

## Executar sem janela

```bash
SDL_VIDEODRIVER=dummy SDL_AUDIODRIVER=dummy \
  ./build-debug/KyuuyakuTen --no-launcher \
  "$HOME/roms/kyuuyaku.sfc"
```

O servidor escuta em `127.0.0.1:4377` por padrão. `SNESRECOMP_DEBUG_PORT`
permite outra porta.

## Cliente Python

O cliente fica no submódulo:

```python
import sys
sys.path.insert(0, "snesrecomp/tools")
from sneslib.client import DebugClient

c = DebugClient(4377, timeout=10)
print(c.query("ping"))
print(c.query("frame"))
```

Comandos úteis:

| Comando | Uso |
|---|---|
| `loadstate 5` | carrega o save state 5 |
| `step 30` | avança 30 frames com o jogo controlado |
| `set_controller up` | segura o direcional para cima |
| `clear_controller` | solta os botões |
| `read_ram 80f 8` | lê 8 bytes da WRAM |
| `write_ram 811 01` | escreve 1 byte na WRAM |
| `screenshot nome` | grava um BMP 256x224 |
| `frame` | mostra o frame atual |
| `get_v2_cpu` | estado da CPU |

As capturas de `screenshot` são gravadas no diretório de trabalho do host
(`build-debug/` quando ele é iniciado pela raiz do projeto).

## O que já foi descoberto

- `0x80f`, `0x811` e `0x813` mudam quando o jogador anda ou vira.
- `0x865`/`0x867` também mudam, mas os valores parecem identificadores de
  sala/tile (`0x41`, `0x0d`, `0x11`, `0x33`), não coordenadas simples.
- Escrever em `0x811` altera a visão renderizada, o que confirma que a região
  participa do estado de posição/câmera.
- Ainda não foi possível mapear com segurança o par de coordenadas para o mapa
  do 8F; escrever valores isolados pode renderizar corredores, mas não levou à
  escada `D` nem ao elevador `E`.

## Correção do modelo de movimento (2026-11-17)

A exploração desta rodada mostrou que `0x80F`/`0x811` **não** são um par x/y.
Os endereços observados são:

| Endereço | Significado |
|---|---|
| `0x877` | x local/global |
| `0x878` | y local/global |
| `0x80F` | direção: `0`=N, `1`=E, `2`=S, `3`=W |
| `0x811` | contador de movimento para frente |
| `0x813` | contador de giro |
| `0x865` | área/sala (`01`/`02`/`03` observados) |
| `0x867` | background/view dependente da direção |

Consequências:

- o BFS antigo tratava a direção como posição e por isso criava vários “nós”
  para a mesma célula;
- o wall follower antigo seguia o anel externo da cidade, não o bloco central;
- os IDs `0x11`, `0x31`, `0x05`, `0x51` etc. são **backgrounds por direção**,
  não um grafo de portas. As transições com A observadas nesses tiles precisam
  ser revalidadas com o modelo novo;
- `up` = andar para frente, `left`/`right` = girar 90°; `down` pode funcionar
  como giro de 180° em alguns estados. Para navegar, prefira `up` e
  `left`/`right` e evite `down`.

### Auto-map

O auto-map é um minimapa **local**. Ele tem dois modos, configuráveis em
`COMP → コンフィグ → オートマッピング`:

- `フリー` (Free): o mapa gira junto com a direção do jogador;
- `こてい` (Fixed): o mapa fica **norte para cima** e mostra a posição atual em
  vermelho, a escada de descida (`D`), a de subida (`U`), o elevador (`E`), a
  catedral (`J`) e a fonte (`K`).

O modo **Fixed** é o que deve ser usado para navegar; o modo Free foi o que
causou a confusão nas tentativas anteriores. Caminho do menu:

```text
A (menu) → COMP → down × 5 → A (config)
  → down × 2 → A (auto mapping)
  → selecionar こてい (Fixed)
```

O 5º item do submenu COMP é `オートマッピング`; o 6º é `コンフィグ`.
O mapa pode ser aberto pelo botão **L** (atalho) ou por `COMP` →
`オートマッピング`. O mapa não mostra a coordenada global; use
`0x877`/`0x878`/`0x865` para registrar a posição.

O **Gate Keeper** verdadeiro é o **demônio azul de cajado no vão escuro** em
`(2,2)` (fonte: Cielgrand, `ddsmegaten33.png`; diálogo confirmado no jogo em
2026-11-17). O velho de verde em `(3,3)` que repete “みな元気じゃな” é uma
mensagem/loja, não o Gate Keeper nem a escada.

A entrada do bloco central é pelo corredor superior, não pelo bloco do elder:
`(0,0) → (2,0) → (2,1) → (2,2)`. A escada fica na sala seguinte, `(2,3)`;
ao entrar, o jogo pergunta `階段を降りますか？` e `YES` desce ao 7F em
`(10,2)` (HUD `7F`).

### Âncoras validadas no 8F

- baú: aberto a partir da célula local `(0,5)`, com `0x878` = 5; loot 500 +
  宝玉, dinheiro `0x0C72` = 500;
- elder: diálogo multi-página em `(1,3)`, com `記録する` / `外に出る` e quatro
  slots de save;
- loja/placa `RAIFURU` e mensagem do velho de verde no bloco central;
- o Gate Keeper é o demônio azul em `(2,2)`; o diálogo “おい、坊主！…” foi
  confirmado entrando em `(2,2)` pelo norte (vindo de `(2,1)`);
- a escada foi acionada em `(2,3)`: `階段を降りますか？` → `YES` → 7F em
  `(10,2)`, com o HUD `7F`;
- o velho de verde em `(3,3)` repete “みな元気じゃな” e empurra o jogador para
  `(3,2)`; ele é uma mensagem/loja, não o Gate Keeper nem a escada;
- loja de armaduras em `(1,5)`: 2 Combat Suits; loja de armas em `(2,5)`:
  Jack Knife + Nunchaku; elevador em `(3,5)` parado (“邪悪な力により…”)；
- o menu de equipamento fica em **`ITEM → そうび`**, não em STATUS. Caminho:
  `A` abre a janela de comandos; `B` volta do submenu COMP para a lista;
  `↓` seleciona `ITEM`; `A`; `↓×3` até `そうび`; `A`. A tela `EQUIPMENTS`
  mostra HEAD/BODY/HAND/SWD/ARM e os itens (Jack Knife, Nunchaku,
  Combat Suit); o manual confirma que é preciso equipar explicitamente.

### Rota confirmada 8F → 7F (2026-11-17)

Rota usada com o `save10` (equipado, em `(1,4)`):

```text
E×3 → (4,4)
N×4 → (4,0)
W×2 → (2,0)
S×2 → (2,1) → (2,2)   # Gate Keeper
S   → (2,3)           # 階段を降りますか？ YES → 7F (10,2)
```

No 7F, o primeiro encontro foi **aleatório**, com Heket em `(8,2)` (WRAM),
ao descer do corredor superior e entrar na sala:

```text
(10,2) --W--> (9,2) --N--> (9,1) --W--> (8,1) --S--> (8,2)
妖魔ヘケットが現れた！
```

O menu de batalha é `FIGHT`/`ESCAPE`/`TALK`/`AUTO`; cada personagem escolhe
`ATTACK`/`COMP`/`ITEM`/`DEFEND` e o jogo pede confirmação `YES`/`NO`.
A negociação `TALK` → `わたしと対等に話すつもりか？` → `NO` →
`はははっ、よく分かっているようだな` →
`悪魔は満足そうに去っていった` encerra a batalha em paz e devolve o controle
ao dungeon em `(8,2)`. Um segundo encontro aleatório no mesmo trecho trouxe
uma besta verde (provável Basim): `TALK` respondeu `グルルルルル...` e
`ESCAPE` falhou duas vezes.

> **Cuidado com `A`/`B`:** no dungeon, `A` abre a janela de comandos; `B`
> volta do submenu para a lista de comandos e `B` de novo fecha. Para
> equipar: `A` → `B` → `↓` até `ITEM` → `A` → `↓×3` até `そうび` → `A`.

### SRAM e save/load (2026-11-17)

O caminho de save/load foi **validado**:

- o elder do 8F grava em quatro slots de `0x800` bytes, em `0x0000`,
  `0x0800`, `0x1000` e `0x1800`;
- cada slot começa com o header `DDSO` e tem um checksum em `slot+0x00EF`;
- a rotina de save em `$03:A35B` copia `$7E:0C00` → SRAM `0x0000` e
  `$7E:8000` → SRAM `0x0400`; a rotina de load em `$03:A3BF` faz o inverso;
- a gravação em disco acontece no shutdown (`RtlWriteSram`): o arquivo
  `saves/save.srm` (8192 bytes) ficou com 93 bytes não-zero e SHA-256
  `a0ca482fe5919969a94c51e9073d1b25527a05b06b273f56ec5493ca56aa100a`,
  idêntico à SRAM em memória;
- no boot seguinte, o arquivo foi relido e a SRAM em memória voltou com o
  mesmo hash;
- **boot natural** → título → `START`/`CONTINUE` → `CONTINUE`: a lista
  mostrou `0 ダイダロス L1 ナカジマあああ ユミコ`; selecionar e confirmar
  `ロードしますか？` carregou o jogo no 8F `(1,4)`, com 10 Macca, party
  10/10/9/9 e 6 MP;
- o checksum em `0x00EF` fica `0x00`; o jogo aceita o save assim mesmo.

> **Cuidado com save states:** o antigo `save1` restaurava uma SRAM zerada.
> Testes que faziam `loadstate 1` antes do `CONTINUE` viam
> `セーブされたデータがありません` e zeravam a SRAM. O `save1` foi regenerado
> no título com a SRAM válida. Para validar o load, faça boot natural com o
> `save.srm` ou use um save state capturado **depois** do save.

As cinco rotinas de SRAM foram promovidas para AOT (`emit = true`,
`entry_m = 1`, `entry_x = 0`): 14 variantes AOT, 0 LLE-only; o save AOT
produz o mesmo hash do save LLE.

## Exploração BFS (2026-11-17)

Foi feito um BFS de caminhos a partir do `save5`, recarregando o state e
repetindo o caminho antes de testar cada direção:

- profundidade 5, limite de 50 nós;
- screenshot de cada nó;
- assinatura lida em `0x80f` e `0x865`.

Resultado: o BFS encontrou muitos estados de **orientação** diferentes no mesmo
trecho, não novas salas. O caminho `up/up/up` a partir do `save5` abre o diálogo
do baú. Nenhum screenshot mostrou a escada `D`, o healer `H` ou o elevador `E`.

A assinatura incluía `0x813` (direção), o que inflou o número de nós. A próxima
iteração deve usar apenas posição/tile e ignorar a direção, além de comparar
com o mapa do 8F.

### Wall follower (2026-11-17)

Foi executado um wall follower left-hand a partir do `save5`, com 113 movimentos
e 89 rotações. Ele percorreu um ciclo fechado de tiles:

```text
0x11 → 0x33 → 0x51 → 0x31 → 0x05 → 0x11 → ...
```

Nenhum tile de escada, healer ou elevador apareceu. Conclusão: a componente
alcançável a partir do `save5` é um loop; a rota para a escada/elevador deve
exigir uma porta/evento ou outro ponto de entrada (por exemplo, o `save8` ou
uma interação com A em um tile específico).

### Interação com A nos tiles do loop

Foram testados os tiles `0x05`, `0x11`, `0x31`, `0x33` e `0x51`, em quatro
orientações cada:

- na maioria, A abre o menu normal (`COMP/MAGIC/ITEM/STATUS`);
- no tile `0x05`, com as orientações 0 e 1, A **não** abre o menu: o tile muda
  para `0x31` e a visão mostra uma parede/abertura. Isso sugere uma porta ou
  transição especial nesse tile;
- mesmo depois dessa transição, o wall follower continua no mesmo ciclo
  `0x11 → 0x33 → 0x51 → 0x31 → 0x05`.

A porta/transição do tile `0x05` é o próximo ponto a investigar com o mapa
do 8F e com A em sequências diferentes.

### Portas de Mikon City (A + direção)

O 8F é uma cidade, não uma dungeon. As transições de porta observadas com A
foram:

| Tile | A + direção | Destino |
|---|---|---|
| `0x41` (início) | face 0 | menu |
| `0x41` | face 1 | `0x11` |
| `0x41` | faces 2/3 | `0x31` |
| `0x31` | face 0 | menu |
| `0x31` | face 1 | `0x05` |
| `0x31` | faces 2/3 | `0x41` |
| `0x05` | faces 0/1 | `0x31` |
| `0x11` | faces 1/2 | `0x31` |
| `0x11` | face 3 | `0x05` |
| `0x51` | face 1 | `0x11` |
| `0x51` | faces 2/3 | `0x01` |
| `0x33` | face 1 | `0x31` |
| `0x35` | qualquer | menu |

Essas transições são portas/entradas de prédios, não escadas. O próximo alvo é
explorar o tile `0x01` e os demais destinos ainda não visitados.

### Save states entre builds

`loadstate 5` funciona no `build-debug`, mas `loadstate 13` carregou um estado
de introdução em vez do corredor. Os states `9`–`13` foram criados pelo build de
release e não são confiáveis no build de debug. Para o próximo BFS, gere os
states **dentro do próprio build-debug** (ou use `save_state`/`load_state` com
arquivos e valide o screenshot antes de explorar).

## Próximo uso

1. Carregar `save11` (chegada ao 7F) ou `save6` (pós-batalha) para continuar.
2. Usar o auto-map `Fixed` e `0x877`/`0x878`/`0x865` para mapear o 7F.
3. Confirmar as coordenadas/gatilhos de Basim, Gnome e Dryad e descer ao 6F.
4. Validar o início do Megami Tensei II (CP-014). Para testar save/load, faça
   boot natural com o `save.srm`; save states antigos podem restaurar SRAM
   zerada.

Não use `write_ram` em um save real; use sempre um save state descartável e
recarregue-o depois do teste.
