# Speaker Notes: Pwn on Autopilot

## Section 0: Survey

- On a scale of 1-5, how comfortable are you with Python?
- How many of you have used `uv`?

- Cover the agenda and open questions.

## Section 1: Setup & `uv`

### Why `uv`?
- **Problem:** Manage packages for a Python project without conflicts in global scope.
- **Problem:** Python environments (`pip`, `venv`, PATH) break easily and frustrate beginners.
- **Solution:** `uv` makes venvs easy and gets out of the way!

### 1. Project Setup
- **[RUN]** Initialize project.

    ```bash
    uv init --bare
    ```

    - Creates `pyproject.toml` and `uv.lock`

- **[SHOW]** [PyPI.org](https://pypi.org/) -> Search for `requests`. 

- **[RUN]** Install package.

    ```bash
    uv add requests
    ```

    - Creates `.venv` instantly and installs package

- **[WRITE]** `hello.py` with import and print statement.

    ```python
    import requests


    print('Hello, world!')
    ```

- **[RUN]** Run the script.

    ```bash
    uv run hello.py
    ```

    - Automatically runs within the `.venv` context, no activation needed!
    - Does not fail on importing `requests`.

### 2. uv Extras

We want to make it easy to test out libraries without installing them globally or even in our project.

- **[WRITE]** `solve.py` with import and print statement.

    ```python
    import pwntools


    print('Successfully imported pwntools!')
    ```

- **[RUN]** Run `solve.py`.

    ```bash
    uv run --with pwntools solve.py
    ```

    - Installs from cache, runs, and throws the environment away.

- **[RUN]** Show uvx with `sqlmap`.

    ```bash
    uvx sqlmap -u http://target.local
    ```

    - Standalone execution: Run Python CLI tools without cluttering your system (like Node's `npx`).

## Section 2: File Operations

### 1. Reading and Writing Text
Quickly remind the audience how to read/write files and the importance of the `b` modifier for binary data.

### 2. The `b` Modifier (Strings vs. Bytes)
Non-text files (executables, payloads, dumps) WILL crash Python using the standard read mode (`r`) because Python tries to decode them as UTF-8 text. We must use the `b` (binary) modifier! If lost:

- **[WRITE]** `binary.py`: Read an image from disk.

    ```python
    # Read binary back
    with open('happy.jpg', 'rb') as f:
        data = f.read()
        print(type(data))
        print(data)
    ```

- **[RUN]** `uv run binary.py`
- **[SHOW]** Point out the `<class 'bytes'>` type and the `b` prefix in the output (`b'\xde\xad\xbe\xef'`).
    - Strings and bytes are different!

## Section 3: Error Handling

### 1. The Hacker Mindset (EAFP)
In cyber, targets are unpredictable. Rather than constantly checking conditions before acting ("Look Before You Leap"), Ask for Forgiveness Rather than Permission. Don't let your script running for 10 hours die! Print errors and variables to debug and find next steps.

- **[WRITE]** `errors.py`: Show how a script completely survives a crash.

    ```python
    try:
        print('Sending payload...')
        1 / 0  # Simulating a crash, like a dropped connection
    except ZeroDivisionError:
        print('Payload failed, but the script keeps scanning!')
    ```

- **[RUN]** `uv run errors.py`
- **[SHOW]** The script finishes completely and never shows a giant red stack trace.

## Section 4: Byte Manipulation

### 1. Strings vs. Bytes
Strings are for human-readable text (`'admin'`), and bytes are for machine data / payload numbers (`b'\x41'`). Note that `\x41` is literally just the integer `65` beneath the hood. You cannot directly mix or concatenate them (`'flag: ' + b'\x41'` throws a `TypeError`). Always `.encode()` or `.decode()`.

### 2. Live Coding Bytes
- **[WRITE]** `bytes.py`: Show encoding and the hacker's best friend (`hex`).

    ```python
    text = 'secret_payload'
    
    # Needs to be encoded for the network socket!
    raw = text.encode('utf-8')
    print(raw)
    
    # Hex representation is a hacker staple for moving payloads
    print(raw.hex())
    print(bytes.fromhex('deadbeef'))
    ```

- **[RUN]** `uv run bytes.py`

### 3. The `bytearray` Solution
- **Explain:** Like strings, standard `bytes` are immutable! If you need to change the 4th byte of a saved 500-byte exploit payload, you must use a `bytearray`.
- **[WRITE]** `bytes.py`: Modify your script to use a `bytearray`.

    ```python
    payload = bytearray(b'\x41\x41\x41\x41')
    
    # Modifying in place requires passing the integer (0-255)
    payload[0] = 0xcc  
    payload.append(0x90)
    
    # Cast back to immutable bytes if required
    print(bytes(payload))
    ```

- **[RUN]** `uv run bytes.py`
- **[SHOW]** The output showing `b'\xccAAA\x90'`, proving we mutated the payload cleanly in place!

## Section 5: Libraries - `base64`

### 1. Intro to Base64
- **Explain:** Base64 is ubiquitous in cyber (HTTP Basic Auth, JWTs, payloads).
- **Explain:** The golden rule in Python: `base64` functions **only accept and return bytes**, NOT strings! This is why we covered `.encode()` and `.decode()` earlier!

### 2. Live Coding: Base64 Encode & Decode
- **[OPEN]** `examples/starter/base64_example.py`
- **Explain:** We have our starter string. We need to Base64 encode it and print it, then decode it back.
- **[WRITE]** Fill in the implementation working towards the `complete` version:

    ```python
    import base64

    message = 'pwn_on_autopilot_base64_demo'

    # Base64 encode the message
    message_bytes = message.encode('utf-8')
    encoded_bytes = base64.b64encode(message_bytes)

    # Print the encoded result (decode back to string for clean printing)
    print(f"Encoded: {encoded_bytes.decode('utf-8')}")

    # Base64 decode it back
    decoded_bytes = base64.b64decode(encoded_bytes)
    print(f"Decoded: {decoded_bytes.decode('utf-8')}")
    ```

- **[RUN]** `uv run examples/starter/base64_example.py`
- **[SHOW]** The terminal output matching: 
  `Encoded: cHduX29uX2F1dG9waWxvdF9iYXNlNjRfZGVtbw==`
  `Decoded: pwn_on_autopilot_base64_demo`
- **Tip:** If anyone asks about web hacking/JWTs breaking URLs with `+` and `/` characters, mention `urlsafe_b64encode` (which swaps them for `-` and `_`). It is documented in the repo reference.

## Section 6: Libraries - `json`

### 1. Intro to JSON
- **Explain:** JSON is the backbone of modern web APIs, cloud IAM policies, and tooling outputs (like BloodHound or Nuclei).
- **Explain:** Python handles JSON flawlessly by turning it directly into Python Dictionaries and Lists.
- **Rule of Thumb:** Remember the rule of **"S"**! `load`/`dump` are for files, `loads`/`dumps` (load *strings*) are for string variables.

### 2. Live Coding: Parsing and Modifying JSON
- **[OPEN]** `examples/starter/1_data.json`
- **[SHOW]** Briefly show the audience the mock data (A server with open ports, marked vulnerable, and admin credentials).
- **[OPEN]** `examples/starter/1_json_example.py`
- **Explain:** We are going to read this tool output from disk, print the admin password, inject our own backdoor user, and write the modified config back to disk.
- **[WRITE]** Fill in the implementation:

    ```python
    import json
    
    # 1. Load the data using standard load() since it's a file
    with open('1_data.json', 'r') as f:
        data = json.load(f)
    
    # 2. Print the admin's password (It's just a Python dictionary now!)
    print(f"Admin password: {data['credentials']['admin']}")
    
    # 3. Add a new backdoor user and patch the vulnerability status
    data['credentials']['backdoor'] = 'pwned'
    data['vulnerable'] = False
    
    # 4. Save the modified data using dump() back to a new file
    with open('1_modified.json', 'w') as f:
        json.dump(data, f, indent=4)  # Highlight indent=4!
        
    print('Successfully backdoored the JSON file!')
    ```

- **[RUN]** `uv run examples/starter/1_json_example.py`
- **[SHOW]** The terminal printing the admin password.
- **[OPEN]** `examples/starter/1_modified.json` so the audience can see the beautifully indented JSON with the backdoor user successfully injected.
- **Tip:** Remind them that if they are grabbing JSON from a network request instead of a file, they use `loads(response.text)`!
