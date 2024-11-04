import rsa

def enc(m, n, e):
    m_int = int.from_bytes(m, byteorder="big")
    c = pow(m_int, e, n)
    return c

def dec(c, n, d):
    m_int = pow(c, d, n)
    m = m_int.to_bytes((m_int.bit_length() + 7) // 8, byteorder="big").decode()
    return m

pub, priv = rsa.newkeys(512)

p = priv.p
q = priv.q
d = priv.d
n = priv.n
phi = (p-1)*(q-1)
e = pub.e

with open("./dec_flag.txt", "rb") as file:
    dec_flag = file.read()

enc_flag = rsa.encrypt(dec_flag, pub)
enc_flag = int.from_bytes(enc_flag, byteorder="big")

#with open("./enc_flag.txt", "wb") as file:
#    file.write(enc_flag)

print(f"Flag is {dec_flag}")
print(f"Encrypted flag is {enc_flag}")

c = enc(dec_flag, n, e)
print(f"c = {c}")

print(f"p = {p}")
print(f"q = {q}")
print(f"n = {n}")
print(f"e = {e}")
print(f"dp = {d % (p-1)}")





