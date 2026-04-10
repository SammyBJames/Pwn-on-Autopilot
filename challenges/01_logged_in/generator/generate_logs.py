import json
import random
import base64
import secrets
import ipaddress
from dataclasses import dataclass, asdict
from datetime import datetime, timedelta

@dataclass
class LogEntry:
    timestamp: str
    ip: str
    endpoint: str
    method: str
    status: int
    payload: str

def random_ip():
    return str(ipaddress.IPv4Address(random.randint(0, 2**32 - 1)))

def generate_flag():
    return f'bsides{{{secrets.token_hex(random.randint(16, 32))}}}'

def generate_random_payload(is_flag=False):
    if is_flag:
        flag = generate_flag()
        return base64.b64encode(flag.encode()).decode('utf-8')
    else:
        junk = secrets.token_bytes(random.randint(10, 30))
        return base64.b64encode(junk).decode('utf-8')

def random_status():
    r = random.random()
    if r < 0.70:
        return 200
    elif r < 0.95:
        return 401
    else:
        return random.choice([500, 502, 503, 504])

def main():
    logs = []
    start_time = datetime(2026, 4, 8, 8, 0, 0)
    
    endpoints = ['/api/v1/auth/login', '/api/v1/auth/refresh', '/api/v1/auth/logout']
    normal_ips = [random_ip() for _ in range(253)]

    # Generate noise (normal traffic)
    for _ in range(16910):
        ip = random.choice(normal_ips)
        endpoint = random.choice(endpoints)
        method = random.choice(['POST', 'GET'])
        
        logs.append(LogEntry(
            timestamp=(start_time + timedelta(seconds=random.randint(0, 3600))).isoformat() + 'Z',
            ip=ip,
            endpoint=endpoint,
            method=method,
            status=random_status(),
            payload=generate_random_payload(is_flag=bool(random.getrandbits(1)))
        ))

    # Add the real attacker
    attacker_ip = random_ip()
    attacker_time = start_time + timedelta(seconds=random.randint(0, 1800))
    
    # Attacker fails 300 times (highest in the logs)
    for i in range(341):
        logs.append(LogEntry(
            timestamp=(attacker_time + timedelta(seconds=i)).isoformat() + 'Z',
            ip=attacker_ip,
            endpoint='/api/v1/auth/login',
            method='POST',
            status=401,
            payload=generate_random_payload(is_flag=False)
        ))

    # Attacker finally succeeds
    real_flag = generate_random_payload(is_flag=True)
    target_time = attacker_time + timedelta(seconds=301)
    logs.append(LogEntry(
        timestamp=target_time.isoformat() + 'Z',
        ip=attacker_ip,
        endpoint='/api/v1/auth/login',
        method='POST',
        status=200,
        payload=real_flag
    ))

    # Sort logs by timestamp to make them chronological
    logs.sort(key=lambda x: x.timestamp)
    log_dicts = [asdict(entry) for entry in logs]

    with open('logs.json', 'w') as f:
        json.dump(log_dicts, f, indent=4)

    print(f'Generated logs.json with {len(logs)} entries.')
    print(f'DEV HINT: Attacker IP is {attacker_ip}')
    print(f'DEV HINT: Real Flag is {base64.b64decode(real_flag).decode("utf-8")}')

if __name__ == '__main__':
    main()
