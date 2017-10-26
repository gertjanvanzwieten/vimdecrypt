#!/usr/bin/env python3

import struct, hashlib, unittest, operator, getpass


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
        raise Exception('failed to import cryptographic module')
      return blowfish.Cipher(key, byte_order='little').encrypt_block
  bf = Blowfish.new(key, mode=Blowfish.MODE_ECB)
  swapendian = lambda data: struct.pack('<2L', *struct.unpack('>2L', data))
  return lambda data: swapendian(bf.encrypt(swapendian(data)))


def decrypt(f, pw=None, encoding='utf8'):
  if f.read(12) != b'VimCrypt~03!':
    raise Exception('not a blowfish2-encoded vimcrypt file')
  salt = f.read(8)
  if pw is None:
    pw = getpass.getpass('password: ')
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
    f = io.BytesIO(b'VimCrypt~03!\xff\xcf\xe2R\x9b\xe0\xa9\x85\xa20\xf4S\x95)18A\xaa,\x11\x83\x98\xfb}i\xfa\xff\xf1\xc6|,')
    self.assertEqual(decrypt(f, 'my password'), 'my secret text\n')
