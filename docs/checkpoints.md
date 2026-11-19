# Checkpoints de validação

Use estes checkpoints para comparar o recomp com o emulador. Para cada um, guarde: frame, screenshot, estado do input e, se possível, um hash da WRAM.

> **Foco atual (2026-11-18):** decompilação/cobertura estática. Estes
> checkpoints são a suíte de regressão; o trabalho principal está em
> `docs/coverage.md` e `recomp/`.

| ID | Cena | Como chegar | Estado |
|---|---|---|---|
| CP-000 | Boot / primeiro frame | iniciar o jogo | OK — boot executa; frame 600 ainda preto |
| CP-001 | Texto de abertura | aguardar o boot (~frame 1800) | OK |
| CP-002 | Tela de título | aguardar (~frame 3600) | OK |
| CP-003 | Introdução do MT1 | pressionar Start no título e aguardar | OK — texto em ~frame 4200 |
| CP-004 | Nome do protagonista | avançar a introdução (~frame 11299) | OK — `ナカジマ` (state 2 tem artefato `あああ`) |
| CP-005 | Nome da Yumiko | confirmar o primeiro nome (~frame 11883) | OK — `ユミコ` |
| CP-006 | Distribuição de status | confirmar o segundo nome (~frame 12667) | OK — 15 pontos por personagem |
| CP-007 | Primeira dungeon | confirmar os status (~frame 14861) | OK — corredor inicial |
| CP-008 | Movimento | setas na dungeon | OK — câmera muda de célula |
| CP-009 | Interação com baú | andar até o baú (~frame 15100) | OK — diálogo YES/NO; loot `500` + `宝玉` |
| CP-010 | Primeira batalha | rota confirmada em `docs/route-8f.md`: Gate Keeper `(2,2)`, escada `(2,3)`, 7F `(10,2)`, batalha em `(8,2)` | **OK** — encontros de Heket, Mad Slug e besta verde, negociação, game over, vitória normal contra Heket (64 EXP, 20 Macca, 1 `宝玉`, Nakajima LV3), **Basim fixo em `(9,3)`** (30 EXP, 18 Macca, 6 MAG) e level-up/alocação de `BONUS` validados |
| CP-011 | Menu de status | apertar A na passagem (~frame 16400) | OK — COMP/MAGIC/ITEM/STATUS; ficha em ~frame 16800 |
| CP-012 | Auto-mapping | A → COMP → `オートマッピング` (5º item; down ×4); configurar `Fixed` | OK — minimapa local; modo Fixed norte-para-cima mostra posição/EV |
| CP-013 | Salvar e carregar pelo jogo | salvar via SRAM, reiniciar, carregar | **OK** — gravação/flush e carregamento validados; o `CONTINUE` lista o arquivo e restaura o estado. O save state antigo `save1` restaurava SRAM zerada e foi regenerado. |
| CP-014 | Início do Megami Tensei II | completar o MT1 ou usar save de teste | pendente |
| CP-015 | Checkpoint do 6F | carregar slot 12/QUICK criado após as batalhas do 7F | **OK** — mapa `Fixed`, equipamentos em Nakajima/Yumiko; 780 frames sem stub/off-rail, `step 60` 1,034–1,039s; exploração/batalhas revelaram 4 roots novos em `$00` |

## CP-010 — detalhes da primeira batalha

- **Data:** 2026-11-17
- **Build:** `build-debug/KyuuyakuTen` (servidor de debug TCP na porta 4377)
- **ROM:** CRC32 `c8d286c9`
- **Rota:** `save10` em `(1,4)` → `E×3` → `(4,4)` → `N×4` → `(4,0)` →
  `W×2` → `(2,0)` → `S×2` → `(2,2)`.
- **Gate Keeper:** WRAM `(2,2)`, demônio azul no vão escuro; diálogo
  `おい、坊主！…` (o velho de verde em `(3,3)` é outro NPC).
- **Escada:** WRAM `(2,3)`, pergunta `階段を降りますか？`; `YES` →
  HUD `7F`, WRAM `(10,2)` virado para o norte.
- **Batalha (encontro aleatório):** WRAM `(8,2)`, mensagem
  `妖魔ヘケットが現れた！`; menu `FIGHT`/`ESCAPE`/`TALK`/`AUTO`.
- **Segundo encontro (besta verde, provável Basim):** ao voltar para
  `(8,2)`, apareceu uma besta verde (provável Basim); `TALK` respondeu
  `グルルルルル...` e `ESCAPE` falhou duas vezes; o inimigo causou 3 de
  dano em Nakajima.
- **Basim fixo (2026-11-18):** a partir de WRAM `(9,3)`, tentar andar para
  leste dispara `何かが潜んでいた！` → `怪獣バシムが現れた！`. A batalha foi
  vencida com os stats de debug (99) no build AOT: `怪獣バシムを倒した！`,
  **30 EXP**, **18 Macca** (88→106), **6 MAG** e **1 `宝玉`**; Nakajima e
  Yumiko chegaram a **LV3** (37/37 e 39/39) e receberam `BONUS 1`. O tile
  depois mostra `辺りを調べてみた・・・・ / が、何もなかった`; a segunda
  tentativa de andar para leste foi bloqueada. Gnome/Dryad e a rota do 6F
  continuam pendentes.
- **Vitória/level-up (com boost de debug):** contra 2 Mad Slugs no 7F, com
  HP/stats elevados via debug (999 HP, 99 stats). A batalha terminou com
  `外道マッドスラッグを倒した！`, **100 EXP**, **65 Macca** e **20 MAG**;
  Nakajima subiu para **LV 2** e a tela `レベルアップ：ナカジマあああ`
  apareceu com `BONUS 1`.
- **Alocação do BONUS:** a tela de level-up funciona. `Cima`/`Baixo` mudam a
  linha; `Direita` ou `A` somam 1 ao atributo selecionado e descontam o
  bônus; `Esquerda` reduz; depois aparece `YES`/`NO`. Em `YES`, Nakajima
  recebeu o ponto (5º atributo, `$0D0D` 0x20→0x21); a tela passou para
  `レベルアップ：ユミコ`, que também recebeu 1 ponto (`$0D19`
  0x20→0x21), confirmou `YES` e mostrou `ユミコは魔法を憶えた`.
  O jogo voltou à dungeon com HP normalizado para **30/30** e **27/27**.
  Yumiko terminou com `POISON` no painel de status.
- **Causa do travamento anterior:** o boost de debug deixou os atributos em
  99, acima do teto de 0x23 (35) da tela; como o valor base também era 99,
  `A`/`Direita` não conseguiam somar e `Esquerda` não conseguia reduzir. A
  tela exibia todos os atributos limitados a **35**. Reduzir o atributo
  selecionado para 0x20 destravou a alocação; não era bug do recomp.
- **Vitória em dificuldade normal (2026-11-18):** sem boost de debug, contra
  `妖魔ヘケット` no 7F. Nakajima estava com Jack Knife + Combat Suit e Yumiko
  com Combat Suit. Nakajima causou 2–5 por golpe; Heket causou 1–3 e matou
  Yumiko durante a luta. Resultado: `妖魔ヘケットを倒した！`, **64 EXP**,
  **20 Macca** e **1 `宝玉`**; Nakajima subiu de **LV1 para LV3** (HP 23/23,
  primeiro atributo 20→22) e recebeu `BONUS 1`. Yumiko ficou em LV1, 0/9,
  `DEAD`; o `宝玉` não a revive (`宝玉の効果はありません`).
- **Menu de batalha:** o cursor fica em `$028F` (0=FIGHT, 1=ESCAPE, 2=TALK,
  3=AUTO). O menu de ação de Yumiko tem `MAGIC`, mas em LV1 responde
  `使える魔法はありません`. Com `DEFEND`, Yumiko não sofreu dano na rodada
  testada, mas a batalha foi encerrada por `ESCAPE` antes da vitória.
- **HUD de batalha:** em uma batalha normal posterior, o painel mostrou
  `997/997` e `999/999` mesmo com a WRAM em 8/0 e 9/9; os valores brutos
  estavam certos. É um candidato a bug de exibição do recomp, não do estado
  do jogo.
- **Combate:** ataques físicos causaram 0–1 de dano; o inimigo revidou com
  2–3 de dano. A negociação `TALK` → `わたしと対等に話すつもりか？` → `NO`
  → `はははっ、よく分かっているようだな` →
  `悪魔は満足そうに去っていった` encerrou a batalha em paz.
- **Derrota/game over:** `AUTO` levou a party a 0/10 e 0/9, com
  `パーティーは敵に敗れて...` / `志半ばに力尽きた` e a cena do barco
  (game over); o jogo não crashou.
- **Vitória:** ainda não obtida; os ataques físicos causam 0–1 e Yumiko não
  tem magia utilizável neste ponto (`使える魔法はありません`). O grupo tem
  Jack Knife, Nunchaku e Combat Suits no inventário, mas o menu de
  equipamentos ainda não foi dominado — provável motivo do dano baixo.
- **Pós-batalha:** retorno ao dungeon do 7F em `(8,2)`, party em 10/10 e 9/9.
- **Saves locais:** `save10` (8F equipado), `save11` (chegada ao 7F),
  `save9` (mensagem de Heket), `save8` (menu inicial da batalha),
  `save7` (menu após o primeiro turno), `save6` (pós-batalha).
  Esses arquivos ficam em `build-debug/saves/` e não são versionados.

## CP-013 — detalhes do SRAM

- **Data:** 2026-11-17
- **Save feito pelo elder** no 8F `(1,3)` via `記録する` → slot 1 → `YES`.
  A lista do elder passou a mostrar
  `0 ダイダロス L1 ナカジマあああ ユミコ`.
- **Formato observado:** quatro slots de `0x800` bytes em `0x0000`,
  `0x0800`, `0x1000` e `0x1800`; cada slot tem o header `DDSO` em `0x0000`
  e um checksum em `slot+0x00EF`. O save mínimo ocupa 93 bytes não-zero
  (o resto é zero).
- **Gravação:** a rotina `$03:A35B` copia `$7E:0C00` → SRAM `0x0000` e
  `$7E:8000` → SRAM `0x0400`, e grava o checksum em `slot+0x00EF`.
- **Flush:** ao fechar a janela (`SDL_QUIT`), `RtlWriteSram` grava
  `saves/save.srm`; o SHA-256 do arquivo ficou igual ao da SRAM em memória
  (`a0ca482f…`).
- **Leitura no boot:** o processo seguinte carregou o arquivo e a SRAM em
  memória voltou com o mesmo hash `a0ca482f…`.
- **Carregamento (boot natural):** com o `save.srm` válido, subir o jogo
  **sem carregar save state** e ir ao título → `START`/`CONTINUE` →
  `CONTINUE`. A lista mostrou
  `0 ダイダロス L1 ナカジマあああ ユミコ`; `A` → `ロードしますか？` → `YES`
  carregou o jogo no 8F em `(1,4)` virado para o sul, com 10 Macca
  (`0x0A`), party 10/10, 9/9 e 6 MP. **CP-013 OK.**
- **Causa da confusão:** o save state antigo `save1` restaurava uma SRAM
  zerada; todos os testes que faziam `loadstate 1` antes do `CONTINUE`
  viam `セーブされたデータがありません`. O `save1` foi regenerado no título
  com a SRAM válida; `loadstate 1` agora preserva o save.
- **Checksum:** o byte em `slot+0x00EF` fica `0x00`; o jogo aceita o save
  assim mesmo. O valor `0x5A` calculado pelo validador não é exigido para
  o load.
- **AOT:** as cinco rotinas de SRAM (`$03:A35B` save, `$03:A3BF` load,
  `$03:A397` header, `$03:ACFB` checksum e `$03:AD20` validação) foram
  promovidas em `recomp/symbols.toml` com `emit = true`, `entry_m = 1`,
  `entry_x = 0`. O analyzer gerou 14 variantes AOT e 0 LLE-only; o save AOT
  produziu o mesmo hash `a0ca482f…` do save LLE.
- **AOT da tela de level-up:** `LevelUp_Apply` (`$01:B3C6`) ficou LLE-only;
  `LevelUp_PrintStat` (`$01:B5D5`) foi emitida em AOT como `M1X1`. O fluxo
  completo (Nakajima e Yumiko, `BONUS`, `YES`/`NO`, magia aprendida) foi
  testado no build AOT sem crash; estado no `save2`.
- **Comparação de referência (2026-11-18):** com o `snesref` (Snes9x
  libretro) e a mesma SRAM, o frame 3660 do título teve apenas 6 bytes de
  WRAM diferentes (animação/stack), SRAM idêntica e framebuffer com RMSE
  0,046%. O MesenCE Linux não reconheceu `--testRunner`; ver
  `docs/reference-comparison.md`.
- **Nota de teste:** não use um save state capturado antes do save para
  validar o load; ele pode restaurar a SRAM zerada. Faça boot natural com o
  `save.srm` ou regenere o save state depois do save.

## CP-015 — checkpoint do 6F (2026-11-19)

- **Estado:** 6F, auto-map `Fixed`, duas batalhas scriptadas do 7F
  concluídas (Basim incluído), equipamentos equipados em Nakajima e Yumiko.
- **Save:** menu **Select+R** → slot **12** (`save11.sav`) e **QUICK**
  (`savequick.sav`); os dois arquivos têm o mesmo SHA-256
  `5e44d02fb4e3d60e7bbc62c461293fe24fca015102d6ccf7faa4f439ac913958`.
- **Cópia segura:** `logs/kyuuyaku/2026-11-19-6f-slot12.sav` (+ `.thumb`).
- **Carregamento:** `loadstate 11` no processo de validação (equivalente ao
  slot 12 do menu) restaurou o campo no frame 49358.
- **Resultado:** 600 + 180 frames com **zero stubs** e **zero off-rails**;
  `step 60` em **1,034–1,039s**; AOT acumulado **98,25–98,59%**.
- **Cobertura:** o state parado registrou 7.958.086 instruções
  interpretadas e `discoveries: []`; a **exploração/batalhas** a partir dele
  revelou **4 variantes novas em `$00`** (`$8993:M1X0`, `$86C0:M1X1`,
  `$845B:M1X1`, `$8608:M1X0`). O grafo foi para **1421/1421 AOT**; a
  tabela `$02:ED4F` foi resolvida no lote seguinte e levou o grafo a
  **1460/1460 AOT**. As capturas pós-promoção voltaram com
  `discoveries: []`.
- **Carregamento do state:** o state abre com o **analisador** na tela;
  pressione **B três vezes** para voltar ao campo. Batalhas aleatórias
  começam com atraso de ~150–200 frames.
- **Estabilidade:** a validação final roda com `setsid nohup`; as quedas
  anteriores não deixaram core, stub ou off-rail.
- **Observação:** o HUD do quick save ainda mostra `7F`; a rota adota a
  designação do jogador (6F), com a divergência registrada em
  `docs/route-8f.md`.
- **Próximo uso:** carregar esse state para mapear o 6F, procurar
  cura/revival e capturar a continuação da rota.
- **Regressão 1421 (2026-11-19):** boot/título, `save4`/`save9`,
  batalha/menus e 6F repetidos com **zero stubs/off-rails**; título contra
  o `snesref` com 6 bytes de WRAM, SRAM idêntica e 2256 pixels diferentes
  (3,93%). O release foi reconstruído e rodou 60,07 fps no smoke test.

## Formato sugerido de registro

```text
ID:
Data:
Build/commit:
ROM (CRC32):
Frame:
Input:
Screenshot:
WRAM hash:
Resultado:
Observações:
```
