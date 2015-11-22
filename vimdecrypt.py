from __future__ import print_function
import sys, os, getpass, warnings, ctypes

dirname = os.path.dirname(__file__)
blowfishpath = os.path.join( dirname, 'blowfish.so' )
blowfish = ctypes.cdll.LoadLibrary( blowfishpath )

# typedef struct { int	method_nr; void *method_state; } cryptstate_T;
# void crypt_blowfish_init( cryptstate_T *state, char_u* key, char_u* salt, int	salt_len, char_u* seed, int seed_len );
# void crypt_blowfish_decode( cryptstate_T *state, char_u	*from, size_t	len, char_u	*to );

class cryptstate_T( ctypes.Structure ):
  _fields_ = ('method_nr', ctypes.c_int), ('method_state', ctypes.c_void_p)

def decrypt( filename ):
  magics = None, b'VimCrypt~02!', b'VimCrypt~03!'
  with open( os.path.expanduser(filename), 'rb' ) as data:
    magic = data.read(12)
    assert magic in magics, 'input should be a vim-encrypted file'
    salt = data.read(8)
    seed = data.read(8)
    assert len(salt) == len(seed) == 8, 'data ended prematurely'
    buf = ctypes.create_string_buffer( data.read() )
  state = cryptstate_T( magics.index(magic) )
  if state.method_nr == 1:
    warnings.warn( 'file uses weak encryption' )
  pw = getpass.getpass( 'password: ' )
  assert pw, 'empty password'
  blowfish.crypt_blowfish_init( ctypes.byref(state), pw.encode(), salt, ctypes.c_int(len(salt)), seed, ctypes.c_int(len(seed)) )
  blowfish.crypt_blowfish_decode( ctypes.byref(state), buf, ctypes.c_long(len(buf)-1), buf );
  return buf.value.decode()

if __name__ == '__main__':
  if len(sys.argv) != 2:
    sys.exit( 'usage: %s [filename]' % os.path.basename(__file__) )
  print( decrypt( sys.argv[1] ) )
