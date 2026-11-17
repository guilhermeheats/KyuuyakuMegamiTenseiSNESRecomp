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
| CP-010 | Primeira batalha | rota confirmada em `docs/route-8f.md`: Gate Keeper `(2,2)`, escada `(2,3)`, 7F `(10,2)`, batalha em `(8,2)` | **OK** — evento scripted de Heket; menu `FIGHT`/`ESCAPE`/`TALK`/`AUTO`, ataques, dano, revide e negociação `TALK`→`NO`; batalha encerrada em paz e retorno ao dungeon |
| CP-011 | Menu de status | apertar A na passagem (~frame 16400) | OK — COMP/MAGIC/ITEM/STATUS; ficha em ~frame 16800 |
| CP-012 | Auto-mapping | A → COMP → `オートマッピング` (5º item; down ×4); configurar `Fixed` | OK — minimapa local; modo Fixed norte-para-cima mostra posição/EV |
| CP-013 | Salvar e carregar pelo jogo | salvar via SRAM, reiniciar, carregar | parcial — menu do elder tem 4 slots e `記録する`/`外に出る`; o SRAM lido ao vivo ficou zerado, falta validar o flush/carregamento |
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
- **Pós-batalha:** retorno ao dungeon do 7F em `(8,2)`, party em 10/10 e 9/9.
- **Saves locais:** `save10` (8F equipado), `save11` (chegada ao 7F),
  `save9` (mensagem de Heket), `save8` (menu inicial da batalha),
  `save7` (menu após o primeiro turno), `save6` (pós-batalha).
  Esses arquivos ficam em `build-debug/saves/` e não são versionados.

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
