import requests

# Create a Session to save our cookies
s = requests.Session()

# Get a cookie by visiting the cookie setting endpoint
s.get('https://httpbin.org/cookies/set/session/super_secret_token')

# Print the cookies saved in the Session
print(f'Cookies saved in the Session: {s.cookies.items()}\n')

# Verify the cookie is still there by visiting the cookies endpoint, which will return the cookies we sent to the server in the request
response = s.get('https://httpbin.org/cookies')

# Print the JSON response which shows the cookies we sent to the server
print(f'Cookies sent to the server: {response.json()}')
