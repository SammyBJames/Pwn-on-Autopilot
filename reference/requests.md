# HTTP Requests

The `requests` library is arguably the most important third-party Python package for cybersecurity.

## Making Requests
You can make requests using any HTTP method.

```python
import requests

# Standard GET request
r1 = requests.get('https://httpbin.org/get')

# Other methods
r2 = requests.post('https://httpbin.org/post')
r3 = requests.put('https://httpbin.org/put')
r4 = requests.delete('https://httpbin.org/delete')
```

## Handling the Response
The response object contains everything the server sent back.

```python
r = requests.get('https://httpbin.org/get')

# HTTP status code (e.g., 200, 404, 500)
print(r.status_code)

# The response body as a string.
# Does not work for binary data!
print(r.text)

# The response body as raw bytes (binary)
print(r.content)

# The HTTP headers returned by the server (case-insensitive dictionary)
print(r.headers)
print(r.headers['Content-Type'])

# The JSON response body deserialized to a Python dictionary
# Does not work if the response is not JSON!
data = r.json() 
```

## Changing Headers
Many targets block default scripts by checking the `User-Agent`. You can perfectly spoof browsers or add authorization headers by passing a dictionary to the `headers` parameter.

```python
custom_headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)',
    'Authorization': 'Bearer eyJhbGci...'
}

r = requests.get('https://httpbin.org/headers', headers=custom_headers)
```

## Sending Data (POST/PUT)
There are two primary ways to send data in a request, depending on what the server expects:

**1. Form Data (`data=`)**
Used for traditional HTML login forms (`application/x-www-form-urlencoded`).
```python
login_info = {'username': 'admin', 'password': 'password123'}
r = requests.post('https://httpbin.org/post', data=login_info)
```

**2. JSON Data (`json=`)**
Used for modern APIs (`application/json`). Automatically converts your dictionary to a JSON string.
```python
login_info = {'username': 'admin', 'password': 'password123'}
r = requests.post('https://httpbin.org/post', json=login_info)
```

`requests` automatically sets the `Content-Type` header based on the parameter you use.

## Sessions (Automating Cookies)
`requests` can manage your session for you so any cookies returned from the server are automatically stored. For subsequent requests, your browser sends those cookies back to prove you are authenticated. 

If you use `requests.get()` and then `requests.post()`, they are completely separate! To maintain cookies automatically across multiple requests (like a real browser), use a `Session`.

```python
# Create a session object
s = requests.Session()

# 1. Log in using .post() on the session (session saves the cookie)
s.post('http://target.local/login', data={'user': 'admin', 'pass': '1234'})

# 2. Access a protected page (session sends the cookie back)
r = s.get('http://target.local/dashboard')
print(r.status_code)
print(r.text)
```

## Error Handling
Always prepare for dropped connections and timeouts.

```python
try:
    r = requests.get('http://target.local')
except requests.exceptions.Timeout:
    print('The server took too long to respond.')
except requests.exceptions.ConnectionError:
    print('Failed to connect to the server (port might be closed).')
```

## Advanced Options

**Stopping Redirects (`allow_redirects=False`)**
By default, `requests` automatically follows HTTP 3xx redirects. You might want to read the `Location` header of the 302 response (e.g., in OAuth token stealing or SSRF testing) rather than ending up at the final destination, so we can inspect the intermediate response rather than the final one.

```python
r = requests.get('http://target.local/login', allow_redirects=False)
print(r.status_code) # 302
print(r.headers['Location']) # Where it tried to send you
```

**File Uploads (`files=`)**
We can use the `files` parameter to upload files in a `multipart/form-data` POST request. The value should be a dictionary where the key is the form field name and the value is a tuple containing the filename, file object, and content type.

```python
# The format is 'form_field_name': ('filename', file_object, 'content-type')
upload = {'avatar': ('shell.php', open('shell.php', 'rb'), 'application/x-php')}
r = requests.post('http://target.local/upload', files=upload)
```

**Timeouts (`timeout=`)**
By default, `requests` will hang **forever** if the server stops answering but keeps the socket open. Always specify a timeout, especially when brute-forcing.

```python
# 5 seconds for the whole process
r = requests.get('http://target.local', timeout=5)

# Tuple: (connect_timeout, read_timeout)
r = requests.get('http://target.local', timeout=(3.0, 10.0)) 
```

**HTTP Basic Authentication (`auth=`)**
If a target is protected by `Authorization: Basic` headers, you don't need to base64 encode it yourself. `requests` handles it with a tuple.

```python
# Automatically base64 encodes the username:password and adds the header
r = requests.get('http://router.local/admin', auth=('admin', 'password123'))
```

**Accessing Specific Cookies**
While `Session` objects handle cookies automatically, sometimes you just need to grab a specific cookie value (like a CSRF token) to use elsewhere.

```python
r = requests.get('http://target.local/login')
# r.cookies is a RequestsCookieJar, behaves like a dictionary
csrf_token = r.cookies.get('csrf_token') 
```

**Retries on Failure**
`requests` doesn't retry failed connections by default. You can mount an adapter to a Session so it automatically retries multiple times before crashing:
```python
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

s = requests.Session()
# Retry 3 times, with a backoff factor to delay between attempts
retries = Retry(total=3, backoff_factor=1, status_forcelist=[500, 502, 503, 504])
s.mount('http://', HTTPAdapter(max_retries=retries))
```

**Prepared Requests - God Mode**
Sometimes you need to see *exactly* what bytes Python is about to put on the wire, or modify a header that `requests` manages. You can break the request process into two steps:

```python
# Prepare the request first without sending it
s = requests.Session()
req = requests.Request('POST', 'http://target.local', data={'key':'value'})
prepared = req.prepare()

# Now you can inspect or mangle the raw prepared request before sending
print(prepared.headers)
print(prepared.body)
prepared.headers['Content-Type'] = 'application/x-custom-malformed-data'

# Then send it
r = s.send(prepared)
```

## Intercepting with Burp Suite / ZAP
When writing exploits, you often want to send your Python script's traffic through Burp Suite to inspect it. You must define a `proxies` dictionary and disable SSL verification using `verify=False` (since Burp uses a self-signed certificate).

```python
# Ignore the annoying InsecureRequestWarning when verify=False
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

burp = {'http': 'http://127.0.0.1:8080', 'https': 'http://127.0.0.1:8080'}

r = requests.get('https://target.local', proxies=burp, verify=False)
```
