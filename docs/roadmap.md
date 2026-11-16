# Roadmap

## Objetivo

Port nativo jogável de **Kyuuyaku Megami Tensei** usando recompilação estática (snesrecomp), com a ROM japonesa original fornecida pelo usuário.

## Escopo do MVP

- Megami Tensei I do início ao fim.
- Título, seleção de save, introdução, dungeon, batalha, menus, fusão/negociação e save/load.
- Megami Tensei II fica para a fase 2; a engine é compartilhada, então boa parte do trabalho se reaproveita.

Fora do MVP: widescreen, tradução, MSU-1, netplay, mods de conteúdo.

## Expectativa com 5h/semana

| Marco | Tempo estimado |
|---|---|
| ROM verificada + ambiente | 1–2 semanas |
| Boot/título no recomp | 1–2 meses |
| Título → novo jogo → primeira sala | 2–4 meses |
| Vertical slice (dungeon + batalha + save) | 4–8 meses |
| Megami Tensei I completo | 12–18 meses |
| MT1 + MT2 + ending | 24–36 meses |

## Rotina semanal

| Sessão | Tempo | Foco |
|---|---|---|
| Estudo | 2h | 65816, debugger, leitura de código |
| Prática | 2h | build, regen, breakpoints, correções |
| Documentação | 1h | atualizar `docs/` e o bring-up log |

## Primeiros 30 dias

### Semana 1

- [ ] Instalar dependências de build (`docs/linux-build-deps.md`).
- [ ] Configurar e compilar o projeto.
- [ ] Rodar com a ROM e registrar o primeiro frame.
- [ ] Estudar registradores e modos de endereçamento do 65816.

### Semana 2

- [ ] Abrir o jogo no MesenCE/Mesen2.
- [ ] Criar save states de boot e título.
- [ ] Confirmar os vetores de RESET, NMI e IRQ.
- [ ] Comparar o boot do recomp com o emulador.

### Semana 3

- [ ] Identificar o main loop e a rotina de input.
- [ ] Mapear as primeiras variáveis de RAM.
- [ ] Resolver o primeiro dispatch miss.
- [ ] Chegar à tela de título.

### Semana 4

- [ ] Passar do título para a seleção de save/novo jogo.
- [ ] Documentar o caminho e os símbolos descobertos.
- [ ] Atualizar `docs/checkpoints.md`.
- [ ] Definir a próxima meta: primeira sala da dungeon.

## Critério de aceite do vertical slice

1. Boot estável.
2. Título e seleção de save.
3. Novo jogo e introdução.
4. Movimento na primeira dungeon.
5. Primeira batalha com uma ação completa.
6. Menu de status.
7. Salvar, reiniciar e carregar.
