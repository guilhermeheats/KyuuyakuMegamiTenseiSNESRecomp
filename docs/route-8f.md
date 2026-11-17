# Rota do 8F — Mikon City

> **Correção importante:** o 8F é **Mikon City**, uma cidade segura, com lojas,
> Healing Spring, House of Heresy, o elder/password e o baú de 500 Macca.
> **Não existem batalhas aleatórias no 8F.** A primeira batalha acontece no
> **7F**; o objetivo aqui é encontrar o Viking/Gate Keeper e descer as escadas.
> O elevador não pode ser usado neste ponto.

## Dados exatos do 8F (tabela derivada do ROM)

Fonte: <https://pareido.jp/cyber-newtown/megaten-daedalus/nam-mt-dg-0/>

| Célula | Evento | Entrada | Observação |
|---|---|---|---|
| `(7,0)` | 邪教の館 / Cathedral of Shadows | — | canto superior direito |
| `(4,1)` | 回復の泉 / Healing Spring | — | |
| `(3,2)` | Conversa | sul | **candidato a Gate Keeper** |
| `(1,3)` | 長老 / Elder | norte | save/password |
| `(3,3)` | **Escada de descida** | — | **→ 7F `(11,3)`** |
| `(4,3)` | Conversa | sul | **candidato a Gate Keeper** |
| `(1,5)` | Baú | norte | 500 Macca + 宝玉 |
| `(2,5)` | Conversa | norte | fileira das lojas |
| `(3,5)` | Conversa | norte | fileira das lojas |
| `(4,5)` | Loja | — | armas + armaduras |
| `(5,5)` | Elevador | — | não usar agora |

O 8F tem 64 células conectadas. A escada `(3,3)` leva ao 7F `(11,3)`.

## Rota da comunidade (anel)

A rota da Sion (<https://sioneus.me/notes/kmt1>) desenha um anel no 8F:

1. virar 180° no início;
2. seguir para o sul até o canto inferior esquerdo;
3. virar à esquerda e seguir para o leste pelo corredor inferior;
4. virar à esquerda e subir pelo corredor direito;
5. virar à esquerda e seguir para o oeste pelo corredor superior;
6. virar à esquerda e descer para o bloco central, onde ficam baú, elder,
   loja, fonte e a escada `(3,3)`.

O wall follower antigo percorreu o anel externo e não entrou no bloco central.
O auto-map local mostra as paredes, mas não a coordenada global.

## O que já foi validado no jogo

- O baú do 8F foi aberto; o diálogo mostrou “500と「宝玉」を手に入れた” e o
  dinheiro em `0x0C72` passou a 500.
- O elder foi encontrado; o diálogo é multi-página e termina em
  `記録する` / `外に出る`, com quatro slots de save.
- A placa `RAIFURU` (loja de armas) foi vista no bloco central.
- O velho de verde (mensagem “みな元気じゃな”) e a chama azul (dica sobre
  recrutar demônios) foram encontrados.
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

## O que ainda falta

- A escada para o 7F ainda **não** foi alcançada nesta rodada.
- O Gate Keeper ainda **não** foi confirmado; os candidatos são os talks
  `(3,2)` e `(4,3)`. O velho de verde em `(3,3)` é uma mensagem, não o aviso
  do Viking do detonado.
- A primeira batalha continua pendente.

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

## 7F — primeira batalha

A tabela do ROM lista 7 eventos no 7F, em duas componentes:

- **#1 (54 células):** subida `(11,3)`, descida `(11,4)`, talks `(12,5)` e
  `(14,6)`;
- **#2 (9 células):** talks `(13,6)` e `(15,2)`, descida `(15,3)`.

A escada do 8F cai na componente #1. O elevador do 7F **não para** (flag 0).
O detonado e o mapa da Sion listam **batalhas não aleatórias contra Basim e
Gnome** no 7F; a tabela do ROM não as lista como eventos fixos, então os tiles
exatos ainda precisam ser confirmados no jogo. Para o primeiro combate, evite
Zombie no início.

## Referências

- Tabela derivada do ROM:
  <https://pareido.jp/cyber-newtown/megaten-daedalus/nam-mt-dg-0/>
- Notas de rota (Sion): <https://sioneus.me/notes/kmt1/>
- Detonado/tradução (GameFAQs 54063):
  <https://gamefaqs.gamespot.com/snes/581301-kyuuyaku-megami-tensei/faqs/54063?print=1>
- Mapas da comunidade (FC/NES, topologia):
  <https://aruto.info/dds/dds1/map1.html> e
  <https://grappli.net/strategy/megamitensei1/story-daidaros-kouryaku/>

Os mapas são material de terceiros e não foram copiados para o repositório.
