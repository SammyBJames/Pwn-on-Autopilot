FROM python:3.14-slim

# Install socat to expose the python script over a TCP port
RUN apt-get update && apt-get install -y socat && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY math_server.py .

# Expose port for the challenge
EXPOSE 8001

# Run socat. reuseaddr and fork allow multiple concurrent connections. 
# -u is passed to python to disable output buffering so data is sent immediately.
CMD ["socat", "TCP-LISTEN:8001,reuseaddr,fork", "EXEC:python3 -u math_server.py"]
