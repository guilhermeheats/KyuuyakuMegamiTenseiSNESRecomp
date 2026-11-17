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

## Próximo uso

1. Carregar `save5` (dungeon) ou `save8` (junção).
2. Ler uma faixa da WRAM antes/depois de um passo em cada direção.
3. Correlacionar os valores com a posição no mapa do 8F.
4. Ao identificar a coordenada da escada/elevador, navegar até ela com
   `set_controller` + `step`, sem editar o estado do jogo.
5. Validar a descida ao 7F e a primeira batalha.

Não use `write_ram` em um save real; use sempre um save state descartável e
recarregue-o depois do teste.
