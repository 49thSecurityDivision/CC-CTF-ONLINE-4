FROM frolvlad/alpine-python3:latest

RUN apk add --no-cache socat
RUN pip3 install wonderwords

COPY story_time.py /

CMD socat -v -T 15 TCP-LISTEN:8005,reuseaddr,fork EXEC:"python3 /story_time.py"
