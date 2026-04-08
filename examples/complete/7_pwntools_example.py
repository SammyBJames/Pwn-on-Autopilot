from pwn import *

# Connect to a local binary
# r = process('./7_vuln_linux') # or ./7_vuln_windows.exe or ./7_vuln_macos
# Or connect to the remote server
r = remote('pwn.inmt.win', 1337)

# Consume output until the server sends "Username: "
r.recvuntil(b'Username: ')

# Send the username "admin"
r.sendline(b'admin')

# Read the next output line and save it to a variable called `response`
response = r.recvline()

# Consume output until "Password: " then send the password "password123"
r.sendafter(b'Password: ', b'password123')

# Drop into an interactive shell
r.interactive()
