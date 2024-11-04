#!/usr/bin/python3

import sys

if len(sys.argv) != 2:
  print("Usage: <program> <program to convert to binary>")
  sys.exit(1)

f = sys.argv[1]
o = f + ".binary"

with open(f, "rb") as file:
    with open(o, "w") as output_file:
        for b in file.read():
            #print(f"{b:08b}")
            output_file.write(f"{b:08b}")
