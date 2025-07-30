#!/usr/bin/env python3

import struct
import hashlib
import unittest
import operator
import getpass
import sys


def cli():
    if len(sys.argv) > 2:
        sys.exit("usage: vimdecrypt [path]")

    file = sys.argv[1] if len(sys.argv) == 2 else sys.stdin.buffer
    print(decrypt(file))


def _swap_endianness(data):
    return struct.pack("<2L", *struct.unpack(">2L", data))


def blowfish(key):
    try:
        from Crypto.Cipher import Blowfish
    except ImportError:
        try:
            from Cryptodome.Cipher import Blowfish
        except ImportError:
            try:
                import blowfish
            except ImportError:
                raise Exception("failed to import cryptographic module")
            return blowfish.Cipher(key, byte_order="little").encrypt_block
    bf = Blowfish.new(key, mode=Blowfish.MODE_ECB)
    return lambda data: _swap_endianness(bf.encrypt(_swap_endianness(data)))


def decrypt(f, pw=None, encoding="utf8"):
    if isinstance(f, str):
        with open(f, "rb") as f:
            return decrypt(f, pw, encoding)
    if f.read(12) != b"VimCrypt~03!":
        raise Exception("not a blowfish2-encoded vimcrypt file")
    salt = f.read(8)
    if pw is None:
        pw = getpass.getpass()
    for i in range(1000):
        pw = hashlib.sha256(pw.encode() + salt).hexdigest()
    cipher = blowfish(hashlib.sha256(pw.encode() + salt).digest())
    block0 = f.read(8)
    block1 = f.read(8)
    decrypted = bytearray()
    while block1:
        decrypted.extend(map(operator.xor, cipher(block0), block1))
        block0 = block1
        block1 = f.read(8)
    return decrypted.decode(encoding)


class Test(unittest.TestCase):
    def test(self):
        import io

        f = io.BytesIO(
            b"VimCrypt~03!\xff\xcf\xe2R\x9b\xe0\xa9\x85\xa20\xf4S\x95)18A\xaa,\x11\x83\x98\xfb}i\xfa\xff\xf1\xc6|,"
        )
        self.assertEqual(decrypt(f, "my password"), "my secret text\n")
