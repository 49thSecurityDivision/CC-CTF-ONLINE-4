#!/bin/sh 

gcc -no-pie -nostartfiles pesticide.s -o pesticide
#objcopy -j .text write_file output
