FROM python:3.14-slim

WORKDIR /app

# Install socat to expose the script over TCP
RUN apt-get update && apt-get install -y socat && rm -rf /var/lib/apt/lists/*

COPY . .

# reuseaddr and fork allow multiple concurrent connections
CMD ["socat", "TCP-LISTEN:8001,reuseaddr,fork", "EXEC:python3 -u main.py"]
