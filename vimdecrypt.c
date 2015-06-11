#include "vim.h"

int main( int argc, char *argv[] ) {

  if ( argc != 2 ) {
    EMSG( "usage: %s [filename]\n", argv[0] )
    return 1;
  }

  FILE *fin = fopen( argv[1], "r" );
  if ( ! fin ) {
    EMSG( "failed to open file '%s'\n", argv[1] )
    return 1;
  }

  char magic[12];
  if ( fread( magic, 1, sizeof(magic), fin ) != sizeof(magic)
    || strncmp( magic, "VimCrypt~02!", sizeof(magic) ) ) {
    EMSG( "input should be a vim-encrypted file\n" );
    return 1;
  }

  char salt[8], seed[8];
  if ( fread( salt, 1, sizeof(salt), fin ) != sizeof(salt)
    || fread( seed, 1, sizeof(seed), fin ) != sizeof(seed) ) {
    EMSG( "data ended prematurely\n" );
    return 1;
  }

  char *pass = getpass( "password: " );
  if ( pass[0] == '\0' ) {
    EMSG( "empty password\n" );
    return 1;
  }

	bf_key_init( pass, salt, sizeof(salt) );
	bf_ofb_init( seed, sizeof(seed) );

  char buf[ 256 ];
  int nread;
  for ( ;; ) {
    nread = fread( buf, 1, sizeof(buf), fin );
    if ( nread == 0 ) {
      break;
    }
    bf_crypt_decode( buf, nread );
    fwrite( buf, 1, nread, stdout );
  }

  return 0;
}
