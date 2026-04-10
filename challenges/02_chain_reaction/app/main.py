import secrets
import time
import uuid
import random
import base64
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

app = FastAPI()

TOTAL_STEPS = 200
FLAG = 'bsides{s0m3th1ing5_0ff_w1th_th15_s1t3}'

# Static generation at startup ensures all players experience the same map concurrently
routes = ['/'] + [f'/{secrets.token_hex(random.randint(8, 16))}' for _ in range(TOTAL_STEPS)]
route_chain = {}

for i in range(TOTAL_STEPS):
    current_path = routes[i]
    next_path = routes[i + 1]

    if i < int(TOTAL_STEPS * 0.3):
        nav_key = 'next'
    elif i < int(TOTAL_STEPS * 0.6):
        nav_key = 'next_url'
    else:
        nav_key = 'location'

    # Encode 10% of the values in the last quarter to Base64
    nav_value = next_path
    if i >= int(TOTAL_STEPS * 0.75) and random.random() < 0.10:
        nav_value = base64.b64encode(next_path.encode('utf-8')).decode('utf-8')

    route_chain[current_path] = {
        'key': nav_key,
        'value': nav_value
    }

# Terminal destination contains the flag
route_chain[routes[-1]] = {
    'key': 'flag',
    'value': FLAG
}

@app.get('/{path:path}')
async def catch_all(_: Request, path: str):
    full_path = f'/{path}' if path else '/'

    if full_path not in route_chain:
        return JSONResponse(status_code=404, content={'error': 'Not found.', 'message': "We can't find the route you're looking for."})

    node = route_chain[full_path]
    
    # Generate noise
    noise_data = {
        'request_time': int(time.time() * 1000),
        'request_id': str(uuid.uuid4()),
        'status': '200 OK',
        'request_latency_ms': random.randint(20, 500)
    }

    # Insert our actual navigation key-value pair
    noise_data[node['key']] = node['value']

    # Randomize key ordering
    keys = list(noise_data.keys())
    random.shuffle(keys)
    shuffled_response = {k: noise_data[k] for k in keys}
    
    return shuffled_response
