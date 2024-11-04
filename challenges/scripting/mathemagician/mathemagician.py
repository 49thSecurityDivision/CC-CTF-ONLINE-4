#!/usr/bin/python

import random

num_dict = {
        0 : "zero",
        1 : "one",
        2 : "two",
        3 : "three",
        4 : "four",
        5 : "five",
        6 : "six",
        7 : "seven",
        8 : "eight",
        9 : "nine",
        }
count = 0
while count < 1000:
    op = ["+", "-", "*"]
    op_num = random.randint(1,3)
    data = ""
    solve = 0

    if count < 500:
        x=random.randint(1,100)
        y=random.randint(1,200)
        if op_num == 1:
            solve = x + y
            data = ("what is %d + %d\n" % (x , y))
        elif op_num == 2:
            solve = x - y
            data = ("what is %d - %d\n" % (x , y))
        else:
            solve = x * y
            data = ("what is %d * %d\n" % (x , y))

    elif count < 750:
        x=random.randint(0,255)
        y=random.randint(0,255)
        if op_num == 1:
            solve = x + y
            data = ("what is %s + %s\n" % (hex(x) , hex(y)))
        elif op_num == 2:
            solve = x - y
            data = ("what is %s - %s\n" % (hex(x) , hex(y)))
        else:
            solve = x * y
            data = ("what is %s * %s\n" % (hex(x) , hex(y)))
    else:
        x=random.randint(0,9)
        y=random.randint(0,9)
        z=random.randint(0,9)
        if op_num == 1:
            solve = x + y * z
            data = ("what is %s + %s * %s\n" % (num_dict[x] , num_dict[y], num_dict[z]))
        elif op_num == 2:
            solve = x * y - z
            data = ("what is %s * %s - %s\n" % (num_dict[x] , num_dict[y], num_dict[z]))
        else:
            solve = x - y + z
            data = ("what is %s - %s + %s\n" % (num_dict[x] , num_dict[y], num_dict[z]))
        
    try:
        r = input(data)
    except Exception as e:
        print("Not sure what you are doing, but I cannot take that...")
        continue

    try:
        val = int(r)
    except ValueError:
        print("That's not an int!")
        continue

    if int(r) == solve:
        count = count + 1
    else:
        print("Resetting the count...")
        count = 0

print("count:")
print(count)
if count == 1000:
    input('cc_ctf{what_are_you_some_k1nd_0f_w1z4rd?}\r\n')
