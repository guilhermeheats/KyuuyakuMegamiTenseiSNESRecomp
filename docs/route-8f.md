# Rota do 8F — Mikon City

> **Correção importante:** o 8F é **Mikon City**, uma cidade segura, com lojas,
> Healing Spring, House of Heresy, o elder/password e o baú de 500 Macca.
> **Não existem batalhas aleatórias no 8F.** A primeira batalha acontece no
> **7F**; o objetivo aqui é encontrar o Viking/Gate Keeper e descer as escadas.
> O elevador não pode ser usado neste ponto.
>
> **Status (2026-11-17): rota confirmada e primeira batalha validada no 7F.**
> O Gate Keeper é o demônio azul de cajado em `(2,2)`. A escada fica na sala
> seguinte, em `(2,3)`, e desce para o 7F em `(10,2)` nas coordenadas de WRAM
> (Atlas `(11,3)`).

## Rota confirmada (save10, com equipamento)

O `save10` começa em `(1,4)`, virado para o norte, com Jack Knife, Nunchaku e
dois Combat Suits. A rota validada foi:

```text
(1,4) --E×3--> (4,4) --N×4--> (4,0) --W×2--> (2,0) --S×2--> (2,2)
```

Passo a passo:

1. virar para **leste** e andar 3 células até `(4,4)`;
2. virar para **norte** e andar 4 células até `(4,0)`;
3. virar para **oeste** e andar 2 células até `(2,0)`;
4. virar para **sul** e andar 2 células: `(2,1)` e depois `(2,2)`.

Em `(2,2)`, o demônio azul do Gate Keeper aparece no vão escuro e diz:

```text
おい、坊主！
ここから先は魔物の棲み家だぜ！
行くことは言わないが
気をつけてな
```

Depois de fechar o diálogo com `A`, continuar para **sul** até `(2,3)`.
Aparece a pergunta `階段を降りますか？` com `YES`/`NO`; escolher `YES` desce
para o **7F**, com o HUD mostrando `7F`, em `(10,2)` virado para o norte.

> **Atenção:** `A` no dungeon abre o menu `COMP`/`MAGIC`/`ITEM`/`STATUS`.
> Use `B` para fechar os menus; não pressione `A` repetidamente depois que o
> diálogo terminar. O velho de verde em `(3,3)` (“みな元気じゃな”) é um NPC de
> mensagem e **não** é o Gate Keeper nem a escada.

### Rota curta (save5, sem equipamento)

Para confirmar apenas o Gate Keeper, o `save5` começa em `(0,0)`:

```text
(0,0) --E--> (1,0) --E--> (2,0) --S--> (2,1) --S--> (2,2)
```

O trecho `(0,0) → (2,0)` já estava validado; `(2,0) → (2,1) → (2,2)` é a
entrada do bloco central pelo corredor superior. O `save5` não serve para a
batalha porque não tem equipamento.

## Dados exatos do 8F (tabela derivada do ROM)

Fonte: <https://pareido.jp/cyber-newtown/megaten-daedalus/nam-mt-dg-0/>

As coordenadas da tabela são **Atlas/ROM (1-based)**. As coordenadas de WRAM
`0x877`/`0x878` são **0-based**; para células walkable, `WRAM = Atlas - 1` nos
dois eixos. Objetos em paredes/portas podem ser acionados da célula adjacente,
por isso a célula de evento nem sempre é a célula onde o jogador está.

| Célula (Atlas) | Evento | Entrada | Observação |
|---|---|---|---|
| `(7,0)` | 邪教の館 / Cathedral of Shadows | — | canto superior direito |
| `(4,1)` | 回復の泉 / Healing Spring | — | |
| `(3,2)` | Conversa | sul | objeto do Gate Keeper; o jogador fica em `(2,2)` (WRAM) |
| `(1,3)` | 長老 / Elder | norte | save/password |
| `(3,3)` | **Escada de descida** | — | objeto na sala `(2,3)` (WRAM) → 7F `(11,3)` (Atlas) / `(10,2)` (WRAM) |
| `(4,3)` | Conversa | sul | talk do bloco central; não é o Gate Keeper |
| `(1,5)` | Baú | norte | 500 Macca + 宝玉 |
| `(2,5)` | Conversa | norte | fileira das lojas |
| `(3,5)` | Conversa | norte | fileira das lojas |
| `(4,5)` | Loja | — | armas + armaduras |
| `(5,5)` | Elevador | — | não usar agora |

O 8F tem 64 células conectadas. A escada `(3,3)` leva ao 7F `(11,3)`.

## O que já foi validado no jogo

- O baú do 8F foi aberto; o diálogo mostrou “500と「宝玉」を手に入れた” e o
  dinheiro em `0x0C72` passou a 500.
- O elder foi encontrado em `(1,3)`; o diálogo é multi-página e termina em
  `記録する` / `外に出る`, com quatro slots de save.
- A placa `RAIFURU` (loja de armas) foi vista no bloco central.
- O velho de verde (mensagem “みな元気じゃな”) e a chama azul (dica sobre
  recrutar demônios) foram encontrados. O velho fica em `(3,3)` e empurra o
  jogador de volta para `(3,2)`; ele não é a escada.
- O auto-map foi aberto por `A` → `COMP` → `オートマッピング`
  (5º item; descer 4 vezes) e é um minimapa local rotacionado pela direção.
- A **loja de armaduras** foi encontrada em `(1,5)`; foram comprados 2
  Combat Suits (280 Macca).
- A **loja de armas** foi encontrada em `(2,5)`; foram comprados Jack Knife
  (80) e Nunchaku (130). Total gasto: 490; restam 10 Macca.
- O **elevador** em `(3,5)` mostra “邪悪な力により エレベーターは停止している”
  (parado por um poder maligno), confirmando que não pode ser usado agora.
- A tela de status/equipamento abre com **X**; a página `EQUIPMENTS` é acessada
  com **direita**. O inventário contém Jack Knife, Nunchaku e 2 Combat Suits.
- O auto-map foi colocado em **`Fixed`** por
  `A → COMP → コンフィグ → オートマッピング → こてい`. O mapa fica norte para
  cima e mostra a posição atual em vermelho, o elevador (`E`), a catedral
  (`J`) e a fonte (`K`); a escada (`D`) aparece quando o trecho é explorado.
- O **Gate Keeper** verdadeiro é o **demônio azul de cajado no vão escuro**
  em `(2,2)`, com o diálogo “おい、坊主！…”. O velho de verde em `(3,3)` que
  diz “みな元気じゃな” é uma mensagem, não o Gate Keeper.
- A **escada** foi acionada em `(2,3)`, na sala imediatamente ao sul do Gate
  Keeper. A pergunta `階段を降りますか？` apareceu; `YES` levou ao 7F, com o HUD
  `7F` e WRAM `(10,2)`.
- A **primeira batalha** foi validada no 7F em `(8,2)` (WRAM), ao descer do
  corredor superior e entrar na sala. O encontro aleatório mostra
  `妖魔ヘケットが現れた！` e abre o menu de batalha
  `FIGHT`/`ESCAPE`/`TALK`/`AUTO`, com as ações
  `ATTACK`/`COMP`/`ITEM`/`DEFEND` por personagem e confirmação `YES`/`NO`.
- No combate, os ataques físicos causaram 0–1 de dano e o inimigo revidou com
  2–3 de dano. A negociação `TALK` → “わたしと対等に話すつもりか？” →
  `NO` → “はははっ、よく分かっているようだな” →
  “悪魔は満足そうに去っていった” encerrou a batalha em paz; o jogo voltou ao
  dungeon no 7F em `(8,2)`, com a party em 10/10 e 9/9.
- O caminho de **derrota/game over** também foi validado com `AUTO`: a party
  chegou a 0/10 e 0/9, apareceram `パーティーは敵に敗れて...` e
  `志半ばに力尽きた`, seguidos da cena do barco; o recomp não crashou.
- A **vitória/level-up** foi validada contra 2 Mad Slugs, com boost de debug
  (999 HP/99 stats): `外道マッドスラッグを倒した！`, **100 EXP**, **65 Macca**,
  **20 MAG** e `レベルアップ：ナカジマあああ` (LV 2, `BONUS 1`).
- A **alocação do bônus** também foi concluída: `Cima`/`Baixo` mudam a linha,
  `Direita`/`A` somam 1 e descontam o bônus, `Esquerda` reduz, e um diálogo
  `YES`/`NO` confirma. Nakajima recebeu 1 ponto e a tela passou para
  `レベルアップ：ユミコ`; ela recebeu 1 ponto, confirmou `YES` e o jogo
  mostrou `ユミコは魔法を憶えた`, voltando à dungeon com HP **30/30** e
  **27/27**. Yumiko ficou com `POISON`.
- O travamento anterior da tela de bônus era efeito do boost de debug: os
  atributos em 99 ficavam acima do teto de 0x23 (35) e iguais ao valor base.
  A tela os exibia limitados a 35 e `A`/`Direita` não somavam nada. Baixar o
  atributo selecionado para 0x20 destravou a alocação; o código da tela está
  em `$01:B4F6` (loop), `$01:B431` (desenho) e `$01:B5D5` (impressão/limite).
- **Vitória em dificuldade normal (2026-11-18):** sem boost de debug, contra
  `妖魔ヘケット` no 7F. Nakajima com Jack Knife + Combat Suit e Yumiko com
  Combat Suit; Nakajima causou 2–5 por golpe e Heket 1–3. Resultado:
  `妖魔ヘケットを倒した！`, **64 EXP**, **20 Macca** e **1 `宝玉`**;
  Nakajima foi de **LV1 para LV3** (HP 23/23, primeiro atributo 20→22) e
  recebeu `BONUS 1`. Yumiko morreu (0/9, `DEAD`) e o `宝玉` não a revive.
  O HUD de batalha mostrou `997/997` e `999/999` sem correspondência na
  WRAM (8/0 e 9/9); é candidato a bug de exibição.
- **Reprodução do encontro:** com `save8` e espera de 12 frames por passo,
  o nono passo em `(8,2)` trouxe Heket. Outros tempos trouxeram Mad Slug
  (W=6), besta verde (W=18) e outro demônio (W=20); o RNG de encontro
  depende do tempo entre passos.
- **Equipamento:** o caminho é `A` → `B` (duas vezes) → `ITEM` → `そうび`;
  a tela `EQUIPMENTS` mostra os slots HEAD/BODY/HAND/SWD/ARM e a lista de
  itens. O cursor é o sublinhado branco na lista; `A` equipa o item no slot
  compatível. O Jack Knife foi para SWD e os dois Combat Suits para BODY
  (Nakajima e Yumiko). O Nunchaku não apareceu para Yumiko; ela usa a arma
  padrão (HAND).

## 7F — primeira batalha

A tabela do ROM lista 7 eventos no 7F, em duas componentes:

- **#1 (54 células):** subida `(11,3)`, descida `(11,4)`, talks `(12,5)` e
  `(14,6)`;
- **#2 (9 células):** talks `(13,6)` e `(15,2)`, descida `(15,3)`.

A escada do 8F cai na componente #1. O elevador do 7F **não para** (flag 0).
O detonado e o mapa da Sion listam **batalhas não aleatórias contra Basim e
Gnome** no 7F. O primeiro encontro observado foi **aleatório**, com **Heket**
em `(8,2)` (WRAM). Um segundo encontro aleatório trouxe uma **besta verde
(provável Basim)** no mesmo trecho: `TALK` respondeu `グルルルルル...` e
`ESCAPE` falhou duas vezes, com 3 de dano em Nakajima.

**Basim fixo confirmado (2026-11-18):** a partir de WRAM `(9,3)`, tentar
andar para leste dispara `何かが潜んでいた！` →
`怪獣バシムが現れた！`, seguido de `怪獣バシムを倒した！`. A batalha foi
vencida com os stats de debug (99) no build AOT, não em dificuldade normal:
**30 EXP**, **18 Macca** (88→106), **6 MAG**, **1 `宝玉`**; Nakajima e
Yumiko chegaram a **LV3** (37/37 e 39/39) e receberam `BONUS 1`. Depois da
vitória, a mensagem `辺りを調べてみた・・・・ / が、何もなかった` confirma
que o tile não dá loot extra. Uma segunda tentativa de andar para leste foi
bloqueada sem mensagem; o gatilho do Gnome e a rota para a escada do 6F a
partir desse lado continuam pendentes.

Para repetir a validação, os save states locais são:

| Slot | Conteúdo |
|---|---|
| `save10` | 8F, `(1,4)`, equipado, 10 Macca |
| `save6` | 7F, `(8,2)`, pós-batalha de Heket, dungeon |
| `save8` | 7F, `(8,2)`, pré-batalha, full HP e equipado |
| `save0` | 7F, `(8,2)`, início da batalha contra Heket (LV1) |
| `save3` | pós-vitória normal contra Heket, Nakajima LV3, Yumiko `DEAD` |
| `save7` | pós-vitória normal contra Heket (cópia de segurança) |
| `save11` | tela `レベルアップ：ユミコ`, antes da alocação |
| `save2` | pré-Basim no build AOT, 7F, HP 26/26 e 27/27, Yumiko `POISON` |
| `save5` | início da batalha fixa contra `怪獣バシム` em `(9,3)` |
| `save4` | tela `レベルアップ：ナカジマあああ` após Basim, `BONUS 1` |
| `save9` | pós-Basim, 7F, Nakajima 37/37 e Yumiko 39/39, LV3, Yumiko `POISON` |

Esses saves são artefatos locais de `build-debug/saves/` e **não** são
versionados.

## O que ainda falta

- Reviver a Yumiko ou repetir a batalha com ela viva (o `宝玉` não revive;
  a opção `MAGIC` fora de batalha responde `魔法を使える者がいません`).
  O `DEFEND` de Yumiko evitou dano na rodada testada, mas a batalha foi
  encerrada por `ESCAPE` antes da vitória.
- Testar a sala `Kaifuku`/revival do 8F se houver caminho de volta, ou seguir
  para o 6F e procurar um ponto de cura/revival.
- Confirmar os gatilhos exatos de **Gnome** e **Dryad** no 7F; o **Basim
  fixo** foi confirmado em `(9,3)` (ver acima). A rota para a escada do 6F a
  partir desse lado ainda não está mapeada.
- Descer do 7F para o 6F e validar a continuação da torre. As tentativas a
  partir de `(8,2)`/`(9,1)` mudaram a área para `0x0002`/`0x0003` e foram
  bloqueadas, sugerindo portas de mão única; mapear com o auto-map antes de
  repetir.
- CP-013 concluído: gravação/flush e load pelo título validados. O antigo
  `save1` restaurava SRAM zerada e foi regenerado com a SRAM válida.
- Mapear o 7F e o 6F com o auto-map `Fixed` para as próximas batalhas.

## Modelo de movimento (corrigido)

O modelo antigo tratava `0x80F`/`0x811` como coordenadas x/y; isso estava
errado. Os endereços observados são:

| Endereço | Significado |
|---|---|
| `0x877` | x local/global |
| `0x878` | y local/global |
| `0x80F` | direção: `0`=N, `1`=E, `2`=S, `3`=W |
| `0x811` | contador de movimento para frente |
| `0x813` | contador de giro |
| `0x865` | área/sala (`01`/`02`/`03` observados) |
| `0x867` | background/view dependente da direção |

Controles observados: `up` = andar para frente; `left`/`right` = girar 90°;
`down` pode funcionar como giro de 180° em alguns estados. Use `up` para
movimento e `left`/`right` para orientação; evite `down` durante a navegação.

## Referências

- Tabela derivada do ROM:
  <https://pareido.jp/cyber-newtown/megaten-daedalus/nam-mt-dg-0/>
- Notas de rota (Sion): <https://sioneus.me/notes/kmt1/>
- Detonado/tradução (GameFAQs 54063):
  <https://gamefaqs.gamespot.com/snes/581301-kyuuyaku-megami-tensei/faqs/54063?print=1>
- Mapas da comunidade (FC/NES, topologia):
  <https://aruto.info/dds/dds1/map1.html> e
  <https://grappli.net/strategy/megamitensei1/story-daidaros-kouryaku/>
- Auto-map SNES do opatil (8F/7F):
  <https://dds.opatil.com/kmt1/story/c01.html>
- Sistema SNES (X=status, L=mapa, R=analisador, config Free/Fixed) e
  screenshot do Gate Keeper azul:
  <https://cielgrand.web.fc2.com/retrogame/ddsmegaten1.html>

Os mapas são material de terceiros e não foram copiados para o repositório.
