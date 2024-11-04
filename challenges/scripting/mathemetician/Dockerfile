FROM frolvlad/alpine-python3:latest

RUN apk add --no-cache socat

COPY mathemetician.py /

CMD socat -v -T 15 TCP-LISTEN:8003,reuseaddr,fork EXEC:"python3 /mathemetician.py"
