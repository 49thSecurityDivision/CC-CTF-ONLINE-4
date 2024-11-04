#!/bin/sh

BIN="fail_safe"
VER="1.0"

docker container kill "${BIN}" || :
docker build -t "${BIN}":"${VER}" .
docker run -t --name "${BIN}" -d --rm --network host "${BIN}":"${VER}"
