# Scripts de input

Estes scripts usam o formato do host do snesrecomp (`--script`) e servem para
reproduzir o caminho já validado sem repetir a introdução inteira.

Os save states ficam em `build/saves/saveN.sav` e **não** são versionados.

## Cadeia de estados

| State | Frame | Cena | Script que gera |
|---|---:|---|---|
| `save1` | 3600 | tela de título | `save-title.txt` |
| `save2` | 11299 | entrada do nome do protagonista | `intro-chunk1.txt` |
| `save3` | 11883 | entrada do nome da Yumiko | `name-clean-yumiko.txt` |
| `save4` | 12667 | distribuição de status do protagonista | `name-save-stats.txt` |
| `save5` | 14861 | primeira dungeon, corredor inicial | `enter-game-save.txt` |
| `save6` | 15346 | diálogo do baú | `save-chest.txt` |
| `save7` | 15868 | baú aberto, loot recebido, um passo atrás | `chest-loot-save.txt` |
| `save8` | 16232 | passagem lateral, com o menu acessível | `save-junction.txt` |

Para regenerar, rode na ordem. Cada script carrega o state anterior.

## Scripts

| Script | Função |
|---|---|
| `save-title.txt` | espera o título (~frame 3600) e salva `save1` |
| `load-title-test.txt` | carrega `save1` para testar rápido |
| `title-start.txt` | pressiona Start no título |
| `intro-skip.txt` | avança a introdução com A (exemplo; não chega ao fim sozinho) |
| `intro-chunk1.txt` | carrega `save1`, acelera com turbo, avança com A e salva `save2` |
| `name-clean-yumiko.txt` | confirma o nome do protagonista e salva `save3` |
| `name-save-stats.txt` | confirma Yumiko e salva `save4` |
| `enter-game-save.txt` | distribui os 15 pontos, confirma e salva `save5` |
| `load-game.txt` | carrega `save5` |
| `move-forward.txt` | dá um passo para frente |
| `move-forward-3.txt` | vai até o baú |
| `save-chest.txt` | salva `save6` no diálogo do baú |
| `chest-open.txt` | carrega `save6`, abre o baú e mostra o loot |
| `chest-loot-save.txt` | abre o baú, fecha a mensagem, dá um passo atrás e salva `save7` |
| `save-junction.txt` | vira à esquerda, avança e salva `save8` |
| `junction-a.txt` | carrega `save8` e abre o menu (COMP/MAGIC/ITEM/STATUS) |
| `menu-status.txt` | abre o menu e entra em STATUS |
| `menu-status-detail.txt` | abre a ficha detalhada do personagem |
| `menu-comp.txt` | abre o submenu COMP |
| `menu-automap.txt` | abre COMP → オートマッピング |

## Exemplo

```bash
./build/KyuuyakuTen \
  --script tools/scripts/save-title.txt \
  "$HOME/roms/kyuuyaku.sfc"
```

Para capturar frames:

```bash
SNESRECOMP_FRAMEDUMP_START=14861 \
SNESRECOMP_FRAMEDUMP_END=14861 \
SNESRECOMP_FRAMEDUMP_PIXELS=1 \
./build/KyuuyakuTen \
  --script tools/scripts/load-game.txt \
  --framedump /tmp/kmt-frames \
  "$HOME/roms/kyuuyaku.sfc"
```

## Navegação via servidor TCP (`build-debug`)

`nav_mikon.py` usa o servidor de debug na porta 4377 (não o `--script` do host)
e serve para calibrar movimento e explorar o 8F:

```bash
./build-debug/KyuuyakuTen --no-launcher "$HOME/roms/kyuuyaku.sfc" &
python3 tools/scripts/nav_mikon.py --loadstate 9 --state
python3 tools/scripts/nav_mikon.py --loadstate 9 --forward 1 --state
python3 tools/scripts/nav_mikon.py --face E --probe
python3 tools/scripts/nav_mikon.py --automap
```

Endereços observados: `0x877` = x, `0x878` = y, `0x80F` = direção
(`0`=N, `1`=E, `2`=S, `3`=W), `0x811`/`0x813` = contadores de movimento/giro,
`0x865` = área/sala, `0x867` = background/view. O auto-map é um minimapa local
(abre com `A` → `COMP` → 5º item → `A`).

## Observações

- Os scripts dependem do timing atual do build. Se a sequência mudar, ajuste os
  `wait`.
- O state `save2` foi gerado por um avanço automático com A e contém caracteres
  extras no nome (`ナカジマあああ`). É um artefato de teste, não um bug do
  recomp. Para um nome limpo, será preciso parar o avanço antes da tela de nome
  ou apagar os caracteres extras nela.
- `save3`/`save4`/`save5` foram regenerados a partir dessa cadeia; o nome do
  protagonista continua com o artefato.
