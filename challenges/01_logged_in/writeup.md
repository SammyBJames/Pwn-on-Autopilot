# Logged In Write Up

## Why Scripting?
The provided `logs.json` contains over 17,000 entries. It would be quite difficult to track down the attacker without creating a script of some sort, especially with the payloads being encoded with base64. 

Shell tools are also not ideal for this challenge because of the sheer volume of data and the fact that we need to correlate multiple fields across multiple entries. A Python script allows us to easily load the data, filter it based on our criteria, and identify the attacker and extract the flag.

## Intended Solution

To solve this challenge, we need to transition from staring at a massive wall of JSON text to logically filtering the data with Python. 

### 1. Exploring the Endpoints
We know that the attack was against the authentication API, so let's first check what endpoints are present in the logs to identify what the login endpoint is called. We can load the JSON file and extract all unique endpoints to get a sense of the API structure.

```python
import json

with open('logs.json') as f:
    logs = json.load(f)

endpoints = set([entry['endpoint'] for entry in logs])
print(endpoints)
```

We get a set `{'/api/v1/auth/login', '/api/v1/auth/refresh', '/api/v1/auth/logout'}`. The login endpoint is `/api/v1/auth/login`, so we can focus on that when counting failed login attempts.

### 2. Checking Login Attempts
A brute-force attack involves many failed login attempts followed (potentially) by a success. When authentication fails, the standard is for the REST API to return a `401 Unauthorized` response. 

Let's count how many times each IP address receives a `401` on the login endpoint. We can use a dictionary (hashmap) to keep a running tally:

```python
failed_logins = {}
for entry in logs:
    if entry['endpoint'] == '/api/v1/auth/login' and entry['status'] == 401:
        ip = entry['ip']
        failed_logins[ip] = failed_logins.get(ip, 0) + 1
```

### 3. Identifying the Bad Actor
Our `failed_logins` dictionary now contains the failed attempt counts for every IP address. Let's take a look at the results so we can identify a baseline and look for anything abnormal.

```python
for ip, count in failed_logins.items():
    print(f'{ip.ljust(16)}: {str(count).rjust(4)} failed logins')
```

If we look through our results, we see an average of 3-8 failed attempts per IP, but one IP stands out with 341 failed logins: `230.104.94.17   :  341 failed logins`. This is our attacker!

### 4. Extracting the Payload
Now that we know the attacker's IP, we need to find their successful login attempt. We can filter our entries originating from the attacker's IP that resulted in a `200 OK` response.

Once we find that successful entry, we extract the `payload` value. We can then decode that payload from base64 to get the flag.

```python
for entry in logs:
    if entry['ip'] == attacker_ip and entry['status'] == 200:
        payload = entry['payload']
        decoded_flag = base64.b64decode(payload).decode('utf-8')
        print(f'Flag: {decoded_flag}')
        break
```

## Solution Script

```python
import json
import base64


def solve():
    # Load the data from our logs file
    with open('logs.json') as f:
        logs = json.load(f)
    print(f'Loaded {len(logs)} log entries.')

    # Count failed logins per IP
    failed_logins = {}
    for entry in logs:
        # Only check requests to the login endpoint that resulted in a 401 Unauthorized
        if entry['endpoint'] == '/api/v1/auth/login' and entry['status'] == 401:
            ip = entry['ip']
            failed_logins[ip] = failed_logins.get(ip, 0) + 1

    # Check failed login counts for all IPs
    # for ip, count in failed_logins.items():
    #     print(f'{ip.ljust(16)}: {str(count).rjust(4)} failed logins')

    # Find the IP with the most failures
    attacker_ip = max(failed_logins, key=failed_logins.get)
    print(f'Attacker IP: {attacker_ip} with {failed_logins[attacker_ip]} failed attempts.')

    # Search for that attacker's successful payload
    for entry in logs:
        if entry['ip'] == attacker_ip and entry['status'] == 200:
            payload = entry['payload']
            # Decode the flag (base64 is bytestring)
            decoded_flag = base64.b64decode(payload).decode('utf-8')
            print(f'Flag: {decoded_flag}')
            break


if __name__ == '__main__':
    solve()
```
