# Dependências de build — openSUSE Leap 16

O scaffold consegue baixar e compilar o SDL3 sozinho, mas o SDL ainda precisa das bibliotecas de desenvolvimento do sistema para criar janela, usar OpenGL e tocar áudio.

## Instalação

```bash
sudo zypper install -y \
  libX11-devel libXext-devel libXrandr-devel libXcursor-devel libXi-devel \
  libXfixes-devel libXinerama-devel libXss-devel libXxf86vm-devel libXrender-devel \
  libXtst-devel \
  wayland-devel wayland-protocols-devel libdecor-devel libxkbcommon-devel \
  Mesa-libGL-devel Mesa-libEGL-devel Mesa-libGLESv2-devel \
  alsa-devel libpulse-devel pipewire-devel \
  systemd-devel libdrm-devel libgbm-devel dbus-1-devel \
  libusb-1_0-devel fribidi-devel libthai-devel
```

`libjack-devel` não entra na lista: neste sistema o `pipewire-jack` já ocupa o provedor de JACK e o pacote entra em conflito. O JACK é opcional para o SDL; ALSA/PipeWire/Pulse bastam.

## Depois de instalar

```bash
cd ~/Projects/KyuuyakuTen
rm -rf build build-headless
cmake -S . -B build -G Ninja -DCMAKE_BUILD_TYPE=Release
cmake --build build --parallel
```

Se o CMake ainda não encontrar X11/Wayland/OpenGL, confira o log `build/CMakeFiles/CMakeOutput.log` e o resumo do SDL no final da configuração.

## Observação

O build `build-headless` foi uma tentativa de contornar a falta dos pacotes com `-DSDL_UNIX_CONSOLE_BUILD=ON`; ele não serve para jogar porque não tem backend de vídeo. O caminho normal é instalar as dependências acima e usar `build/`.
