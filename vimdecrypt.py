from __future__ import print_function
import sys, os, getpass, ctypes

dirname = os.path.dirname(__file__)
blowfishpath = os.path.join( dirname, 'blowfish.so' )
blowfish = ctypes.cdll.LoadLibrary( blowfishpath )

# void bf_key_init( unsigned char *password, unsigned char *salt, int salt_len );
# void bf_cfb_init( unsigned char *iv, int iv_len );
# void bf_crypt_decode( unsigned char *ptr, long len );

def decrypt( filename ):
  with open( filename, 'rb' ) as data:
    assert data.read(12) == b'VimCrypt~02!', 'input should be a vim-encrypted file'
    salt = data.read(8)
    seed = data.read(8)
    assert len(salt) == len(seed) == 8, 'data ended prematurely'
    buf = ctypes.create_string_buffer( data.read() )
  pw = getpass.getpass( 'password: ' )
  assert pw, 'empty password'
  blowfish.bf_key_init( pw.encode(), salt, ctypes.c_int(len(salt)) )
  blowfish.bf_cfb_init( seed, ctypes.c_int(len(seed)) )
  blowfish.bf_crypt_decode( buf, ctypes.c_long(len(buf)-1) );
  return buf.value.decode()

if __name__ == '__main__':
  if len(sys.argv) != 2:
    sys.exit( 'usage: %s [filename]' % os.path.basename(__file__) )
  print( decrypt( sys.argv[1] ) )
