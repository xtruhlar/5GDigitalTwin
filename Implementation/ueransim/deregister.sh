#!/bin/bash

# UE
UE=ueransim-ue1

UERANSIM_DIR=/UERANSIM
UE_BIN="$UERANSIM_DIR/build/nr-ue"

# Cesta k tvojej konfiguračnej YAML súbore pre UE
CONFIG="$UERANSIM_DIR/config/$UE.yaml"

# Spusti UE s Deregistration-only režimom (špeciálna flag nie je súčasťou UERANSIM, tak to treba simulovať)
$UE_BIN -c $CONFIG -r &
UE_PID=$!

# Počkaj, kým sa zaregistruje (alebo nastav vlastné logiku)
sleep 2

# Pošli 'Deregister Request' pomocou SIGINT – UERANSIM to správne spracuje ako korektné ukončenie
kill -INT $UE_PID

wait $UE_PID