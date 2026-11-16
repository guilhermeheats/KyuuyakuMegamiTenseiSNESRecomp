# RAM map — rascunho

Este arquivo reúne âncoras iniciais para comparar o recomp com o emulador. Os endereços abaixo vêm de cheats públicos do GameHacking.org; eles servem para localizar variáveis, não como documentação definitiva da engine.

| Endereço | Uso relatado | Observação |
|---|---|---|
| `$7E0C72`–`$7E0C74` | dinheiro / makka (3 bytes) | cheat “999,999 Yen/Makka” |
| `$7E0C75`–`$7E0C76` | magnetita (2 bytes) | cheat “9,999 Magnetite” |
| `$7E0420` | flag de encontros aleatórios | `00` = sem encontros |
| `$7E0D04`–`$7E0D05` | HP do personagem 1 | cheat “P1 Always Has Max 999 HP” |
| `$7E0D09`–`$7E0D0D` | stats do personagem 1 | cheat “P1 Max Stats” |
| `$7E0D14`–`$7E0D15` | HP do personagem 2 | cheat “P2 set max HP to 999” |
| `$7E0D16` | MP do personagem 2 | cheat “P2 Infinite MP” |
| `$7E0D19`–`$7E0D1D` | stats do personagem 2 | cheat “P2 Max Stats” |

## Como usar

1. Abra o jogo no MesenCE/Mesen2.
2. Confira o valor no memory viewer.
3. Faça a mesma leitura no recomp (via debugger ou log).
4. Se os valores não baterem, o problema está antes da variável: banco, ponteiro, DMA ou rotina de menu.

## TODO

- Confirmar quais endereços são de fato P1/P2 (os rótulos dos cheats podem estar trocados).
- Mapear coordenadas do jogador, direção, mapa atual e estado de encontro.
- Mapear ponteiros de party, inventário e demônios.
- Mapear o buffer de texto e o estado da caixa de diálogo.
