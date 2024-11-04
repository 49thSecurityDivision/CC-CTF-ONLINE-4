#!/usr/bin/env python3

from pwn import *

exe = ELF("./motivation")

context.binary = exe

def pwn(p):
    p.recvuntil(b'What motivates you?')
    p.recvline()

    with open("./payload.txt", "rb") as file:
        payload = file.read()

    p.sendline(payload)

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
        r = remote("challenges.carolinacon.org", 8002)

    return r


def main():
    r = conn()
    pwn(r)

    # good luck pwning :)

    r.interactive()


if __name__ == "__main__":
    main()
