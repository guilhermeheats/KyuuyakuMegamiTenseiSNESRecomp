# Checkpoints de validação

Use estes checkpoints para comparar o recomp com o emulador. Para cada um, guarde: frame, screenshot, estado do input e, se possível, um hash da WRAM.

| ID | Cena | Como chegar | Estado |
|---|---|---|---|
| CP-000 | Boot / primeiro frame | iniciar o jogo | OK — boot executa; frame 600 ainda preto |
| CP-001 | Texto de abertura | aguardar o boot (~frame 1800) | OK |
| CP-002 | Tela de título | aguardar (~frame 3600) | OK |
| CP-003 | Introdução do MT1 | pressionar Start no título e aguardar | OK — texto em ~frame 4200 |
| CP-004 | Seleção de save / novo jogo | avançar a introdução | pendente |
| CP-005 | Primeira sala da dungeon | terminar a introdução e andar | pendente |
| CP-006 | Primeira batalha | andar até um encontro | pendente |
| CP-007 | Menu de status | abrir o menu | pendente |
| CP-008 | Salvar e carregar | salvar, reiniciar, carregar | pendente |
| CP-009 | Início do Megami Tensei II | completar o MT1 ou usar save de teste | pendente |

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
