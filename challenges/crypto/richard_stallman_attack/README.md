# Prompt

Introducing the Richard Stallman Algorithm! 

It is just like RSA, except we removed all of the stupid stuff and made more variables public.

We are so confident it works I will give you the exact code I use to encrypt and decrypt messages:

```
def enc(m, n, e):
    m_int = int.from_bytes(m, byteorder="big")
    c = pow(m_int, e, n)
    return c

def dec(c, n, d):
    m_int = pow(c, d, n)
    m = m_int.to_bytes((m_int.bit_length() + 7) // 8, byteorder="big").decode()
    return m

```

My favorite part of the past several decades is that people keep using RSA instead of switching to my new coolness.

Those others guys are greedy with their information, but for us, we like to give a lot more. In fact, here is how secure my RSA is: I will give you a message and all of the public variables we release by default, and I *bet you a flag* you won't be able to decrypt it!

Here is my super secret message:

```
e = 65537
n = 8387272652763816957649402162456494214377790102005836448658782891972530669784768122262760686135715400089454301201598707218766276369357291935087715344530529
dp = 6500451392660115929606308612183761342326319188085955403082185804023940135089199459
c = 1016654411324907893775160227349517335245984349146124653872253371015168464826587683923434999763187025960510085106796775235685315008051501028220634874688625
```

# Category 

Crypto 

# Files to Release

```
N/A
```

# Remote 

`N/A`

# Solution

This challenge requires reconstructing the RSA private key from the information given. There are a number of writeups online of how to do this, but the solution from the following article basically works if you just copy/paste it: 

https://medium.com/@hva314/some-basic-rsa-challenges-in-ctf-part-1-some-basic-math-on-rsa-5663fa337c27

In sagemath, the solution looks like this:

```
sage: for kp in range(1,e):
....:     x = (e*dp-1)/kp+1
....:     if (x in ZZ):
....:         if (n/x) in ZZ:
....:             p = x
....:             break
sage: q = n/p
sage: phi = (p-1)*(q-1)
sage: d = inverse_mod(e,phi)
sage: m = int(pow(c,d,n))
sage: hex(m) # unhexlify this for the flag
```

`cc_ctf{how_did_you_find_out_what_dp_was???}`
