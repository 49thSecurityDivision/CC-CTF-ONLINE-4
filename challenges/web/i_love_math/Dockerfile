FROM python:3.9-slim

WORKDIR /app
COPY app.py /app/

COPY flag.txt /flag.txt

RUN pip install flask

EXPOSE 8080

CMD ["python", "app.py"]
