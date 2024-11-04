FROM ubuntu:22.04

RUN apt update -y
RUN apt upgrade -y
RUN apt install socat -y

COPY ./work /work
COPY ./flag.txt /flag.txt
COPY ./script.sh /script.sh

HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD nc -z localhost 8007 || exit 1

ENTRYPOINT [ "sh", "/script.sh" ]
