# Speaker Notes: Pwn on Autopilot

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
    uvx sqlmap -u http://target.com
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

