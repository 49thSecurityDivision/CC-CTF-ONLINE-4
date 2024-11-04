#!/usr/bin/env python3

import argparse

from secrets import token_bytes as randbytes
from base64 import urlsafe_b64encode as encode

"""
    This file is for generating flags for the ctf 
    if you don't are about them having a meaning 
    of some kind.
"""

def generate_flag(size=24):
    flag = encode(randbytes(size))
    flag = f'cc_ctf{{{flag.decode()}}}'
    return flag


def get_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('-c', '--count', type=int, default=10)
    parser.add_argument('-l', '--length', type=int, default=24)
    
    return parser.parse_args()


if __name__ == '__main__':
    args = get_args()
    count = args.count
    length = args.length
    print("\n".join(generate_flag(length) for _ in range(count)))
    
