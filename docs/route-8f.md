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
  corredor superior e entrar na sala. O evento scripted mostra
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
- **Vitória** ainda pendente: os ataques físicos causam 0–1 e Yumiko não tem
  magia utilizável neste ponto (`使える魔法はありません`).

## 7F — primeira batalha

A tabela do ROM lista 7 eventos no 7F, em duas componentes:

- **#1 (54 células):** subida `(11,3)`, descida `(11,4)`, talks `(12,5)` e
  `(14,6)`;
- **#2 (9 células):** talks `(13,6)` e `(15,2)`, descida `(15,3)`.

A escada do 8F cai na componente #1. O elevador do 7F **não para** (flag 0).
O detonado e o mapa da Sion listam **batalhas não aleatórias contra Basim e
Gnome** no 7F; a tabela do ROM não as lista como eventos fixos. O primeiro
evento scripted observado nesta rodada foi **Heket** em `(8,2)` (WRAM), não
Basim/Gnome. O guia também recomenda recrutar Heket/Gnome; a negociação
respeitosa com Heket funcionou.

Para repetir a validação, os save states locais são:

| Slot | Conteúdo |
|---|---|
| `save10` | 8F, `(1,4)`, equipado, 10 Macca |
| `save11` | 7F, `(10,2)`, chegada da escada |
| `save9` | 7F, `(8,2)`, mensagem `妖魔ヘケットが現れた！` |
| `save8` | 7F, `(8,2)`, menu inicial da batalha (HP cheio) |
| `save7` | 7F, `(8,2)`, menu da batalha após o primeiro turno |
| `save6` | 7F, `(8,2)`, pós-batalha, dungeon |

Esses saves são artefatos locais de `build-debug/saves/` e **não** são
versionados.

## O que ainda falta

- Confirmar as coordenadas e os gatilhos exatos de Basim, Gnome e Dryad no 7F
  (o evento de Heket já foi confirmado em `(8,2)`).
- Descer do 7F para o 6F e validar a continuação da torre.
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
