#!/usr/bin/env python
# This is source code copied from the Ceph project in Github
# and ported to Python
# see also: https://burtleburtle.net/bob/hash/doobs.html 

import sys

def to32(x):
    if x < 0:
        return to32(x + 0x100000000)
    return x & 0xffffffff

def rot32(x, num):
    assert x>=0 and x<=0xffffffff
    assert num>0 and num<32 
    return ((x << num) & 0xffffffff) ^ (x >> (32-num))

def mix(a, b, c):
    a = to32(a-b-c) ^ rot32(c, 32-13)
    b = to32(b-a-c) ^ rot32(a, 8)
    c = to32(c-a-b) ^ rot32(b, 32-13)
    a = to32(a-b-c) ^ rot32(c, 32-12)
    b = to32(b-a-c) ^ rot32(a, 16)
    c = to32(c-a-b) ^ rot32(b, 32-5)
    a = to32(a-b-c) ^ rot32(c, 32-3)
    b = to32(b-a-c) ^ rot32(a, 10)
    c = to32(c-a-b) ^ rot32(b, 32-15)
    return a, b, c

def rjenkins(input):
    k = []
    for x in input:
        k.append(ord(x))

    a = 0x9e3779b9;      # the golden ratio; an arbitrary value 
    b = a;
    c = 0;               # variable initialization of internal state

    # handle most of the key
    while len(k) >= 12: 
        a += k[0] + (k[1] << 8) + (k[2] << 16) + (k[3] << 24)
        b += k[4] + (k[5] << 8) + (k[6] << 16) + (k[7] << 24)
        c += k[8] + (k[9] << 8) + (k[10] << 16) + (k[11] << 24)
        a, b, c = mix(to32(a), to32(b), to32(c))
        k = k[12:]

    # handle the last 11 bytes 
    assert len(k) <= 11
    c += len(input)

    if len(k) == 11:
        c += k[10] << 24
    if len(k) >= 10:
        c += k[9] << 16
    if len(k) >= 9:
        c += k[8] << 8
        # the first byte of c is reserved for the length
    if len(k) >= 8:
        b += k[7] << 24
    if len(k) >= 7:
        b += k[6] << 16
    if len(k) >= 6:
        b += k[5] << 8
    if len(k) >= 5:
        b += k[4]
    if len(k) >= 4:
        a += k[3] << 24
    if len(k) >= 3:
        a += k[2] << 16
    if len(k) >= 2:
        a += k[1] << 8
    if len(k) >= 1:
        a += k[0]
        # case 0: nothing left to add

    a, b, c = mix(to32(a), to32(b), to32(c))
    return c

if len(sys.argv) != 2:
    print ("pass a string to compute the rjenkins hash of it")
    exit(-1)

hash = rjenkins(str(sys.argv[1]))
print(hex(hash))
exit(0)
