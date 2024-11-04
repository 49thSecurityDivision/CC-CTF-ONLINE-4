#!/usr/bin/python3

import random
import string

with open("./decrypted_answer.txt", "r") as file:
    msg_to_enc = file.read()
enc_msg = ""

lower    = string.ascii_lowercase
upper    = string.ascii_uppercase
alph_mod = len(lower) # Works for both
rand     = random.randint(1, 100000) 

for char in msg_to_enc:
    if char in lower:
        index = lower.index(char)
        enc_msg += lower[(rand + index) % alph_mod]
    elif char in upper:
        index = upper.index(char)
        enc_msg += upper[(rand + index) % alph_mod]
    else:
        enc_msg += char

with open("./encrypted_challenge.txt", "w") as file:
    file.write(enc_msg)
