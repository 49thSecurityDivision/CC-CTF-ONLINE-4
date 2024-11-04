import string

freq_chrs  = "ETAOINRSHLWD" # don't use lowercase so we don't swap twice
lower      = string.ascii_lowercase
freq_dct   = {}
sorted_dct = {}
sorted_lst = []
tmp = ""


"""
    This solve file will not *entirely* solve the challenge. 
    You will have to manually replace about 10 letters after 
    running this file to get the flag.
"""

with open("./encrypted_challenge.txt", "r") as file:
    enc = file.read()

enc = enc.lower()

for c in enc:
    try:
        freq_dct[c] += 1
    except:
        freq_dct[c] = 1

for key in sorted(freq_dct, key=freq_dct.get):
    if key in lower:
        sorted_dct[key] = freq_dct[key]

sorted_lst = list(sorted_dct)
#print(sorted_dct)
print(sorted_lst[-1])

freq_index = 0
for c in freq_chrs:
    enc_chr = sorted_lst[-1]
    sorted_lst = sorted_lst[:-1]
    
    for x in enc:
        if enc_chr == x:
            tmp += freq_chrs[freq_index]
        else:
            tmp += x
        
    # Set the data to have removed the chr we just targeted
    enc = tmp
    tmp = ""
    freq_index += 1

dec = enc
print(dec)
