#!/bin/bash

GIF_PATH=$1

echo "---->${GIF_PATH}<------"

#sleep 2

mpv --no-config --audio-device=alsa --background='0.0' --keep-open=yes --loop=inf --geometry=50%:50% --no-border --panscan=1.0 --ontop --player-operation-mode=pseudo-gui "$GIF_PATH" &2>1 &


#mpv --no-config --background='0.0'  --audio-device=pulse --keep-open=yes --loop=inf --geometry=50%:50% --no-border --panscan=1.0 --ontop --player-operation-mode=pseudo-gui  "$GIF_PATH"
#mpv --no-config --keep-open=yes --loop=inf --geometry=50%:50% --no-border --ontop "$GIF_PATH"
