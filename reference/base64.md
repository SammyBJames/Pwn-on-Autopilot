# Base64 Encoding

Base64 is everywhere in cybersecurity: HTTP Basic Auth, JWTs (JSON Web Tokens), email attachments, and so much more. Python’s built-in `base64` module makes interacting with it simple, provided you remember that **Base64 operations work on `bytes`, not `str` (strings)!**

## Standard Base64

Because the `base64` functions require bytes, you must `.encode()` your strings before passing them in, and `.decode()` the result if you want human-readable text back.

```python
import base64

message = 'some_data_to_encode'

# 1. Convert string to bytes
raw_bytes = message.encode() # Uses 'utf-8' by default

# 2. Encode to Base64 (returns bytes)
encoded_bytes = base64.b64encode(raw_bytes)
print(encoded_bytes) # b'c29tZV9kYXRhX3RvX2VuY29kZQ=='

# 3. Decode back to original bytes
decoded_bytes = base64.b64decode(encoded_bytes)

# 4. Convert original bytes back to string
print(decoded_bytes.decode()) # 'some_data_to_encode'
```

## URL-Safe Base64

Standard Base64 uses `+` and `/` characters, which can break URLs or web requests if not properly URL-encoded. For web hacking (like JWTs or exploiting deserialization in cookies), use URL-safe base64, which swaps `+` for `-` and `/` for `_`. The API is the same, just use `urlsafe_b64encode()` and `urlsafe_b64decode()` instead.

```python
import base64

payload = b'\xfb\xef\xff'

# Standard: b'++//'
print(base64.b64encode(payload))

# URL Safe: b'--__'
print(base64.urlsafe_b64encode(payload))
```

## Resources
- [`base64` Official Documentation](https://docs.python.org/3/library/base64.html)
- [RFC 4648 (Base64 Encoding)](https://datatracker.ietf.org/doc/html/rfc4648)
