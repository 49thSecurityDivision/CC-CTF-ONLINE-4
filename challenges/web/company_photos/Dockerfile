FROM python:3.9-slim

RUN apt-get update
RUN apt-get install python3-full php python3-pip -y

WORKDIR /app

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY app.py .
COPY flag.txt /flag.txt

RUN mkdir uploads

RUN chmod 777 uploads

EXPOSE 8080

CMD ["python", "app.py"]
