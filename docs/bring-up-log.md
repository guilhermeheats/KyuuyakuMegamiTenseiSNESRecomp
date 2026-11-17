# Bring-up log

## 2026-11-16

### ROM

- Escolhida a ROM japonesa original (No-Intro), sem header: 2 MiB, LoROM, 8 KiB SRAM, sem coprocessador.
- CRC32 `c8d286c9`, SHA-1 `827f6e0534e2317e3348ce76bd47bec8691b3563`.
- A revisão 1 (`e257d574`) foi descartada para este projeto; é outra revisão.
- `probe_rom.py` confirmou `checksum_valid=True`.

### Projeto

- Repositório criado em `~/Projects/KyuuyakuTen`.
- Scaffold do snesrecomp gerado com 1 jogador, sem netplay, sem GitHub.
- `tools/regen.sh` gerou 4 arquivos C em `src/gen/`, 1 banco e 4 roots.
- `I_RESET` (`$8000`) e `I_NMI` (`$827A`) vieram do scaffold.
- O vetor IRQ foi localizado em `$C672`. Uma tentativa de semeá-lo como `I_IRQ` (`emit = false`) zerou os roots da análise; a entrada foi revertida e o vetor ficou apenas documentado em `docs/rom-map.md`.
- `recomp/bank00.cfg` foi atualizado pelo regen com o bloco de símbolos.

### Build

- A primeira configuração parou por falta de bibliotecas de desenvolvimento do sistema (X11/Wayland/OpenGL/XTest).
- Instalados os pacotes de `docs/linux-build-deps.md`; o `libXtst-devel` foi o último necessário para o SDL habilitar XTest.
- Configuração e build concluídos:
  - binário: `build/KyuuyakuTen` (8,0 MB)
  - 514 alvos compilados
  - SDL3 3.4.10 compilado do source, com X11, Wayland, OpenGL, ALSA e PipeWire.

### Runtime

- `./build/KyuuyakuTen ~/roms/kyuuyaku.sfc`
- Janela 960x720, renderer OpenGL, áudio PipeWire a 32 kHz.
- ~60 fps; a ROM carrega e o jogo executa.
- Marcos observados com `--framedump`:
  - frame 600: tela preta (início do boot)
  - frame 1800: texto de introdução em japonês
  - frame 3600: tela de título “旧約・女神転生”
  - frame 3720: transição após pressionar Start
  - frame 4200: texto da introdução do MT1
  - frame 11299: entrada do nome do protagonista
  - frame 11883: entrada do nome da Yumiko
  - frame 12667: distribuição de status do protagonista
  - frame 14861: primeira dungeon, corredor inicial
  - frame 15100: diálogo do baú (“宝箱だ！ 開けますか？”)
  - frame 15500: loot do baú (`500` + `宝玉`)
  - frame 16400: menu principal (COMP/MAGIC/ITEM/STATUS)
  - frame 16600: submenu COMP (aliados, auto-mapping, config)
  - frame 16800: ficha de status e auto-mapping
- Nenhum screenshot do jogo foi commitado; os frames ficam em `/tmp`.

### Rota do 8F

- O 8F é o andar do baú inicial; a primeira batalha é no 7F.
- A rota conhecida está em `docs/route-8f.md`: baú → corredor inferior a leste → lado direito a norte → corredor superior a oeste → sala central com a escada de descida (`D`).
- O auto-map do jogo (`COMP` → `オートマッピング`) foi validado, mas é um minimapa local e não mostrou a rota completa.
- Exploração: o baú foi aberto; as saídas laterais levam a corredores longos que retornam ao mesmo baú. A escada `D` e o elevador `E` ainda não foram alcançados.
- A primeira batalha continua pendente; os save states 9–13 foram usados em exploração local e não são uma cadeia estável.

### Depuração (2026-11-17)

- Compilado `build-debug` com `-DSNESRECOMP_ENABLE_TRACE=ON`.
- Servidor TCP de debug validado em `127.0.0.1:4377`.
- Testados `loadstate`, `step`, `set_controller`, `read_ram`, `write_ram` e
  `screenshot` com o cliente `snesrecomp/tools/sneslib`.
- `0x80f`, `0x811` e `0x813` mudam com movimento/rotação; escrever em `0x811`
  altera a visão renderizada.
- `0x865`/`0x867` mudam, mas parecem IDs de sala/tile, não coordenadas simples.
- BFS de caminhos a partir do `save5`, profundidade 5/50 nós: o caminho
  `up/up/up` abre o baú; nenhuma escada, healer ou elevador foi encontrado.
- A assinatura incluía a direção (`0x813`), gerando muitos estados duplicados;
  a próxima tentativa deve usar só posição/tile.
- Wall follower left-hand: 113 movimentos e 89 rotações em um ciclo fechado
  `0x11 → 0x33 → 0x51 → 0x31 → 0x05 → 0x11`, sem escada/elevador. A saída
  deve exigir uma porta/evento ou outro ponto de entrada.
- Ainda não foi possível mapear a coordenada da escada `D`/elevador `E`; a
  primeira batalha continua pendente.

### Save states e input

- Criada uma cadeia de save states locais em `build/saves/` (`save1` … `save8`).
- Scripts em `tools/scripts/` reproduzem o caminho; a documentação está em
  `tools/scripts/README.md`.
- O state `save2` contém `ナカジマあああ` por causa do avanço automático com A;
  é um artefato de teste, não um bug do recomp.

### Próximo passo

1. Testar a primeira batalha (`CP-010`).
2. Testar salvar/carregar pelo jogo (SRAM de 8 KiB), não só save state do host.
3. Comparar o boot com o MesenCE e registrar um checkpoint com hash de WRAM.
4. Começar a nomear as rotinas descobertas em `recomp/symbols.toml`.
