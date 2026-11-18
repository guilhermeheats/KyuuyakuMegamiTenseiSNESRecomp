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
  exatos ainda não foram confirmados. No jogo, o primeiro encontro observado
  no 7F foi **aleatório**, com **Heket** em `(8,2)` (WRAM); uma besta verde
  (provável Basim) também apareceu aleatoriamente no mesmo trecho.

### 2. Sion’s Runs — rota de speedrun (SNES)

- URL: <https://sioneus.me/notes/kmt1>
- Conteúdo extraído:
  - rota do 8F em anel até o bloco central;
  - recomendação de comprar Jack Knife, Nunchaku e Combat Suits;
  - 7F: Basim e Gnome como encontros fixos; evitar Zombie no início;
  - Heket é recrutável apenas no 7F; no jogo, Heket apareceu como encontro
    aleatório em `(8,2)` (WRAM) e pôde ser dispensado pela opção `TALK` → `NO`.
  - Uma besta verde (provável Basim) também apareceu como encontro aleatório;
    `TALK` respondeu `グルルルルル...` e `ESCAPE` falhou duas vezes.
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

### 5. Cielgrand — sistema SNES

- URL: <https://cielgrand.web.fc2.com/retrogame/ddsmegaten1.html>
- Conteúdo extraído:
  - `X` abre o status; `L` abre o mapa; `R` abre o analisador de demônios;
  - o status tem 3 páginas; a página da direita é a de equipamento;
  - o auto-map é o efeito da magia マッパラー e mostra escada de descida (`D`),
    de subida (`U`), elevador (`E`), catedral (`J`), fonte (`K`) e a posição
    atual em vermelho;
  - o config tem `オートマッピング` com os modos `フリー` (Free) e `こてい`
    (Fixed); o modo Fixed é norte-para-cima;
  - screenshot do **Gate Keeper** azul no vão escuro:
    <https://cielgrand.web.fc2.com/img/ddsmegaten33.png>;
  - screenshot do auto-map da cidade:
    <https://cielgrand.web.fc2.com/img/ddsmegaten22.png>.
- Ressalva: o texto é uma visão geral do sistema; não é um mapa passo a passo.

### 6. Tabela de RAM / cheats públicos

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
- O Gate Keeper foi confirmado em `(2,2)` (WRAM), com o diálogo
  `おい、坊主！…`; o velho de verde em `(3,3)` é outro NPC.
- A escada foi acionada em `(2,3)` (WRAM), com `階段を降りますか？` → `YES`,
  e desceu para o 7F em `(10,2)` (HUD `7F`).
- A primeira batalha foi validada no 7F em `(8,2)` (WRAM): encontro aleatório
  com `妖魔ヘケットが現れた！`, menu de batalha, ataques/dano, revide e
  negociação `TALK` → `NO` encerrando a batalha em paz.
- A vitória/level-up foi validada contra 2 Mad Slugs, com boost de debug:
  `外道マッドスラッグを倒した！`, 100 EXP, 65 Macca, 20 MAG e
  `レベルアップ：ナカジマあああ` (LV 2). A alocação do `BONUS` também foi
  validada (Nakajima e Yumiko, `YES`/`NO`); Yumiko aprendeu magia e o jogo
  voltou à dungeon com HP 30/30 e 27/27. O travamento inicial era artefato
  dos atributos 99 acima do teto de 35 da tela, não bug do recomp.
- O save/load real foi validado (CP-013): o elder grava o slot, o flush no
  shutdown persiste `save.srm`, o boot natural relê o arquivo e o `CONTINUE`
  do título carrega o estado no 8F. Save states antigos podem restaurar SRAM
  zerada; o `save1` foi regenerado.

## Próximos passos de pesquisa

1. Confirmar as coordenadas/gatilhos de Basim, Gnome e Dryad no 7F e descer ao
   6F.
2. Mapear o 7F com o auto-map `Fixed` e `0x877`/`0x878`/`0x865`.
3. Validar o início do Megami Tensei II (CP-014) e continuar a cobertura de
   batalha/AOT no MT1.
