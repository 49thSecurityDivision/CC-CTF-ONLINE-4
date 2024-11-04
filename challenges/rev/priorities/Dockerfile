FROM ubuntu:22.04

ENV ANSWER="1144201745"
ENV FLAG="cc_ctf{s0m3b0dyKN0W\$th31rPR10R1T13S}"

EXPOSE 8033

RUN apt update -y
RUN apt upgrade -y
RUN apt install socat -y

COPY ./priorities /priorities
COPY ./script.sh /script.sh

ENTRYPOINT [ "sh", "/script.sh" ]
