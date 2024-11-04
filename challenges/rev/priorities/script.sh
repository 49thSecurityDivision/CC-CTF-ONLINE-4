#!/bin/sh

BIN="/priorities"
PORT="8033"

socat -s TCP-LISTEN:"${PORT}",reuseaddr,fork EXEC:"${BIN}",stderr
