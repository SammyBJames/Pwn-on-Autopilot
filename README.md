# Pwn on Autopilot: Python for Hackers
**Sam Bradley**

[![License](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)

## Overview
This workshop aims to teach beginner to intermediate learners how to speed up their hacking using Python and some common libraries for cybersecurity and provides you with several challenges to gain experience and hone your skills. The workshop will be broken down into the following sections:

1. **Setup:**
    - Install `uv`
    - Create a project / virtual environment
    - Install packages (PyPI)

2. **Review Basics:**
    - File operations (text/binary, operating modes)
    - Error handling
    - Bytes and byte arrays

3. **Libraries:**
    - `base64` for B64 encoding/decoding
    - `json` for working with JSON data
    - `requests` for HTTP interactions
    - `beautifulsoup4` for parsing HTML
    - `argparse` for command-line interfaces
    - `pwntools` for CTFs and network interactions

4. **AI for Scripting:**
    - Use AI to speed up scripting without getting off-track

5. **Practice:**
    - Work on challenges to apply what you've learned and gain experience

## Setup
uv is a modern Python package and project manager written in Rust, much faster and simpler than alternatives. It will automatically manage Python, a virtual environment, and your dependencies for you.

1. **Install `uv`:**

    **macOS, Linux, and WSL:**
    ```bash
    curl -LsSf https://astral.sh/uv/install.sh | sh
    ```

    **Windows:**
    ```powershell
    powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"
    ```

2. **Initialize project:**

    ```bash
    uv init --bare
    ```

    For this workshop:

    ```bash
    uv init --bare --python 3.13 --pin-python
    ```

3. **Install packages:**

    ```bash
    uv add requests beautifulsoup4 pwntools
    ```

    Find more packages on [PyPI](https://pypi.org/).

4. **Run your Python script:**

    ```bash
    uv run <script-name>.py
    ```

5. **More information:**

    uv is a very powerful tool with many features beyond just these basics. To explore more features, look at the [uv Reference](reference/uv.md) in this repository.

## Basics

### File Operations
For Python file operations, always use the `with open()` context manager. It automatically closes the file for you when the block is finished, preventing locked files or memory leaks.

**File Modes:**
- `r`: Read (default). Fails if the file doesn't exist.
- `w`: Write. Overwrites existing files or creates new ones.
- `a`: Append. Adds to the end of an existing file or creates a new one.
- `b`: Binary modifier (e.g., `rb` or `wb`). Skips text decoding and reads/writes raw bytes.

**Writing Text:**

```python
with open('notes.txt', 'w') as f:
    f.write('Pwn on Autopilot\n')
    f.write('I ❤️ File Operations!')
```

**Reading Binary (Strings vs. Bytes):**
You will often deal with binary files: images, compiled executables, packet captures, raw payloads, etc. Opening these as text (`r`) will crash your script with a decoding error. Use `rb` to safely read them as raw bytes.

```python
with open('file.bin', 'rb') as f:
    data = f.read()
    print(type(data))
    print(data)
```

For more on file operations, see the [Files Reference](reference/files.md).

### Error Handling
In cyber, we often deal with unpredictable targets and data. Servers timeout, files contain bad bytes, etc. Instead of letting your script crash halfway through an attack, handle your errors with `try`/`except` and log errors for debugging and analysis.

```python
try:
    # Attempt a risky operation
    print(10 / 0)
except ZeroDivisionError:
    # Handle the specific error so the script survives
    print('Math error caught. Moving on to the next target!')
```
For a deeper dive into error handling, check out the [Errors Reference](reference/errors.md).

### Bytes
You will constantly work with raw bytes when dealing with network packets, compiled binaries, shellcode, and cryptography.

**Strings vs. Bytes:**
- **Strings (`str`):** Human-readable text (`'admin'`).
- **Bytes (`bytes`):** Raw machine data represented as integers from 0 to 255 (`b'admin'` or `b'\x41'`).
You cannot mix them directly; you must `.encode()` strings to bytes or `.decode()` bytes to strings.

**Hexadecimal:**
Binary data is often represented as hex. Python makes it easy to convert back and forth without messy loops:

```python
payload = b'\xca\xfe\xba\xbe'
hex_payload = payload.hex() # 'cafebabe'

converted_back = bytes.fromhex(hex_payload) # b'\xca\xfe\xba\xbe'
```

**Byte Arrays:**
`bytes` are immutable (unchangeable). If you are constructing or mutating an exploit dynamically, convert it to a `bytearray`:

```python
mutable = bytearray(b'\x41\x41\x41\x41') # bytearray(b'AAAA')
mutable[0] = 0x42  # Overwrite first byte: bytearray(b'BAAA')
```

For more details, see the [Bytes Reference](reference/bytes.md). You can also learn about structured packing and unpacking of binary data using `struct` in the [Struct Reference](reference/struct.md).

## Libraries

This section introduces you to some of the most critical Python libraries for automation and exploit development. This section makes up the bulk of the presentation part of the workshop. We will be working with the code in the `examples` folder. You can follow along using the starter templates in `examples/starter` or jump to the completed code in `examples/complete`.

### `base64`
Base64 encoding is everywhere in cybersecurity: HTTP Basic Auth, JSON Web Tokens (JWTs), email attachments, and encoded reverse shells. Python’s built-in `base64` module handles this natively. 

The key thing to remember about `base64` in Python 3 is: **It requires and returns `bytes`, not `str` (strings).**

```python
import base64

# Base64 encode the message (Remember to .encode() first!)
message_bytes = 'super_secret'.encode('utf-8')
encoded_bytes = base64.b64encode(message_bytes)

# Print the encoded result
print(encoded_bytes.decode('utf-8'))
```

For more info on standard and URL-safe base64 encoding, see the [Base64 Reference](reference/base64.md).

### `json`
JSON is the universal language of web APIs, configs, and tooling output (like BloodHound or Nmap). Python interacts with JSON out of the box with the `json` module.

The most important rule for the `json` library is the rule of "S" (String):
- `json.load()` / `json.dump()`: For reading/writing directly to **Files**.
- `json.loads()` / `json.dumps()`: For reading/writing from **Strings**.

```python
import json

# Reading from a file
with open('config.json', 'r') as f:
    data = json.load(f)

# Modifying the data since it's just a Python dictionary!
data['debug'] = True

# Overwriting the file with the new configuration
with open('config.json', 'w') as f:
    json.dump(data, f, indent=4)  # indent=4 pretty-prints it
```

For more info on handling JSON, see the [JSON Reference](reference/json.md).

### `requests`
The `requests` library is arguably the most important third-party Python package for hackers. Any web hacking will almost certainly involve `requests`.

```python
import requests

# Set custom headers
headers = {'User-Agent': 'Mozilla/5.0'}

try:
    # Make a simple GET request
    r = requests.get('https://httpbin.org/get', headers=headers)
    
    # Check the status code
    if r.status_code == 200:
        # Print the response text
        print(r.text)
    else:
        print(f'Unexpected status code: {r.status_code}')
except requests.exceptions.ConnectionError:
    print('Failed to connect to the target.')
```

`requests` can also handle sessions, automatically managing cookies across multiple requests (like logging in and accessing protected routes).

```python
# Use a Session to handle cookies between requests
s = requests.Session()
s.post('http://target.local/login', data={'user': 'admin', 'pass': '1234'})

# The session automatically sends the cookie with subsequent requests
r = s.get('http://target.local/dashboard')
```

To dive deeper, see the [Requests Reference](reference/requests.md).

### `BeautifulSoup` (`bs4`)
When writing web exploitation scripts, we need to interact with and extract data from HTML strings. `BeautifulSoup` turns HTML into cleanly searchable Python objects.

The two most common use cases are extracting CSRF tokens for brute-forcing scripts and scraping targets for links or hidden data.

```python
import requests
from bs4 import BeautifulSoup

r = requests.get('https://example.com/login')

# Parse the raw HTML text into a searchable object
soup = BeautifulSoup(r.text, 'html.parser')

# Look for a tag like: <input name="csrf_token" value="abc123xyz">
token_input = soup.find('input', {'name': 'csrf_token'})

if token_input:
    # Extract the 'value' attribute using .get()
    token = token_input.get('value')
    print(f'CSRF Token: {token}')
```

For more info, check out the [BeautifulSoup Reference](reference/bs4.md).

### `argparse`
When you want to test payloads fast, or build reusable tools, you need to stop hardcoding parameters. `argparse` is Python's built-in module for building proper CLIs. It automatically generates help menus (`-h`) and validates user input for you.

```python
import argparse

# Initialize the parser
parser = argparse.ArgumentParser(description='Web Exploitation Script')

# Add a required positional argument (order matters)
parser.add_argument('target', help='The target IP address or URL')

# Add an optional argument (starts with dashes)
parser.add_argument('-p', '--port', type=int, default=80, help='Target port')

# Add a boolean flag (true if passed, false otherwise)
parser.add_argument('-v', '--verbose', action='store_true', help='Enable verbose output')

# Parse the final arguments
args = parser.parse_args()

print(f'Target: {args.target}')
if args.verbose:
    print(f'Verbose mode ENABLED on port {args.port}')
```

For a deeper dive into validating files and options, check out the [Argparse Reference](reference/argparse.md).

### `pwntools`
`pwntools` is a CTF framework and exploit development library. It is a massive library that abstracts away the most frustrating parts of binary exploitation.

Its biggest feature is the "Tube." You can use the same script to attack a local binary (`process()`) or a remote server (`remote()`). This means you can write and test your exploit locally, then point it at the target with a single line change (or CLI arg).

```python
from pwn import *

# 1. Connect to the target (Change 'process' to 'remote' to launch against a real server)
target = process('./vulnerable_app')
# target = remote('10.10.10.50', 1337)

# 2. Wait exactly for the prompt (no sleep() needed!)
target.recvuntil(b'Enter Password: ')

# 3. Pack an integer into raw 32-bit Little-Endian bytes, instantly
payload = b'A' * 44 + p32(0xdeadbeef)

# 4. Send the payload with a newline (\n)
target.sendline(payload)

# 5. Drop straight into the hacked shell!
target.interactive()
```

Because this library is massive, check out the [Pwntools Reference](reference/pwntools.md) for more advanced features and techniques.

## AI for Scripting & Review
LLMs are incredible at speeding up scripting and generating code. They remove the friction of remembering syntax and let you focus on the logic of your attack. 

Here are my recommendations for how to use AI effectively when writing hacking scripts:

- **Verify Everything!:** If you let an LLM loose without supervision, it will cause you more harm than good. Always review all output carefully.
- **Generate Boilerplate & Scaffold:** Never start from an empty file. Describe how the script should work, and let your LLM set up the project structure.
- **Parsing:** Give the LLM a sample of the data and have it write the parser for you. Doing tedious tasks like this manually is a waste of time.
- **Explaining & Deobfuscating:** Paste in confusing code or data and ask it to explain to you the logic or structure. Once you understand your target, you can better focus your exploits.
- **Refactoring:** If you have a working prototype, give it to the LLM and ask it to make it faster or more efficient. For certain tasks, speed is critical.
- **Debugging:** When you get an error, give it to an LLM with your project context and it will usually be able to decipher the message and point you in the right direction.

For a full breakdown of my recommendations, see the [AI for Scripting Reference](reference/ai.md).
