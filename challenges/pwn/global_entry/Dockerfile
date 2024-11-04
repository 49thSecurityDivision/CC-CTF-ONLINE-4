FROM ubuntu:22.04

ENV FLAG="cc_ctf{thr34d_l0c4l_gl0b4l5}"

RUN apt update -y
RUN apt upgrade -y
RUN apt install socat -y

COPY ./global_entry /global_entry
COPY ./script.sh /script.sh

ENTRYPOINT [ "sh", "/script.sh" ]
