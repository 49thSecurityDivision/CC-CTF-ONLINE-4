FROM frolvlad/alpine-python3:latest

RUN apk add --no-cache socat

COPY mathemagician.py /

CMD socat -v -T 15 TCP-LISTEN:8004,reuseaddr,fork EXEC:"python3 /mathemagician.py"
