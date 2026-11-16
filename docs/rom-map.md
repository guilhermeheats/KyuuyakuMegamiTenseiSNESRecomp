# Mapa inicial da ROM

## Vetores 65816 (LoROM, banco 0)

Os vetores nativos ficam em `$00:FFE4`–`$00:FFFF`, que nesta LoROM correspondem aos offsets `$007FE4`–`$007FFF` da imagem.

| Vetor | Endereço | Offset na ROM | Observação |
|---|---:|---:|---|
| COP | `$FFFF` | `$007FE4` | não usado |
| BRK | `$FFFF` | `$007FE6` | não usado |
| ABORT | `$FFFF` | `$007FE8` | não usado |
| NMI | `$827A` | `$007FEA` | rotina de NMI |
| UNUSED | `$8000` | `$007FEC` | valor residual |
| IRQ | `$C672` | `$007FEE` | rotina de IRQ |
| RESET | `$8000` | `$007FFC` | ponto de entrada após reset |

## Entradas já semeadas

`recomp/symbols.toml` começa com:

| Nome | Endereço | Uso |
|---|---:|---|
| `I_RESET` | `$8000` | vetor de reset |
| `I_NMI` | `$827A` | NMI |

O vetor IRQ aponta para `$C672`, mas ainda não foi semeado. Nesta versão do snesrecomp, adicionar `I_IRQ` com `emit = false` fez a análise cair de 4 roots para 0; a entrada foi revertida e fica para investigação. O endereço continua registrado no mapa acima.

## Próximos mapeamentos

- Banco 0: reset, init de PPU/APU, main loop, NMI, IRQ.
- Bancos de código: identificar `JSL`/`JSR` de entrada e tabelas de dispatch.
- Dados: gráficos, tabelas de texto, mapas, tabelas de inimigos e save.
- RAM: ver `docs/ram-map.md`.

Este arquivo é um rascunho vivo; atualize conforme o bring-up avançar.
