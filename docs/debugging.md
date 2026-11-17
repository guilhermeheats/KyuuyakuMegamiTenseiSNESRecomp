# Debugging e rastreamento de WRAM

Este projeto pode ser compilado com o servidor TCP de debug do snesrecomp. É
um build separado, apenas para investigação; o build de release não o inclui.

## Build

```bash
cmake -S . -B build-debug -G Ninja \
  -DCMAKE_BUILD_TYPE=RelWithDebInfo \
  -DSNESRECOMP_ENABLE_TRACE=ON
cmake --build build-debug --parallel
```

`build-debug/` é ignorado pelo Git.

## Executar sem janela

```bash
SDL_VIDEODRIVER=dummy SDL_AUDIODRIVER=dummy \
  ./build-debug/KyuuyakuTen --no-launcher \
  "$HOME/roms/kyuuyaku.sfc"
```

O servidor escuta em `127.0.0.1:4377` por padrão. `SNESRECOMP_DEBUG_PORT`
permite outra porta.

## Cliente Python

O cliente fica no submódulo:

```python
import sys
sys.path.insert(0, "snesrecomp/tools")
from sneslib.client import DebugClient

c = DebugClient(4377, timeout=10)
print(c.query("ping"))
print(c.query("frame"))
```

Comandos úteis:

| Comando | Uso |
|---|---|
| `loadstate 5` | carrega o save state 5 |
| `step 30` | avança 30 frames com o jogo controlado |
| `set_controller up` | segura o direcional para cima |
| `clear_controller` | solta os botões |
| `read_ram 80f 8` | lê 8 bytes da WRAM |
| `write_ram 811 01` | escreve 1 byte na WRAM |
| `screenshot nome` | grava um BMP 256x224 |
| `frame` | mostra o frame atual |
| `get_v2_cpu` | estado da CPU |

As capturas de `screenshot` são gravadas no diretório de trabalho do host
(`build-debug/` quando ele é iniciado pela raiz do projeto).

## O que já foi descoberto

- `0x80f`, `0x811` e `0x813` mudam quando o jogador anda ou vira.
- `0x865`/`0x867` também mudam, mas os valores parecem identificadores de
  sala/tile (`0x41`, `0x0d`, `0x11`, `0x33`), não coordenadas simples.
- Escrever em `0x811` altera a visão renderizada, o que confirma que a região
  participa do estado de posição/câmera.
- Ainda não foi possível mapear com segurança o par de coordenadas para o mapa
  do 8F; escrever valores isolados pode renderizar corredores, mas não levou à
  escada `D` nem ao elevador `E`.

## Exploração BFS (2026-11-17)

Foi feito um BFS de caminhos a partir do `save5`, recarregando o state e
repetindo o caminho antes de testar cada direção:

- profundidade 5, limite de 50 nós;
- screenshot de cada nó;
- assinatura lida em `0x80f` e `0x865`.

Resultado: o BFS encontrou muitos estados de **orientação** diferentes no mesmo
trecho, não novas salas. O caminho `up/up/up` a partir do `save5` abre o diálogo
do baú. Nenhum screenshot mostrou a escada `D`, o healer `H` ou o elevador `E`.

A assinatura incluía `0x813` (direção), o que inflou o número de nós. A próxima
iteração deve usar apenas posição/tile e ignorar a direção, além de comparar
com o mapa do 8F.

### Wall follower (2026-11-17)

Foi executado um wall follower left-hand a partir do `save5`, com 113 movimentos
e 89 rotações. Ele percorreu um ciclo fechado de tiles:

```text
0x11 → 0x33 → 0x51 → 0x31 → 0x05 → 0x11 → ...
```

Nenhum tile de escada, healer ou elevador apareceu. Conclusão: a componente
alcançável a partir do `save5` é um loop; a rota para a escada/elevador deve
exigir uma porta/evento ou outro ponto de entrada (por exemplo, o `save8` ou
uma interação com A em um tile específico).

### Interação com A nos tiles do loop

Foram testados os tiles `0x05`, `0x11`, `0x31`, `0x33` e `0x51`, em quatro
orientações cada:

- na maioria, A abre o menu normal (`COMP/MAGIC/ITEM/STATUS`);
- no tile `0x05`, com as orientações 0 e 1, A **não** abre o menu: o tile muda
  para `0x31` e a visão mostra uma parede/abertura. Isso sugere uma porta ou
  transição especial nesse tile;
- mesmo depois dessa transição, o wall follower continua no mesmo ciclo
  `0x11 → 0x33 → 0x51 → 0x31 → 0x05`.

A porta/transição do tile `0x05` é o próximo ponto a investigar com o mapa
do 8F e com A em sequências diferentes.

### Portas de Mikon City (A + direção)

O 8F é uma cidade, não uma dungeon. As transições de porta observadas com A
foram:

| Tile | A + direção | Destino |
|---|---|---|
| `0x41` (início) | face 0 | menu |
| `0x41` | face 1 | `0x11` |
| `0x41` | faces 2/3 | `0x31` |
| `0x31` | face 0 | menu |
| `0x31` | face 1 | `0x05` |
| `0x31` | faces 2/3 | `0x41` |
| `0x05` | faces 0/1 | `0x31` |
| `0x11` | faces 1/2 | `0x31` |
| `0x11` | face 3 | `0x05` |
| `0x51` | face 1 | `0x11` |
| `0x51` | faces 2/3 | `0x01` |
| `0x33` | face 1 | `0x31` |
| `0x35` | qualquer | menu |

Essas transições são portas/entradas de prédios, não escadas. O próximo alvo é
explorar o tile `0x01` e os demais destinos ainda não visitados.

### Save states entre builds

`loadstate 5` funciona no `build-debug`, mas `loadstate 13` carregou um estado
de introdução em vez do corredor. Os states `9`–`13` foram criados pelo build de
release e não são confiáveis no build de debug. Para o próximo BFS, gere os
states **dentro do próprio build-debug** (ou use `save_state`/`load_state` com
arquivos e valide o screenshot antes de explorar).

## Próximo uso

1. Carregar `save5` (dungeon) ou `save8` (junção).
2. Ler uma faixa da WRAM antes/depois de um passo em cada direção.
3. Correlacionar os valores com a posição no mapa do 8F.
4. Ao identificar a coordenada da escada/elevador, navegar até ela com
   `set_controller` + `step`, sem editar o estado do jogo.
5. Validar a descida ao 7F e a primeira batalha.

Não use `write_ram` em um save real; use sempre um save state descartável e
recarregue-o depois do teste.
