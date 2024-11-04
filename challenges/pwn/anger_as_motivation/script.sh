#!/bin/sh

BIN="/motivation"
PORT="8002"

socat -s TCP-LISTEN:"${PORT}",reuseaddr,fork EXEC:"${BIN}",stderr
