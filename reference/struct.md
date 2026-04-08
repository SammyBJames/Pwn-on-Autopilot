# Parsing Structured Binary (`struct`)
The `struct` library is the your best friend for unpacking and packing contiguous binary data. The `int.from_bytes()` method is great for single integers, but if we are reading a custom binary file header with a 4-byte integer, a 2-byte short, and an 8-byte timestamp, `struct` can parse them all at once with a format string.

## Format Strings (Defining the Structure)
You define the structure of the binary data using format strings:
- **Endianness:** `<` (Little-Endian), `>` (Big-Endian), `!` (Network Big-Endian, standard for network packets)
- **Data Types:** 
    - `B` / `b`: 1-byte (char)
    - `H` / `h`: 2-byte (short)
    - `I` / `i`: 4-byte (int)
    - `Q` / `q`: 8-byte (long / long long)
    - `s`: Byte string (`10s` means "read exactly 10 bytes as a string")
    - `x`: Pad byte (skips or ignores a byte)

## Unpacking Data
Use `struct.unpack()` to extract integers and variables from raw bytes based on your format string.

```python
import struct

# A mock 15-byte packet: [4-byte ID] + [2-byte Flags] + [1-byte Type] + [8-byte Timestamp]
packet = b'\xef\xbe\xad\xde\x01\x00\xff\xaa\xbb\xcc\xdd\x00\x00\x00\x00'

# Unpack 4-bytes (I), 2-bytes (H), 1-byte (B), 8-bytes (Q) in little-endian (<) order
packet_id, flags, p_type, timestamp = struct.unpack('<IHBQ', packet)

print(hex(packet_id)) # '0xdeadbeef'
print(hex(flags))     # '0x1'
print(hex(p_type))    # '0xff'
print(hex(timestamp)) # '0xddccbbaa'
```

## Packing Data
Use `struct.pack()` to create your own headers or payloads from integers.

```python
# Create a custom packet header using Network Big-Endian order (!)
forged_header = struct.pack('!IHB', 0xcafebabe, 0x02, 0x00)
# Output: b'\xca\xfe\xba\xbe\x00\x02\x00'
```

## Avoiding Guesswork (`calcsize`)
Exploits fail instantly if you read the wrong number of bytes from a file or socket. Instead of doing the math in your head, ask `struct` exactly how many bytes to read using `calcsize()`.

```python
fmt = '<IHBQ'
expected_size = struct.calcsize(fmt) # Automatically calculates 15 bytes

with open('capture.pcap', 'rb') as f:
    # Read exactly 15 bytes so we can safely unpack it
    header_data = f.read(expected_size)
    packet_id, flags, p_type, timestamp = struct.unpack(fmt, header_data)
```

## Resources
- [`struct` Official Documentation](https://docs.python.org/3/library/struct.html)
- [`struct` Module in Python (Geeks for Geeks)](https://www.geeksforgeeks.org/python/struct-module-python/)
