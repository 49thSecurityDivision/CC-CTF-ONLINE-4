FROM python:3.9-slim

WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install -r requirements.txt

# Copy application files
COPY app.py schema.sql seed.sql ./

EXPOSE 8080

CMD ["python", "app.py"]
