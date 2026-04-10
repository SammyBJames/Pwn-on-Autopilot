# Chain Reaction Write Up

## Why Scripting?
The challenge requires us to iterate through over many dynamically generated API endpoints. The path to the next endpoint is hidden within a JSON response filled with noise, and the key identifying the next path changes periodically (`next`, `next_url`, `location`). Finally, near the end, some paths are intermittently encoded in base64. Attempting to go through this by hand would take forever. Scripting allows us to automate the iteration, account for the changing keys, decode the base64 paths dynamically, and find the flag fast.

## Intended Solution

### 1. Initial Request
Let's first take a look at the initial response with the browser. We receive a response with a few pieces of irrelevant data (like `request_time` and `request_id`) and a key named `next` that contains what looks like a URL path.

If we follow that path, we get a similar response with a new `next` path, same for the next path, and so on. We can see that the server is shuffling us around to a new path with every new route we try. Let's set up a script to go through all these paths for us and look for anything interesting.

### 2. Setting Up a Loop
Since we don't know exactly how many endpoints there are, we can set up a `while True` loop to continuously fetch the next path. We'll extract the JSON data and pull the next path from the `next` key. We don't know if this is sending us in a cycle, so if it runs for more than a few seconds, we can kill it and track which routes we've visited in a `set` so we know we aren't going in circles.

```python
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

        # Check for no next path
        if 'next' not in data:
            print('Could not find a next path in the response.')
            print(f'Response: {res.text}')
            break

        # Extract the next path
        path = data['next']
```

### 3. Handling Changing Keys
We run our script, and eventually it fails on one of the requests. Looking at the response we have, we can see that the key for the next path has changed to `next_url`.

Let's define a list of possible keys and check all of them to find the next path, instead of hardcoding `'next'`.

```python
# Parse the JSON response
data = res.json()

# Extract the next path using the possible keys
next_path = None
possible_keys = ['next', 'next_url']
for key in possible_keys:
    if key in data:
        next_path = data[key]
        break

# No next path found
if not next_path:
    print('Could not find a next path in the response.')
    print(f'Response: {res.text}')
    break

# Queue it up for the next iteration
path = next_path
```

When we rerun our script, we again eventually fail on a request, and this time the response contains a key named `location` with our next path! Let's add that to our list of possible keys and move along. If we keep running into switching keys, we could add some logic to figure out which key is not in the standard set and select that route automatically, but in this case it turns out we just have to handle these three.

# 4. Decoding Base64

After another run, we again fail, but this time it's a `requests.exceptions.InvalidURL` error. Looking at the response, we see that the next path doesn't contain a leading slash. We can see an '=' character at the end of the string, a telltale sign of base64! Let's try base64 decoding the path and trying that.

After decoding, we get a valid path with a leading slash that leads us to a new route! Let's add some logic to handle base64 encoding dynamically. If the next path doesn't start with a slash, we can attempt to decode it as base64 and use that as our next path instead. 

```python
if not next_path.startswith('/'):
    next_path = base64.b64decode(next_path).decode('utf-8')
```

Our script fails one last time, but this time we get a key named `flag` in the response!

## Solution Script

```python
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
```
