FROM ubuntu:22.04

RUN apt update -y
RUN apt upgrade -y
RUN apt install socat -y

COPY ./target/debug/fail_safe /fail_safe
COPY ./script.sh /script.sh
COPY ./flag.txt /flag.txt

ENTRYPOINT [ "sh", "/script.sh" ]
