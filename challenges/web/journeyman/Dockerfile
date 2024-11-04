FROM python:3.9-slim

WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install -r requirements.txt

# Copy application files
COPY app.py .
COPY db.json .

# Create documents directory and add sample files
RUN mkdir documents
# COPY sample_files/* documents/

# Add flag in a non-obvious location
COPY flag.txt /var/internal/company_secrets/flag.txt

# Set up some sample directories to make it look legitimate
RUN mkdir -p /var/internal/company_secrets /var/internal/user_data /var/internal/logs

EXPOSE 8080

CMD ["python", "app.py"]
