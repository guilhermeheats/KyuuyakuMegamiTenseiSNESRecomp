# Cobertura de bytes do ROM — 2026-11-18

Este relatório mede **bytes de instrução descobertos** no ROM original, não
uma porcentagem subjetiva de “decompilação”. Todos os números são contagens
do ROM japonês limpo:

- CRC32 `c8d286c9`
- SHA-256 `ffdc7f254c6d965d481918e7d53a451f94f6b1cb035383ae3dfc8f3b5895de3b`

## Método

1. O manifesto final tem **1417 nós / 1417 AOT / 0 LLE-only**.
2. Cada nó foi decodificado com o decoder v2; os bytes de cada instrução
   foram mapeados para o offset LoROM e deduplicados.
3. `data_region` e `force_lle` foram lidos dos cfgs.
4. Nenhum byte de ROM, gráfico ou tabela é reproduzido aqui; só contagens.

## Grafo

| Métrica | Valor |
|---|---:|
| Roots | 80 |
| Variantes descobertas | **1417** |
| Variantes AOT-eligible | **1417** |
| Variantes LLE-only | **0** |
| Bancos com código | 12 |
| Entradas de dispatch | 1103 |
| Entradas com AOT | 1103 |
| Variantes AOT no dispatch | 1417 |
| Instruções físicas únicas | 56.280 |

Além do grafo, existem **2 entradas `force_lle` intencionais**, fora do
manifesto de nós: `$00:8000` (reset) e `$00:827A` (NMI). Contando-as como
funções, a taxa efetiva é **1417 / 1419 = 99,8591% AOT** por contagem de
funções.

Há também **8 nós AOT com borda interpretada** (`has_lle_indirect_edge`):
`$02:DC53`, `$02:ED38` e os seis handlers de som `$30:*`. Eles não são
LLE-only; o `JMP ($80AE,X)` de 16 bits ainda não foi modelado no emitter.

## Bytes do ROM

| Métrica | Bytes | % do ROM |
|---|---:|---:|
| ROM total | 2.097.152 | 100% |
| Instruções únicas descobertas | **126.969** | **6,0544%** |
| Instruções no grafo AOT | 126.969 | 100% do grafo |
| `data_region` (fronteiras de BRK) | 4 | 0,0002% |
| Desconhecido (dados/gráficos/som/código não achado) | 1.970.183 | 93,9456% |

O número de **6,0544%** é a fração do ROM ocupada por instruções já
decodificadas. Ele **não** significa “6% decompilado”: a maior parte do
cartucho é dado, gráfico, som ou código ainda não alcançado.

### Denominadores de código

| Denominador | Capacidade | Instruções descobertas | Cobertura |
|---|---:|---:|---:|
| 12 bancos com código | 393.216 | 126.969 | **32,2899%** |
| 6 bancos do núcleo (`$00`,`$01`,`$02`,`$03`,`$05`,`$30`) | 196.608 | 118.964 | **60,5082%** |
| ROM total | 2.097.152 | 126.969 | **6,0544%** |

Os bancos contêm dados além de código; por isso a cobertura dos 12 bancos é
um **limite inferior** de código mapeado, não uma divisão exata
código/dados.

## Por banco

| Banco | Bytes de instrução | % do banco (32 KB) | Papel aproximado |
|---|---:|---:|---|
| `$00` | 17.306 | 52,81% | núcleo / boot / main loop / HDMA |
| `$01` | 25.667 | 78,33% | núcleo / texto / input / tabelas |
| `$02` | 18.250 | 55,69% | núcleo / batalha / menus |
| `$03` | 22.949 | 70,03% | núcleo / save / texto |
| `$04` | 1.437 | 4,39% | periférico |
| `$05` | 14.734 | 44,96% | núcleo / campo / texto |
| `$07` | 925 | 2,82% | periférico |
| `$21` | 711 | 2,17% | periférico |
| `$2E` | 2.854 | 8,71% | periférico |
| `$30` | 20.058 | 61,21% | som / gráficos |
| `$38` | 391 | 1,19% | periférico |
| `$3F` | 1.687 | 5,15% | periférico |

Os outros 52 bancos não têm instrução decodificada; são majoritariamente
dados, gráficos, som ou código de rotas ainda não capturadas.

## Validação dinâmica

| Teste | Resultado |
|---|---|
| A/B `save9` | 99,9094–99,9109% AOT, `step 60` 1,050–1,060s |
| Stubs / tier hits | 0 / 0 |
| Boot até título | frame 3722, 0 off-rails, 0 stubs |
| Título vs `snesref` | 6 bytes de WRAM, SRAM idêntica, **2353 pixels diferentes (4,10%)** |
| `save4` / `save9` | party correta, 0 stubs |
| Batalha/menus (`save0/5/7`) | 0 off-rails, 0 stubs |
| Campo (`save2`, 2 mil frames) | 0 off-rails, 0 stubs, 99,7088% AOT |
| Checkpoint 6F (slot 12, 780 frames) | 0 stubs, 0 off-rails, `step 60` 1,034–1,039s, AOT 98,25–98,59%, 0 roots novos |
| LLE quente no campo | `$00:9300`, 0,2741% dos ciclos |

O LLE restante no campo está fora do grafo AOT (reset/NMI, bordas
indiretas e o caminho `$00:9300`), não em nós LLE-only. Os HDMA já são AOT;
a próxima fronteira é modelar a tabela 16-bit `$80AE`, os dois sites do
banco `$02` e continuar a rota a partir do checkpoint do 6F.

## Leitura honesta

- **Grafo descoberto:** 100% AOT.
- **Código já descoberto:** 126.969 bytes, 100% no grafo AOT.
- **12 bancos de código:** 32,2899% dos bytes são instruções mapeadas; o
  resto é dado ou código não descoberto.
- **6 bancos do núcleo:** 60,5082% dos bytes são instruções mapeadas.
- **ROM física:** 6,0544% dos bytes são instruções; não é “% de decomp”.
- **Jogo:** boot/título/8F/7F/**6F**/save4/save9/batalha/level-up
  validados; o restante do 6F e o late game ainda não estão mapeados.

O próximo passo para aumentar o denominador é modelar a tabela 16-bit de
`$80AE`, resolver os dois sites do banco `$02` e continuar a rota a partir
do checkpoint do 6F.
O mapa acima é a base exata para comparar os próximos lotes.
