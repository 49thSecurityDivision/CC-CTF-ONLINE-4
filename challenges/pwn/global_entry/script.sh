#!/bin/sh

BIN="/global_entry"
PORT="8006"

socat -s TCP-LISTEN:"${PORT}",reuseaddr,fork EXEC:"${BIN}",stderr
