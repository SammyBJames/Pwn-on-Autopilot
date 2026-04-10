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
