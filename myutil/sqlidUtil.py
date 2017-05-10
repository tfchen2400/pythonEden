#!/usr/bin/env python3
# coding=utf-8

import hashlib
import math
import struct


def sqlid_2_hash(sqlid):
    sum = 0
    i = 1
    alphabet = '0123456789abcdfghjkmnpqrstuvwxyz'
    for ch in sqlid:
        sum += alphabet.index(ch) * (32 ** (len(sqlid) - i))
        i += 1
    return sum % (2 ** 32)


def stmt_2_sqlid(stmt):
    h = hashlib.md5(stmt.encode('utf8')).digest()
    (d1, d2, msb, lsb) = struct.unpack('IIII', h)
    sqln = msb * (2 ** 32) + lsb
    stop = int(math.log(sqln, math.e) / math.log(32, math.e) + 1)
    sqlid = ''
    alphabet = '0123456789abcdfghjkmnpqrstuvwxyz'
    for i in range(0, stop):
        sqlid = alphabet[int((sqln / (32 ** i))) % 32] + sqlid
    return sqlid


def stmt_2_hash(stmt):
    return struct.unpack('IIII', hashlib.md5(stmt + '\x00').digest())[3]


if __name__ == '__main__':
    print(stmt_2_sqlid("STUINFO WHERE STUNAME = 'CHENTF'"))
