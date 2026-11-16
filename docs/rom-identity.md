# Identidade da ROM

## ROM escolhida

- Arquivo local: `~/roms/kyuuyaku.sfc` (fora do repositório; nunca versionar)
- Dataset: No-Intro, dump japonês sem header de copier
- Tamanho: `2.097.152` bytes (2 MiB)
- CRC32: `c8d286c9`
- SHA-1: `827f6e0534e2317e3348ce76bd47bec8691b3563`
- SHA-256: `ffdc7f254c6d965d481918e7d53a451f94f6b1cb035383ae3dfc8f3b5895de3b`
- Mapeamento: LoROM, SlowROM
- SRAM: 8 KiB, com bateria
- Coprocessador: nenhum
- Checksum interno: válido (confirmado pelo `probe_rom.py`)
- Título no header: kana half-width; o probe não o apresentou como ASCII legível

## Por que esta ROM e não a Rev 1

A outra imagem encontrada em `~/Downloads` é a revisão 1:

- CRC32: `e257d574`
- SHA-1: `b1d350fde1ad200d7c331906c3a6fef7d97a7a97`
- SHA-256: `bb9e0011db50ab120b4dce6e7211a778ff035d5eeb57c76eff774bab7946c0ec`

Ela é uma revisão diferente. O projeto foi pinado na ROM japonesa original porque:

1. é a identidade conhecida e documentada (No-Intro);
2. o scaffold foi gerado e validado com ela;
3. manter uma única revisão evita divergência silenciosa no código gerado.

Se no futuro quisermos suportar a Rev 1, o correto é abrir uma variante separada, atualizar `rom_identity.txt` e regenerar com a outra imagem. Não misture as duas no mesmo build.

## Verificação local

```bash
python3 - <<'PY'
import hashlib, zlib, pathlib

p = pathlib.Path("kyuuyaku.sfc")
d = p.read_bytes()
print("tamanho:", len(d))
print("crc32:  ", f"{zlib.crc32(d) & 0xffffffff:08x}")
print("sha1:   ", hashlib.sha1(d).hexdigest())
print("sha256: ", hashlib.sha256(d).hexdigest())
PY
```

O resultado esperado é o bloco acima. Se o arquivo tiver 2.097.664 bytes, ele tem um header de copier de 512 bytes; remova antes de usar:

```bash
dd if=kyuuyaku.smc of=kyuuyaku-clean.sfc bs=512 skip=1
```

## Regra do projeto

- A ROM e o C gerado em `src/gen/` são derivados de material protegido: não entram no Git.
- Não use a ROM traduzida (inglês/português) como base do recomp. Traduções entram depois, como mod de localização em runtime.
- Use sempre `--rom` ou `SNESRECOMP_ROM` apontando para a mesma imagem.
