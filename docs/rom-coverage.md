# Cobertura de bytes do ROM — 2026-11-18

Este relatório mede **bytes de instrução descobertos** no ROM original, não
uma porcentagem subjetiva de “decompilação”. Todos os números são contagens
do ROM japonês limpo:

- CRC32 `c8d286c9`
- SHA-256 `ffdc7f254c6d965d481918e7d53a451f94f6b1cb035383ae3dfc8f3b5895de3b`

## Método

1. O manifesto final tem **1229 nós / 1229 AOT / 0 LLE-only**.
2. Cada nó foi decodificado com o decoder v2; os bytes de cada instrução
   foram mapeados para o offset LoROM e deduplicados.
3. `data_region` e `force_lle` foram lidos dos cfgs.
4. Nenhum byte de ROM, gráfico ou tabela é reproduzido aqui; só contagens.

## Grafo

| Métrica | Valor |
|---|---:|
| Roots | 72 |
| Variantes descobertas | **1229** |
| Variantes AOT-eligible | **1229** |
| Variantes LLE-only | **0** |
| Bancos com código | 12 |
| Entradas de dispatch | 951 |
| Entradas com AOT | 951 |
| Variantes AOT no dispatch | 1229 |
| Instruções físicas únicas | 52.074 |

Além do grafo, existem **4 entradas `force_lle` intencionais**, fora do
manifesto de nós: `$00:8000` (reset), `$00:827A` (NMI), `$00:86C0` e
`$00:88CE` (HDMA). Contando-as como funções, a taxa efetiva é
**1229 / 1233 = 99,6756% AOT** por contagem de funções.

## Bytes do ROM

| Métrica | Bytes | % do ROM |
|---|---:|---:|
| ROM total | 2.097.152 | 100% |
| Instruções únicas descobertas | **117.456** | **5,6007%** |
| Instruções no grafo AOT | 117.456 | 100% do grafo |
| `data_region` (fronteiras de BRK) | 4 | 0,0002% |
| Desconhecido (dados/gráficos/som/código não achado) | 1.979.696 | 94,3993% |

O número de **5,6007%** é a fração do ROM ocupada por instruções já
decodificadas. Ele **não** significa “5,6% decompilado”: a maior parte do
cartucho é dado, gráfico, som ou código ainda não alcançado.

### Denominadores de código

| Denominador | Capacidade | Instruções descobertas | Cobertura |
|---|---:|---:|---:|
| 12 bancos com código | 393.216 | 117.456 | **29,8706%** |
| 6 bancos do núcleo (`$00`,`$01`,`$02`,`$03`,`$05`,`$30`) | 196.608 | 109.498 | **55,6936%** |
| ROM total | 2.097.152 | 117.456 | **5,6007%** |

Os bancos contêm dados além de código; por isso a cobertura dos 12 bancos é
um **limite inferior** de código mapeado, não uma divisão exata
código/dados.

## Por banco

| Banco | Bytes de instrução | % do banco (32 KB) | Papel aproximado |
|---|---:|---:|---|
| `$00` | 16.602 | 50,67% | núcleo / boot / main loop |
| `$01` | 22.236 | 67,86% | núcleo / texto / input |
| `$02` | 14.243 | 43,47% | núcleo / batalha / menus |
| `$03` | 22.295 | 68,04% | núcleo / save / texto |
| `$04` | 1.437 | 4,39% | periférico |
| `$05` | 14.064 | 42,92% | núcleo / campo / texto |
| `$07` | 925 | 2,82% | periférico |
| `$21` | 664 | 2,03% | periférico |
| `$2E` | 2.854 | 8,71% | periférico |
| `$30` | 20.058 | 61,21% | som / gráficos |
| `$38` | 391 | 1,19% | periférico |
| `$3F` | 1.687 | 5,15% | periférico |

Os outros 52 bancos não têm instrução decodificada; são majoritariamente
dados, gráficos, som ou código de rotas ainda não capturadas.

## Validação dinâmica

| Teste | Resultado |
|---|---|
| A/B `save9` | 99,9078–99,9063% AOT, `step 60` 1,033–1,036s |
| Stubs / tier hits | 0 / 0 |
| Boot até título | frame 3728, 0 off-rails, 0 stubs |
| Título vs `snesref` | 6 bytes de WRAM, SRAM idêntica, AE 2353 / RMSE 30,29 |
| `save4` / `save9` | party correta, 0 stubs |
| Campo (`save2`) | 12 mil frames, 0 off-rails, 0 stubs |
| AOT acumulado no campo | 99,5701% (6 mil frames), 98,3445% (12 mil frames) |
| LLE quente no campo | `$00:9300`, 0,4106% dos ciclos |

O LLE restante no campo está fora do grafo AOT (reset/NMI/HDMA e o caminho
`$00:9300`), não em nós LLE-only. O `force_lle` da NMI/HDMA é a próxima
fronteira da fase 2.

## Leitura honesta

- **Grafo descoberto:** 100% AOT.
- **Código já descoberto:** 117.456 bytes, 100% no grafo AOT.
- **12 bancos de código:** 29,8706% dos bytes são instruções mapeadas; o
  resto é dado ou código não descoberto.
- **6 bancos do núcleo:** 55,6936% dos bytes são instruções mapeadas.
- **ROM física:** 5,6007% dos bytes são instruções; não é “% de decomp”.
- **Jogo:** boot/título/8F/7F/save4/save9/batalha/level-up validados; **6F e
  late game ainda não mapeados**.

O próximo passo para aumentar o denominador é a fase 2 (tabelas indiretas,
HDMA e `$30:$0080AE`) e a captura da rota até o 6F. O mapa acima é a base
exata para comparar os próximos lotes.
