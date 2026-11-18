# Comparação com emulador de referência

Esta nota registra a primeira comparação do recomp com um emulador
independente. O objetivo é detectar divergências de estado (WRAM/SRAM) e de
renderização antes de promover mais rotinas para AOT.

## Ferramenta usada

- **snesref** (`snesrecomp/tools/snesref`), o frontend de referência do
  projeto, com o core libretro **Snes9x 1.63** (`snes9x_libretro.so`).
- O **MesenCE 2.2.1 Linux x64** foi baixado e extraído, mas o binário Linux
  deste release não reconheceu a opção `--testRunner`: ele abriu a GUI e
  falhou com `XOpenDisplay failed`. A comparação com MesenCE fica pendente de
  um build com o test runner funcional; o MesenCE não está no Flathub.
- O snesref foi compilado localmente contra os headers do SDL2 2.30.7 e o
  runtime `libSDL2-2.0.so.0` do sistema. O binário e o core **não** são
  versionados.

## Entrada comum

- ROM japonesa original (`c8d286c9` / SHA-1 `827f6e05...`).
- SRAM do recomp: `build-debug/saves/save.srm` (8192 bytes, 93 não-zero,
  SHA-256 `a0ca482fe5919969a94c51e9073d1b25527a05b06b273f56ec5493ca56aa100a`).
- O snesref carrega a SRAM com `SNESREF_SRAM_IN=...` e usa
  `SNESREF_WRAM_FILL=0` para partir de uma WRAM zerada, como o hard reset do
  recomp.

### Script do snesref

```text
wait 3660
dump title3660
quit
```

Execução (caminhos locais):

```bash
SNESREF_HEADLESS=1 \
SNESREF_WRAM_FILL=0 \
SNESREF_SRAM_IN=build-debug/saves/save.srm \
SNESREF_SCRIPT=title3660.txt \
SNESREF_DUMP_DIR=/tmp/opencode/snesref-run/dumps \
./snesref snes9x_libretro.so "$HOME/roms/kyuuyaku.sfc"
```

### Lado do recomp

```python
c.query("loadstate 1")   # título com SRAM válida; frame 3660
c.query("step 30")
# ler 0x00000..0x1FFFF em blocos de 0x800 com read_ram
```

## Resultados (frame 3660, tela de título)

- **WRAM:** 6 bytes diferentes em 131072 (0,0046%):

  | Endereço | recomp | snesref | Observação |
  |---|---|---|---|
  | `$028D` | `0x74` | `0x73` | contador de animação |
  | `$1BFE` | `0xC0` | `0xBF` | scratch da stack |
  | `$1FDE` | `0x41` | `0x42` | scratch da stack |
  | `$1FEC` | `0x40` | `0x41` | scratch da stack |
  | `$1FEE` | `0x30` | `0x03` | scratch da stack |
  | `$07C03` | `0x30` | `0x32` | timer/PPU auxiliar |

  Os geradores de RNG em `$0200–$0204` e os contadores de frame em
  `$0236`/`$023B` bateram exatamente neste frame.

- **SRAM:** idêntica nos três lados (recomp, snesref e `save.srm`), com o
  mesmo SHA-256 e 93 bytes não-zero.

- **Framebuffer do título:** 2353 pixels diferentes (4,10%) e RMSE 30,29
  (0,046%). A diferença visual está concentrada na animação do logo e no
  círculo do cursor I/II; o layout, as fontes e as cores estáticas batem.

A comparação foi repetida depois da varredura de cobertura/AOT (105 variantes
em 10 bancos, com `$00:86C0`/`$00:88CE` em LLE): os mesmos **6 bytes** de
WRAM, a mesma SRAM e o mesmo framebuffer (AE 2353 / RMSE 30,29). O
`unresolved_stub_get` ficou **zero** no título. A promoção AOT não alterou o
estado de referência.

## Limitações e próximo passo

- A tela de título, tanto no recomp quanto no snesref, mostra apenas a
  seleção **I/II** dos dois jogos; não há um menu `CONTINUE` visível nesse
  ponto. O caminho exato usado no CP-013 para carregar o save pelo título
  ainda precisa ser reproduzido. A validação da SRAM em si não depende disso.
- Para comparar dungeon/batalha, é preciso um ponto de entrada comum. A
  opção mais direta é reproduzir o carregamento pelo título (ou usar um save
  state equivalente no snesref) e então comparar WRAM/frame no 8F.
- O MesenCE continua sendo o oráculo desejado para timing/PPU; assim que um
  build Linux com `--testRunner` funcional estiver disponível, repetir este
  roteiro e comparar os mesmos endereços.
