# Byte Manipulation

In Python, `bytes` are immutable sequences of integers from 0 to 255. You will constantly work with bytes when dealing with network packets, compiled binaries, shellcode, and cryptography.

## Creating Bytes
You can create bytes using the `b` prefix or the `bytes()` constructor. Use `\x` for hexadecimal byte values.

```python
# Byte literals (only ASCII characters are allowed directly)
payload = b'A' * 40 # b'AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA'
shellcode = b'\x41\x42\x43' # b'ABC'

# Convert a list of integers (0-255)
data = bytes([0x41, 0x42, 0x43]) # b'ABC'
```

## Encoding and Decoding
Strings (`str`) and bytes (`bytes`) are separate types. You must convert between them.
- **Encode** (`str` -> `bytes`): Translates characters into raw bytes.
- **Decode** (`bytes` -> `str`): Translates raw bytes back into characters.

```python
text = 'admin'
raw_data = text.encode('utf-8') # b'admin'

# Sometimes payloads have non-UTF8 bytes.
# 'latin-1' is an encoding that safely maps 1:1 for 0-255.
decoded = raw_data.decode('latin-1') 
```

## Basic Operations
Bytes support many of the same operations as strings.

```python
buf = b'Hello World'

# Concatenation and Repetition
padded = b'\x90' * 10 + buf + b'\x00'

# Searching and Replacing
if b'World' in buf:
    new_buf = buf.replace(b'World', b'Hacker')

# Slicing
world = buf[6:] # b'World'

# Indexing (Returns an int, not a byte)
first_byte = buf[0] # 72 (which is 0x48 / 'H')

# Padding (Useful for block ciphers and buffer overflows)
padded_left = b'AAAA'.rjust(8, b'\x00')  # b'\x00\x00\x00\x00AAAA'
padded_right = b'AAAA'.ljust(8, b'\x90') # b'AAAA\x90\x90\x90\x90'
```

## Hexadecimal Conversions
We often pass payloads back and forth as hex strings. Python makes converting these simple:

```python
# Bytes to Hex String
raw = b'\xde\xad\xbe\xef'
hex_str = raw.hex() # 'deadbeef'

# Hex String to Bytes
recovered_raw = bytes.fromhex(hex_str) # b'\xde\xad\xbe\xef'
```

## Integers Conversions (Endianness)
When writing exploits, you frequently need to convert memory addresses (integers) into raw bytes. You need to specify the length and the byte order (endianness).
- **Little-Endian (least significant byte first):** Used by mostly all modern Intel/AMD processors (x86/x64).
- **Big-Endian (most significant byte first):** Often used in network protocols.

```python
address = 0xcafebabe

# Integer to Bytes
little = address.to_bytes(4, byteorder='little') # b'\xbe\xba\xfe\xca'
big = address.to_bytes(4, byteorder='big')       # b'\xca\xfe\xba\xbe'

# Bytes to Integer
recovered = int.from_bytes(b'\xbe\xba\xfe\xca', byteorder='little') # 0xcafebabe
```

## File Carving (Magic Bytes)
When analyzing memory dumps or network captures, you often need to find specific files (like extracting an image) hidden inside a massive blob of bytes. You can use `.find()` to locate the index of file "magic bytes" (signatures) and slice them out.

```python
dump = b'junkdata...\xff\xd8\xff\xe0...image_data...\xff\xd9morejunk'

# Find the start and end signatures (JPEG starts with 0xffd8ffe0 and ends with 0xffd9)
start_idx = dump.find(b'\xff\xd8\xff\xe0') 
end_idx = dump.find(b'\xff\xd9', start_idx) 

if start_idx != -1 and end_idx != -1:
    # Slice out the image bytes
    # Add 2 to the end index to include the 2 EOF bytes (0xffd9)
    image_bytes = dump[start_idx:end_idx + 2] 
    
    # Save the image to a file (note the 'b' modifier for binary)
    with open('extracted.jpg', 'wb') as f:
        f.write(image_bytes)
```

## `bytearray`: Mutable Bytes
Because standard `bytes` are immutable, you cannot change bytes in the middle of a payload (e.g., `buf[2] = 0xff` throws a `TypeError`). When you need to build or modify a payload dynamically without constantly creating new objects, use a `bytearray`.

```python
# Create a bytearray from existing bytes
payload = bytearray(b'\x41\x41\x41\x41') # bytearray(b'AAAA')

# Modify in place (must be an integer 0-255)
payload[0] = 0x43 # bytearray(b'CAAA')

# Append and extend
payload.append(0x42)
payload.extend(b'\x44\x45')

# Convert back to immutable bytes if needed
final_payload = bytes(payload) # b'CAAABDE'
```

## XORing Bytes
A classic CTF task. You can't XOR bytes directly (like `b'A' ^ b'B'`), because the operator works on integers. You usually pair them up using `zip()` to iterate through their integer equivalents.

```python
data = b'secret'
key = b'\xaa\xbb\xcc\xdd\xee\xff'

# XOR each byte pair together
xored = bytes([b1 ^ b2 for b1, b2 in zip(data, key)])
```
