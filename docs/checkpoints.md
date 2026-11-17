# Checkpoints de validação

Use estes checkpoints para comparar o recomp com o emulador. Para cada um, guarde: frame, screenshot, estado do input e, se possível, um hash da WRAM.

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
| CP-010 | Primeira batalha | rota confirmada em `docs/route-8f.md`: Gate Keeper `(2,2)`, escada `(2,3)`, 7F `(10,2)`, batalha em `(8,2)` | **OK** — evento scripted de Heket; menu `FIGHT`/`ESCAPE`/`TALK`/`AUTO`, ataques, dano, revide, negociação `TALK`→`NO` e derrota/game over via `AUTO`; vitória ainda pendente |
| CP-011 | Menu de status | apertar A na passagem (~frame 16400) | OK — COMP/MAGIC/ITEM/STATUS; ficha em ~frame 16800 |
| CP-012 | Auto-mapping | A → COMP → `オートマッピング` (5º item; down ×4); configurar `Fixed` | OK — minimapa local; modo Fixed norte-para-cima mostra posição/EV |
| CP-013 | Salvar e carregar pelo jogo | salvar via SRAM, reiniciar, carregar | **parcial** — gravação/flush OK: o elder grava os 4 slots; `save.srm` tem 8192 bytes e 93 bytes não-zero; o boot relê o arquivo. O carregamento pelo título (`CONTINUE`) ainda falha: mostra `セーブされたデータがありません` e zera o SRAM. |
| CP-014 | Início do Megami Tensei II | completar o MT1 ou usar save de teste | pendente |

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
- **Batalha:** WRAM `(8,2)`, mensagem `妖魔ヘケットが現れた！`; menu
  `FIGHT`/`ESCAPE`/`TALK`/`AUTO`.
- **Combate:** ataques físicos causaram 0–1 de dano; o inimigo revidou com
  2–3 de dano. A negociação `TALK` → `わたしと対等に話すつもりか？` → `NO`
  → `はははっ、よく分かっているようだな` →
  `悪魔は満足そうに去っていった` encerrou a batalha em paz.
- **Derrota/game over:** `AUTO` levou a party a 0/10 e 0/9, com
  `パーティーは敵に敗れて...` / `志半ばに力尽きた` e a cena do barco
  (game over); o jogo não crashou.
- **Vitória:** ainda não obtida; os ataques físicos causam 0–1 e Yumiko não
  tem magia utilizável neste ponto (`使える魔法はありません`).
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
- **Bloqueio:** no título, `START`/`CONTINUE` → `CONTINUE` mostra
  `セーブされたデータがありません` e zera a SRAM. O elder reconhece o mesmo
  save, então o problema está no caminho de validação/carregamento do título,
  não na gravação.
- **Tentativas:** duplicar o slot válido para os quatro offsets e corrigir o
  checksum (`0x5A`) não resolveu; o título continuou zerando a SRAM. A
  comparação com emulador foi iniciada com Snes9x, mas a configuração de
  input do emulador ainda não permitiu selecionar `CONTINUE`.
- **AOT:** as cinco rotinas de SRAM (`$03:A35B` save, `$03:A3BF` load,
  `$03:A397` header, `$03:ACFB` checksum e `$03:AD20` validação) foram
  promovidas em `recomp/symbols.toml` com `emit = true`, `entry_m = 1`,
  `entry_x = 0`. O analyzer gerou 14 variantes AOT e 0 LLE-only; o save AOT
  produziu o mesmo hash `a0ca482f…` do save LLE, mas o `CONTINUE` do título
  continua rejeitando/zerando o SRAM.
- **Diagnóstico GDB:** no boot, `Sram_ValidateChecksums_M1X0` chamou
  `Sram_Checksum_M1X0` para o slot 0 e o checksum calculado foi `0x5A`;
  o valor gravado no save era `0x00`. Mesmo gravando manualmente `0xEF=0x5A`
  e deixando todo o resto igual, o `CONTINUE` ainda zerou a SRAM. Portanto a
  rejeição **não é só o checksum**: o título deve checar outro campo/tabela
  (provável tabela de arquivos/metadata) que o save do elder não preenche.
- **Instrumentação local (revertida):** logs em `cpu_write8`/`cpu_write16`,
  `cart_writeLorom`/`cart_writeHirom`, `RtlReset`, `SnesInit` e
  `RtlReadSram` não dispararam no `CONTINUE`; a SRAM é zerada por um caminho
  que não passa por esses pontos (provável `memset`/DMA/reinit de cart).
- **Próximo passo:** instrumentar `cart_load`/`memset`/DMA ou comparar com
  um save válido de emulador (para ver a tabela/metadata esperada) e achar a
  condição exata que rejeita o save.

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
