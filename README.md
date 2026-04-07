# Pwn on Autopilot: Python for Hackers
**Sam Bradley**

[![License](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)

## Overview
This workshop aims to teach beginner to intermediate learners how to speed up their hacking using Python and some common libraries for cybersecurity and provides you with several challenges to gain experience and hone your skills. The workshop will be broken down into the following sections:

1. **Setup:**
    - Install `uv`
    - Create a virtual environment
    - Install packages (PyPI)

2. **Review Basics:**
    - File operations (read, write, different modes)
    - Error handling (and catching abnormalities)
    - Byte manipulation (encoding, decoding, bytearrays, modes, etc.)

3. **Libraries:**
    - Network `requests`
    - `base64` encoding/decoding
    - `json` parsing and manipulation
    - `pwntools` for CTFs and network interactions
    - `argparse` for command-line interfaces

4. **Resources:**
    - Where to learn more
    - Use AI to test, debug, and speed up scripting!

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

3. **Install packages:**

    ```bash
    uv add <package-name>
    ```

    e.g. to install `requests`:

    ```bash
    uv add requests
    ```

    Find packages on [PyPI](https://pypi.org/).

4. **Run your Python script:**

    ```bash
    uv run <script-name>.py
    ```

5. **More information:**

    uv is a very powerful tool with many features beyond just these basics. To explore more features, look at the [uv reference](reference/uv.md) in this repository, or check out the official documentation at [docs.astral.sh/uv](https://docs.astral.sh/uv/).

## Basics

### File Operations
For Python file operations: always use the `with open()` context manager. It automatically closes the file for you when the block is finished, preventing locked files or memory leaks.

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



