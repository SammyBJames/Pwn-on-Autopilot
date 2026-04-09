# pwntools

`pwntools` is a CTF framework and exploit development library. It is a massive library that abstracts away the most frustrating parts of binary exploitation.

We can break this library down into 5 key components:

## "Tubes" (Networking & Execution)
Normally, writing a script that talks to a network socket and another script that talks to a local executable requires completely different code. `pwntools` unifies them into a single object called a "Tube."

You can write your entire exploit against a local binary (`process()`), and when you're ready to attack the real server, you just change one line of code to `remote()`.

### Connecting
```python
from pwn import *

# Run a local executable
r = process('./vulnerable_app')

# Connect to a remote server
r = remote('10.10.10.50', 1337)

# Listen for an incoming reverse shell
# Your script can automatically interact with the callback
l = listen(4444)
r = l.wait_for_connection()
```

### Reading and Writing
Tubes save you from writing loops to read chunks of network data. They wait exactly as long as needed.

```python
# Wait until the server sends 'Username: '
r.recvuntil(b'Username: ')

# Send our payload with an automatic newline (\n) attached
r.sendline(b'admin')

# Read exactly one line of response
response = r.recvline()

# Send data after seeing a prompt (combines recvuntil + send)
r.sendlineafter(b'Password: ', b'supersecret')

# Read everything until the connection closes
full_response = r.recvall()
```

### Getting an Interactive Shell
Once you get a shell, you don't need to write custom code to send and receive commands. You just call `.interactive()`, and `pwntools` drops your terminal into the remote session.

```python
# Assuming we just sent the exploit payload...
r.interactive()
```

## Data Packing
When writing buffer overflows, you need to pack memory addresses (like `0xdeadbeef`) into Little-Endian bytes (`b'\xef\xbe\xad\xde'`).

```python
from pwn import *

# Pack an integer into 32-bit (4 bytes) Little-Endian
payload = p32(0xdeadbeef) # b'\xef\xbe\xad\xde'

# Pack into 64-bit (8 bytes) Little-Endian
payload_64 = p64(0x00000000004005c0) 

# Unpack raw leaked bytes back into an integer
leaked_memory = r.recv(4)
address = u32(leaked_memory)
print(hex(address)) # 0xdeadbeef

# Pack data with a dynamic size
payload = pack(0xdeadbeef, 16) # b'\xef\xbe\xad\xde' + 14 null bytes
```

## Buffer Overflows
When setting up a buffer overflow, we need to know at what offset we want to overwrite. `pwntools` has this built-in.

```python
from pwn import *

# Generate a 100-byte De Bruijn sequence (aaaabaaacaaadaaa...)
pattern = cyclic(100)
r.sendline(pattern)

# When GDB says our instruction pointer was overwritten with "qaac" (0x63616171)
# Find the exact offset length to reach that memory address:
offset = cyclic_find(b'qaac') 
print(f'Offset found at: {offset}') 

# Build the final payload
exploit = b'A' * offset + p32(0xdeadbeef)
```

## Context & Shellcode
`pwntools` introduces a global `context` object. By setting your target architecture and OS once, the entire library magically adapts (including packing functions and assembly generation).

```python
from pwn import *

# Set the global context for target
context.arch = 'amd64'
context.os = 'linux'

# Create the assembly instructions to pop /bin/sh
code = shellcraft.sh()

# Compile the assembly into machine code based on the context
compiled_shellcode = asm(code)

# Send payload to the server
r.sendline(compiled_shellcode)
```

## ELF Parsing & Bypassing ASLR
`pwntools` can natively parse compiled binaries (ELF files).

By loading an ELF into `pwntools`, you can completely automate the reverse engineering and targeting process directly in Python.

### Reading Binary Mitigations
Before writing an exploit, find out what defenses the binary was compiled with:
```python
from pwn import *

# Automatically prints whether ASLR/PIE, NX, or Stack Canaries are enabled
elf = ELF('./vuln_server')
```

### Defeating ASLR
When ASLR is enabled, the base memory address of libraries (like `libc`) is randomized on every run, but the internal offsets remain identical. You can use `pwntools` to rebase the entire library if you can leak the address of a function!

```python
libc = ELF('/lib/x86_64-linux-gnu/libc.so.6')

# Imagine your exploit successfully leaks where 'puts' was loaded in memory:
leaked_puts = 0x7f8a9b4c3d20 

# We can now calculate the randomized ASLR base with pwntools
libc.address = leaked_puts - libc.symbols['puts']

# Now every symbol in the ELF is updated to the correct, real memory address
system_addr = libc.symbols['system'] # Find the real address of 'system'
bin_sh_addr = next(libc.search(b'/bin/sh\x00')) # Find the real address of the string '/bin/sh'
```

### Extracting Functions and Pointers
When crafting Return-Oriented Programming (ROP) chains or GOT overwrites, you can quickly grab addresses from the PLT and GOT tables.

```python
# Where does the 'main' function start?
main_func = elf.symbols['main']

# Where is the internal instruction to jump to the external 'printf'?
plt_printf = elf.plt['printf']

# Where does the program store the exact memory pointer to 'printf'?
got_printf = elf.got['printf']
```

### Patching Binaries
You can also use the `ELF` module as a headless binary patcher.
```python
# Overwrite the instructions at a function address
elf.write(elf.symbols['check_admin'], asm('nop') * 10)

# Save the patched executable
elf.save('./vuln_server_patched')
```

## Resources
- [`pwntools` Official Documentation](https://docs.pwntools.com/en/latest/)
- [Pwntools Tutorials](https://github.com/Gallopsled/pwntools-tutorial)
