#!/bin/sh

BIN="/work"
PORT="8007"

trap 'kill $(jobs -p) 2>/dev/null' EXIT

# socat -s TCP-LISTEN:"${PORT}",reuseaddr,fork EXEC:"${BIN}",stderr 2>&1
socat TCP-LISTEN:"${PORT}",reuseaddr,fork EXEC:"${BIN}",stderr
