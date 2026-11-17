# Fontes de pesquisa — Mikon City / Torre de Daedalus

Este documento registra o que foi extraído de cada fonte e as ressalvas. Nenhum
mapa, imagem, ROM ou save de terceiros é versionado no repositório.

## Fontes primárias

### 1. Pareido — tabela derivada do ROM

- URL: <https://pareido.jp/cyber-newtown/megaten-daedalus/nam-mt-dg-0/>
- Conteúdo extraído:
  - tabela de eventos do 8F e 7F (coordenadas Atlas, tipo, direção de entrada);
  - componentes conectados de cada andar (8F = 64 células; 7F = 54 + 9);
  - conexão 8F `(3,3)` → 7F `(11,3)`;
  - flag de parada do elevador do 7F = 0;
  - tabelas de encontros 8F–5F e 4F–1F;
  - estoque e preços da loja do 8F;
  - baú do 8F: 500 Macca + 宝玉.
- Ressalva: a tabela não lista batalhas fixas no 7F. O detonado e o mapa da
  Sion listam Basim e Gnome como encontros não aleatórios no 7F; os tiles
  exatos ainda não foram confirmados.

### 2. Sion’s Runs — rota de speedrun (SNES)

- URL: <https://sioneus.me/notes/kmt1>
- Conteúdo extraído:
  - rota do 8F em anel até o bloco central;
  - recomendação de comprar Jack Knife, Nunchaku e Combat Suits;
  - 7F: Basim e Gnome como encontros fixos; evitar Zombie no início;
  - Heket é recrutável apenas no 7F.
- Ressalva: as notas são de speedrun; algumas indicações de “tile de encontro
  fixo” não têm coordenada explícita.

### 3. GameFAQs 54063 — tradução/detonado (SNES)

- URL: <https://gamefaqs.gamespot.com/snes/581301-kyuuyaku-megami-tensei/faqs/54063?print=1>
- Conteúdo extraído:
  - 8F é Mikon City, sem encontros aleatórios;
  - Gate Keeper (homem de roupas Viking): aviso sobre a sala dos demônios;
  - “head pass the Viking and go down the stairs to the 7th floor”;
  - elevador indisponível neste ponto;
  - 7F: batalhas não aleatórias contra Basim e Gnome;
  - 7F 2ª seção: batalha não aleatória contra Dryad.
- Ressalva: é uma tradução; o texto em japonês do Gate Keeper pode diferir.

### 4. Mapas da comunidade (FC/NES e auto-map SNES)

- Aruto: <https://aruto.info/dds/dds1/map1.html>
- Grappli: <https://grappli.net/strategy/megamitensei1/story-daidaros-kouryaku/>
- Opatil (mapas SNES): <https://dds.opatil.com/kmt1/story/c01.html>
- Conteúdo extraído:
  - topologia do 8F: anel externo, bloco central, sala da escada `▼`, gate `門`,
    loja, elevador, catedral;
  - posição relativa da escada, do elder e da fonte;
  - o auto-map SNES do opatil mostra o marcador do jogador sobre o ícone cinza
    da escada, com o ícone de mensagem/Gate Keeper logo acima, e a fonte azul
    à direita; a fileira inferior tem baú, armadura, arma, EV e mensagens;
  - o 7F do opatil confirma Basim, Gnome e Dryad como encontros fixos.
- Ressalva: os mapas do aruto/grappli são da versão FC; o do opatil é o
  auto-map da versão SNES. Use-os para topologia, não para coordenadas locais
  de WRAM.

### 5. Tabela de RAM / cheats públicos

- `docs/ram-map.md`
- Endereços usados: dinheiro `0x0C72`–`0x0C74`, magnetita `0x0C75`–`0x0C76`,
  HP/stats da party `0x0D04`+.
- Novos endereços observados nesta rodada:
  - `0x877` = x local/global;
  - `0x878` = y local/global;
  - `0x80F` = direção (0=N, 1=E, 2=S, 3=W);
  - `0x811` = contador de movimento para frente;
  - `0x813` = contador de giro;
  - `0x865` = área/sala (01/02/03 observados);
  - `0x867` = background/view dependente da direção.
- Ressalva: `0x80F`/`0x811` **não** são coordenadas x/y. O modelo antigo de BFS
  que os tratava como coordenadas estava errado.

## O que foi validado no jogo

- O baú do 8F foi aberto: 500 Macca + 宝玉; o dinheiro foi confirmado em
  `0x0C72` = 500.
- O elder foi encontrado; o diálogo é multi-página e oferece
  `記録する` / `外に出る` e quatro slots de save.
- A placa `RAIFURU` (loja de armas) foi vista no bloco central.
- O velho de verde (mensagem “みな元気じゃな”) e a chama azul (dica sobre recrutar
  demônios) foram encontrados.
- A escada para o 7F ainda **não** foi alcançada; a primeira batalha continua
  pendente.

## Próximos passos de pesquisa

1. Mapear o grafo de salas/áreas do 8F usando `0x865` + `0x877`/`0x878` e o
   auto-map local.
2. Identificar o Gate Keeper pelo diálogo, testando os talks `(3,2)` e `(4,3)`
   a partir das direções de entrada corretas.
3. Encontrar a sala da escada `▼` e descer para 7F `(11,3)`.
4. Validar a primeira batalha no 7F (Basim/Gnome fixos ou encontro aleatório),
   com screenshots e resultado.
