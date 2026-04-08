import requests

headers = {
    'User-Agent': 'Pwn-on-Autopilot/1.0',
    'X-Custom-Header': 'Hello from Python'
}

data = {
    'username': 'admin',
    'password': 'password123'
}

# Make a POST request with the custom headers and JSON data
r = requests.post('https://httpbin.org/post', headers=headers, json=data, timeout=3)

# Prove that the server received our custom headers and data
response_data = r.json()

print('Headers sent to server:')
print(response_data['headers'])
print()
print('JSON Data sent to server:')
print(response_data['json'])
