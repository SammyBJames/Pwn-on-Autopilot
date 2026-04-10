FROM python:3.14-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# Expose port for the challenge
EXPOSE 8002

# Run flask using a lightweight server, listening on all interfaces
CMD ["python3", "app.py"]
