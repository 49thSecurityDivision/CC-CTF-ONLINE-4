from pwn import *


conn = remote('challenges.carolinacon.org', 8004)
#conn = process([ "python3", "./mathemagician.py" ])
eng = { "zero": "0",
        "one": "1", 
       "two": "2", 
       "three": "3", 
       "four": "4", 
       "five": "5", 
       "six": "6", 
       "seven": "7", 
       "eight": "8", 
       "nine": "9", 
       "ten": "10", 
       "eleven": "11", 
       "twelve": "12", 
       "thirteen": "13", 
       "fourteen": "14", 
       "fifteen": "15", 
       "sixteen": "16", 
       "seventeen": "17", 
       "eighteen": "18", 
       "nineteen": "19", 
       "twenty": "20", 
       }
try:
    while True:
        line = conn.recvline().decode()

        print(line)
        if "what is " in line :

            # Extract math problem
            prob = line.replace("what is ", "")

            for english, num in eng.items() :
                prob = prob.replace(english, num)

            sol = eval(prob)
            print("Answer:", sol)
            conn.sendline(str(sol).encode())
        else:
            print(conn.recvline())
            break

except EOFError:
    print("except")
    #conn.close()

print(conn.recvline())
conn.close()
