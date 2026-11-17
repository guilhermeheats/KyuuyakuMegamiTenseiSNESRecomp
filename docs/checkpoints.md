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
| CP-010 | Primeira batalha | descer ao 7F (rota em `docs/route-8f.md`) e andar até um encontro | pendente — 8F é Mikon City, sem batalhas; escada/Gate Keeper ainda não acionados. 7F tem batalhas fixas Basim/Gnome |
| CP-011 | Menu de status | apertar A na passagem (~frame 16400) | OK — COMP/MAGIC/ITEM/STATUS; ficha em ~frame 16800 |
| CP-012 | Auto-mapping | A → COMP → `オートマッピング` (5º item; down ×4) | OK — minimapa local rotacionado; não é mapa global |
| CP-013 | Salvar e carregar pelo jogo | salvar via SRAM, reiniciar, carregar | parcial — menu do elder tem 4 slots e `記録する`/`外に出る`; o SRAM lido ao vivo ficou zerado, falta validar o flush/carregamento |
| CP-014 | Início do Megami Tensei II | completar o MT1 ou usar save de teste | pendente |

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
