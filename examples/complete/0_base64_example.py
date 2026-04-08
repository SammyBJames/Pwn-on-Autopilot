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
