# Speaker Notes: Pwn on Autopilot

## Intro

### 1. Agenda
- Set up `uv` and cover its features
- Review some Python basics
- Libraries
    - Data formats
    - Web requests
    - Web scraping
    - Creating CLI tools
    - Binary exploitation with `pwntools`
- Briefly talk about scripting with AI
- Work on challenges!

### 2. Expectations
- This workshop is targeted at beginners with some coding experience
- If you are an advanced programmer, you'll probably find the content basic and boring, though you can stick around and work through some of the challenges!
- This is by no means comprehensive and is meant to be a starting point to jump into scripting for cyber.
- The first hour I'll intro you to the tools and then the second hour I've got challenges for you to work on.
- Ask your questions!

### 3. Repo
- The workshop repo has the "slides", commands to copy, the examples we'll work on, and reference guides with more info about the topics.
- It will also have the challenge code and writeups after the workshop ends.

### 4. Survey
- On a scale of 1-5, how comfortable are you with Python?
- How many of you have used `uv`?

## Setup `uv`

### 1. What is uv
- uv is a python project and environment manager that is way easier than other options
- It handles virtual environments, dependencies, and running temporary scripts quickly

### 2. Install uv

```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

### 3. Initialize the Project

```bash
uv init --bare --python 3.13 --pin-python
```

### 4. Install Packages

```bash
uv add requests beautifulsoup4 pwntools
```

- Sets up the venv automatically
- Find packages on PyPI

### 5. Run Scripts

```bash
uv run main.py
```

- Automatically runs within the `.venv` context

### 6. uv Extras

- Run without setting up a project:

    ```bash
    uv run --with requests main.py
    ```

    - Installs from cache, runs, and throws the environment away.

- Run tools with `uvx`:

    ```bash
    uvx sqlmap -u http://inmt.win
    ```

    - Standalone execution: Run CLI tools without cluttering your system (like `npx`).

## The Basics

### 1. Reading Files
- Use `with open()`
- Modes:
    - `r` = read text
    - `rb` = read binary
    - `w` = write text (overwrites)
    - `wb` = write binary (overwrites)
    - `a` = append text
    - `ab` = append binary

### 2. Strings vs Bytes
- Strings and bytes are treated differently in Python
- Strings are human-readable, bytes can be any data
- Byte objects look like strings but have are prefixed with 'b'
- Binary files must be read with `b` mode to avoid decoding errors
- Use `.encode()` to convert strings to bytes and `.decode()` to convert bytes to strings
- Use `.hex()` to get a hex representation of bytes, and `bytes.fromhex()` to convert hex back to bytes
- Byte objects are immutable, so if you want to modify them, convert to a `bytearray` instead

### 3. Handle Errors!
- Use `try`/`except` blocks to handle errors (no `catch`)
- In cyber, things are unpredictable so handle errors and log what happened for debugging

## Libraries

### 1. Base64

#### 1. Intro to Base64
- Base64 encoding is everywhere! Know how to recognize it! (= and chars)
- Python has a built in `base64` module to deal with it
- It accepts and returns bytes, not strings!

#### 2. Encoding and Decoding
- `examples/starter/base64_example.py`

    ```python
    import base64

    message = 'pwn_on_autopilot_base64_demo'

    # Encode the message to bytes first
    message_bytes = message.encode('utf-8')

    # Base64 encode the message
    encoded_bytes = base64.b64encode(message_bytes)

    # Print the encoded result
    print(f'Encoded: {encoded_bytes}')

    # Base64 decode it back
    decoded_bytes = base64.b64decode(encoded_bytes)

    # Convert back to human-readable string
    decoded_str = decoded_bytes.decode('utf-8')

    # Print the decoded result
    print(f'Decoded: {decoded_str}')
    ```

#### 3. URL Safe Base64
- If we want to send base64 for web requests, we need to use URL-safe base64.
- `urlsafe_b64encode` instead of `b64encode`

### JSON

### 1. Intro to JSON
- JSON is even more common than base64, especially for any web hacking
- Python also has a built in `json` module for JSON data

### 2. Serializing and Deserializing
- We call converting JSON data serializing and deserializing.
- Serializing is converting objects into JSON strings
- Deserializing is converting JSON strings back into Python objects
- After deserializing, we get a dictionary that we can manipulate and then serialize again afterwards
- In Python, we have two different functions for both serializing and deserializing:
    - `json.loads()` and `json.dumps()` for strings
    - `json.load()` and `json.dump()` for files

- `examples/starter/1_data.json`
    ```python
    import json

    # Load the data from 1_data.json
    # We use .load() because we are reading from a file object
    with open('1_data.json') as f:
        data = json.load(f)

    # Print the admin's password from the dictionary
    print(f'Admin password: {data["credentials"]["admin"]}')

    # Add a new user 'backdoor' with password 'pwned'
    data['credentials']['backdoor'] = 'pwned'

    # Save the modified data to a file called 1_modified.json
    with open('1_modified.json', 'w') as f:
        json.dump(data, f, indent=4)

    ```

## Requests

### 1. Intro to Requests
- The `requests` library is a simple and powerful way to work with HTTP.
- We can send any type of request, manipulate headers, handle sessions, etc.

### 2. Make Requests and Handle Responses
- `examples/starter/2_requests_basics.py`

    ```python
    import requests

    # Send a GET request to https://httpbin.org/json
    response = requests.get('https://httpbin.org/json')

    # Print the status code and the response text
    print('Status Code:', response.status_code)
    print('Response Text:', response.text)

    # Print the response content as bytes
    print('Response Content (bytes):', response.content)

    # Print the response body as JSON
    print('Response JSON:', response.json())

    # Send a POST or PUT request to https://httpbin.org/post and print the status code
    post_response = requests.post('https://httpbin.org/post')

    # Print the status code of the POST request
    print('POST Status Code:', post_response.status_code)
    ```

- Throws `requests.exceptions.JSONDecodeError` if you try to parse non-JSON response with `.json()`
- If data is binary, `.text` will not work!  

### 3. Sending Data and Headers
- In cyber, we need to manipulate requests, sending malicious payloads, custom headers, things to cause problems!
- `examples/starter/3_requests_data.py`

    ```python
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
    ```

### 4. Sessions and Cookies
- With web hacking, we will need to maintain cookies and sessions to stay authenticated and access protected routes.
- `requests` gives us a `Session` object that keeps track of cookies for us so we don't have to handle them manually.
- We can then call our request methods on the session object.
- `examples/starter/4_requests_sessions.py`

    ```python
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
    ```

## BeautifulSoup

### 1. Intro to BeautifulSoup
- We now know how to get data from the web, and we can handle JSON, but what about HTML?
- We want to "web scrape" and parse HTML to extract specific pieces of data.
- We could use a regex or search for specific strings in the response text, but that is tedious and unreliable.
- `BeautifulSoup` is a library that allows us to parse HTML and easily data from HTML.
- We first parse the HTML into a tree, like the DOM in the browser, and then we can navigate through it using selectors and methods.

### 2. Parse HTML and Extract Data
- `examples/starter/5_bs4_example.py`
    ```python
    import requests
    from bs4 import BeautifulSoup

    # Fetch the content of a form page
    response = requests.get('http://quotes.toscrape.com/login')

    # Parse the page content with BeautifulSoup
    soup = BeautifulSoup(response.text, 'html.parser')

    # Extract the CSRF token from the page and print it
    csrf_input = soup.find('input', {'name': 'csrf_token'})
    csrf_token = csrf_input.get('value')
    print(f'CSRF Token: {csrf_token}')
    ```

### 3. Navigating the HTML Tree
- These methods let us navigate through the HTML tree:
    - `find()` and `find_all()` to search for tags with specific attributes
    - `.parent` to get the parent element
    - `.children` to get the child elements
    - `.next_sibling` and `.previous_sibling` to navigate between siblings
    - `.select_one()` and `.select()` to use CSS selectors to find elements

## Argparse

### 1. Intro to Argparse
- `argparse` is a built in library for handling command line arguments and options
- We will eventually need to create reusable tools or send different payloads to the same target, so we can set up our script as a CLI tool with `argparse` to change parameters quickly.
- We want to pass arguments on the command line like `uv run tool.py target.com -w wordlist.txt -v`

### 2. Create a CLI Tool
- `examples/starter/6_argparse_example.py`
    ```python
    import argparse

    # Initialize an ArgumentParser
    parser = argparse.ArgumentParser(description='Basic web content scanner')

    # Add a required positional argument for the 'target' URL
    parser.add_argument('target', help='The target URL')

    # Add an optional flag '-w' / '--wordlist' with a default value of 'common.txt'
    parser.add_argument('-w', '--wordlist', default='common.txt', help='Path to wordlist')

    # Add an boolean option '-v' / '--verbose' using action='store_true'
    parser.add_argument('-v', '--verbose', action='store_true', help='Show all attempts')

    # Parse the arguments
    args = parser.parse_args()

    print(f'\nStarting attack against: {args.target}')
    print(f'Loading wordlist: {args.wordlist}')

    if args.verbose:
        print('Verbose logging ENABLED. Showing all failed attempts.')
    else:
        print('Verbose logging DISABLED. Only showing successful hits.')
    ```

## Pwntools

### 1. Intro to Pwntools
- `pwntools` was built for CTFs to solve binary exploitation challenges, so it is great at quickly developing and testing exploits
- `pwntools` is massive and has so many features I can't even pretend to know all of them.
- It gives us lots of options for analyzing binaries, creating payloads, and sending them to the target

### 2. Tubes
- One of the big advantages of `pwntools` for CTFs is that it allows us to easily interact with both local processes and remote services using the same logic.
- We use a "tube" object to represent our connection to the target, and we can send and receive data through it.
- That means we can develop our payload locally and then just switch the target with a single line (or CLI arg) to run it against the real target.
- `pwntools` also uses bytes rather than strings
- `examples/starter/7_pwntools_example.py`

    ```python
    from pwn import *

    # Connect to a local binary
    # r = process('./7_vuln')
    # Or connect to the remote server
    r = remote('target.inmt.win', 1337)

    # Consume output until the server sends "Username: "
    r.recvuntil(b'Username: ')

    # Send the username "admin"
    r.sendline(b'admin')

    # Read the next output line and save it to a variable called `response`
    response = r.recvline()

    # Consume output until "Password: " then send the password "password123"
    r.sendafter(b'Password: ', b'password123')

    # Drop into an interactive shell
    r.interactive()
    ```

### 3. Advanced Features
- `pwntools` has a lot of features for analyzing binaries, creating payloads, and exploiting them.
- It has built in functions for packing and unpacking data
- It has a powerful `ELF` class for analyzing ELF binaries and their symbols
- It has a `ROP` class for creating ROP chains
- Cover reference doc for `pwntools`

## Scripting with AI
- **Verify Everything!:** If you let an LLM loose without supervision, it will cause you more harm than good. Always review all output carefully.
- **Generate Boilerplate & Scaffold:** Never start from an empty file. Describe how the script should work, and let your LLM set up the project structure.
- **Parsing:** Give the LLM a sample of the data and have it write the parser for you. Doing tedious tasks like this manually is a waste of time.
- **Explaining & Deobfuscating:** Paste in confusing code or data and ask it to explain to you the logic or structure. Once you understand your target, you can better focus your exploits.
- **Refactoring:** If you have a working prototype, give it to the LLM and ask it to make it faster or more efficient. For certain tasks, speed is critical.
- **Debugging:** When you get an error, give it to an LLM with your project context and it will usually be able to decipher the message and point you in the right direction.

## Challenges
- The best way to learn is by doing!
- Solve the challenges using the skills we've covered **and the reference materials in the repo.**
- There is one challenge where you'll need to find the right tool or package to solve, but other than that the tools you need are covered.
- I'd recommend going through the challenges on your own without an LLM. You can use one if you like, but you'll learn a lot more without it. I didn't build the challenges to be AI-resistant, so dumping them into Gemini will probably get you a working answer pretty quick.
