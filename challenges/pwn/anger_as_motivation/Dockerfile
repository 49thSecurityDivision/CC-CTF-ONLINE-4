FROM ubuntu:22.04

ENV FLAG="cc_ctf{50_4ngr_m0t1v4t35_y0u_t00_huh_?}"

EXPOSE 8002

RUN apt update -y
RUN apt upgrade -y
RUN apt install socat -y

COPY ./motivation /motivation
COPY ./script.sh /script.sh

ENTRYPOINT [ "sh", "/script.sh" ]
