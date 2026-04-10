import base64
import requests


def solve():
    url = 'https://api.inmt.win'
    path = '/'

    while True:
        # Get the next page
        print(f'Fetching: {url}{path}')
        res = requests.get(f'{url}{path}')

        # Break if our response is not 200 OK
        if res.status_code != 200:
            print(f'Got non-200 response: {res.status_code}')
            print(f'Response: {res.text}')
            break

        # Parse the JSON response
        data = res.json()

        # Extract the next path using the possible keys
        next_path = None
        possible_keys = ['next', 'next_url', 'location']
        for key in possible_keys:
            if key in data:
                next_path = data[key]
                break

        # No next path found
        if not next_path:
            print('Could not find a next path in the response.')
            print(f'Response: {res.text}')
            break

        # Check if next path is base64-encoded (doesn't start with a slash)
        if not next_path.startswith('/'):
            next_path = base64.b64decode(next_path).decode('utf-8')

        # Queue it up for the next iteration
        path = next_path


if __name__ == '__main__':
    solve()
