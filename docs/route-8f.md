# Rota do 8F — Mikon City

> **Correção importante:** o 8F é **Mikon City**, uma cidade segura, com lojas,
> Healing Spring, House of Heresy, o homem do password e o baú de 500 makka.
> **Não existem batalhas aleatórias no 8F.** A primeira batalha acontece no
> **7F**; o objetivo aqui é encontrar o Viking/Gate Keeper e descer as escadas.
> O elevador não pode ser usado neste ponto.

O 8F é o andar do baú inicial; a primeira batalha acontece no **7F**. Para
chegar lá é preciso encontrar a escada de descida (`D`) no mapa.

## Rota conhecida

Segundo as notas de rota da comunidade, a sequência do 8F é:

1. Pegar o baú do 8F (`500` Macca; neste build também veio `宝玉`).
2. Sair do quarto do baú para o corredor inferior.
3. Seguir para **leste** pelo corredor inferior.
4. Subir para **norte** pelo lado direito do mapa.
5. Seguir para **oeste** pelo corredor superior.
6. Descer para **sul** até a sala central, onde ficam a escada de descida (`D`)
   e o healer (`H`).

O mapa completo do 8F mostra também a catedral (`C`), o elevador (`E`) e as
escadas. Use o auto-map do jogo (`COMP` → `オートマッピング`) para acompanhar
a posição atual.

## Status do bring-up

- O baú do 8F foi aberto e o loot (`500` + `宝玉`) foi validado.
- O loop de tiles não é uma dungeon: é a área segura de Mikon City. A ausência
  de encontros em 113 movimentos é esperada.
- O próximo objetivo é entrar nas lojas/casas, falar com NPCs, achar o
  Viking/Gate Keeper e a escada para o 7F.
- O quarto do baú tem saídas laterais que levam a corredores longos; a
  exploração inicial voltou ao mesmo baú, então a rota ainda não foi concluída.
- O elevador (`E`) na parte inferior central é uma alternativa à escada (`D`).
- A escada para o 7F ainda **não** foi alcançada; a primeira batalha continua
  pendente.
- Os save states `9`–`13` foram usados em exploração local e não formam uma
  cadeia estável; a cadeia documentada no repositório vai até `save8`.
- O build de debug (`SNESRECOMP_ENABLE_TRACE=ON`) e o servidor TCP foram
  validados. `0x80f`/`0x811`/`0x813` reagem ao movimento, mas ainda não foi
  possível correlacioná-los com segurança com a grade do mapa. Veja
  `docs/debugging.md`.
- Um BFS de profundidade 5 (50 nós) encontrou o diálogo do baú no caminho
  `up/up/up`, mas nenhuma escada, healer ou elevador. A assinatura incluía a
  direção, gerando muitos nós duplicados; a próxima tentativa deve usar só
  posição/tile.
- Um wall follower left-hand (113 movimentos, 89 rotações) percorreu o ciclo
  `0x11 → 0x33 → 0x51 → 0x31 → 0x05 → 0x11` sem encontrar escada, healer ou
  elevador. A área alcançável a partir do `save5` é um loop fechado; a saída
  deve exigir porta/evento ou outro ponto de entrada.
- Teste de A nos cinco tiles do loop: no tile `0x05`, com as orientações 0 e 1,
  A muda para o tile `0x31` em vez de abrir o menu. É uma porta/transição
  especial, mas o loop continua; esse é o próximo ponto de investigação.
- Foram encontradas portas com A em vários tiles: `0x41 → 0x11/0x31`,
  `0x31 → 0x05/0x41`, `0x11 → 0x31/0x05`, `0x51 → 0x11/0x01`. O grafo completo
  está em `docs/debugging.md`. O tile `0x01` ainda não foi explorado.

## Próximo ponto

Ao descer para o 7F:

- a primeira batalha é um encontro aleatório;
- se nenhum encontro aparecer, existe um tile de encontro fixo no 7F;
- para o primeiro combate, evite zumbis, conforme a rota da comunidade.

## Referências

- Notas de rota (Sion): <https://sioneus.me/notes/kmt1/>
- Mapa do 8F usado como referência visual (não versionado):
  <https://www.deviantart.com/24karatdvno/art/Kyuuyaku-Megami-Tensei-Maps--Tower-of-Daedalus-496133904>

O mapa é material de terceiros; não foi copiado para o repositório. A rota
acima é uma descrição textual para orientar o bring-up.
