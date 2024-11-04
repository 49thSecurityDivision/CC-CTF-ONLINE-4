#!/bin/sh

BIN="/fail_safe"
PORT="8001"

socat -s TCP-LISTEN:"${PORT}",reuseaddr,fork EXEC:"${BIN}",stderr
