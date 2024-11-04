#!/bin/bash 

printf "" > output.txt

for i in {0..74}; do
  ROW=$(tr -dc 0-9X < /dev/urandom | head -c 75)
  printf "%s\n" "${ROW}" >> output.txt
done
