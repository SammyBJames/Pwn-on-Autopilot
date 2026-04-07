# File Operations in Python

Handling files is fundamental. Python makes file operations (mostly) straightforward.

## Context Managers (The `with` statement)
Always use the `with` statement when opening files. It acts as a context manager, meaning Python automatically closes the file for you as soon as the block of code is finished, even if an error occurs. This prevents locked files and memory leaks.

```python
with open('flag.txt', 'r') as f:
    print(f.read())
# The file is automatically closed here.
```

## File Modes
When opening a file, you must specify the mode. The mode dictates what you can do with the file and how the data is handled.

### Primary Modes
- `r` (Read): Default mode. Opens a file for reading. Throws `FileNotFoundError` if the file doesn't exist.
- `w` (Write): Opens a file for writing. Creates the file if it doesn't exist, and **overwrites existing files**.
- `a` (Append): Opens a file for writing, but appends data to the end without overwriting it. Creates the file if it doesn't exist.
- `x` (Exclusive Creation): Opens a file for writing but fails if the file already exists.

### Modifiers
- `b` (Binary): Opens the file in binary mode instead of text mode. Use this when dealing with any non-text data such as executables, images, network captures, etc. - (`rb`, `wb`).
- `+` (Update): Opens a file for both reading and writing.
    - `r+`: Read and write. The file pointer is placed at the *beginning*. Be careful: writing immediately will overwrite the beginning of the existing content.
    - `w+`: Write and read. **Clears the entire file** upon opening, then allows writing (and reading) new content.
    - `a+`: Append and read. The file pointer is placed at the *end*. Note: to read existing content with `a+`, you must first move the file pointer back to the start using `f.seek(0)`.

## Reading Files
Depending on the file size, you have a few ways to pull data into your script:

- **`f.read()`**: Reads the entire file into a single string (or byte array). Great for small files.
- **`f.readlines()`**: Reads the entire file and returns a list of strings, one for each line.
- **`for line in f:` (Iterating)**: The best approach for large files. It reads one line at a time, keeping your memory footprint small.

```python
# Find a password in rockyou.txt
with open('rockyou.txt', 'r') as f:
    for line in f:
        if password in line:
            print(f'Found it: {line.strip()}')
            break
```

## Writing Files
Call `f.write(content)` to write to a file, where `content` is the string or bytes you want to write.

```python
# Write a payload to exploit.txt
with open('exploit.txt', 'w') as f:
    f.write('A' * 100 + '\n')
    f.write('B' * 50)
```

## Binary Files
In cybersecurity we constantly deal with non-text files like executables, memory dumps, and raw network packets.

When you open a file in default text mode (`r`), Python automatically attempts to decode the data using an encoding like UTF-8. If the file is not encoded in UTF-8, this decoding process will inevitably fail and crash your script with a `UnicodeDecodeError`.

By using the `b` (binary) modifier (`rb` or `wb`), Python skips the decoding process. Instead of returning a string, it returns the raw data as a `bytes` object.

**Key differences when dealing with `bytes`:**
- A `bytes` object looks like a string but has a `b` prefix: `b'\x90\x90\x90'`.
- While extracting a character from a string gives you a letter (`'A'`), extracting from a `bytes` object gives you an integer from 0-255 (`65`).
- We'll talk more about working with bytes later.

```python
# Read an image
with open('image.jpg', 'rb') as f:
    data = f.read()
    print(f'File starts with magic bytes: {data[:4]}')

# Write constructed shellcode to disk
shellcode = b'\x90\x90\x90\x90\xcc'
with open('payload.bin', 'wb') as f:
    f.write(shellcode)
```
