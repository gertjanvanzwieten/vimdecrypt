from __future__ import print_function
import getpass, warnings, ctypes

libvimdecrypt = ctypes.cdll.LoadLibrary('libvimdecrypt.so')

class cryptstate_T( ctypes.Structure ):
  _fields_ = ('method_nr', ctypes.c_int), ('method_state', ctypes.c_void_p)

def decrypt( filename ):
  method_nr = { b'VimCrypt~02!':1, b'VimCrypt~03!':2 }
  with open( filename, 'rb' ) as data:
    magic = data.read(12)
    assert magic in method_nr, 'input should be a vim-encrypted file'
    salt = data.read(8)
    seed = data.read(8)
    assert len(salt) == len(seed) == 8, 'data ended prematurely'
    buf = ctypes.create_string_buffer( data.read() )
  state = cryptstate_T( method_nr[magic] )
  if state.method_nr == 1:
    warnings.warn( 'file uses weak encryption' )
  pw = getpass.getpass( 'password: ' )
  assert pw, 'empty password'
  libvimdecrypt.crypt_blowfish_init( ctypes.byref(state), pw.encode(), salt, ctypes.c_int(len(salt)), seed, ctypes.c_int(len(seed)) )
  libvimdecrypt.crypt_blowfish_decode( ctypes.byref(state), buf, ctypes.c_long(len(buf)-1), buf );
  return buf.value.decode()

def cli():
  import sys
  if len(sys.argv) != 2:
    sys.exit( 'usage: {} [filename]'.format( sys.argv[0] ) )
  print( decrypt( sys.argv[1] ) )
