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
    || strncmp( magic, "VimCrypt~0", 10 )
    || magic[10] != '2' && magic[10] != '3'
    || magic[11] != '!' ) {
    EMSG( "input should be a vim-encrypted file\n" );
    return 1;
  }

  cryptstate_T state;
  if ( magic[10] == '2' ) {
    state.method_nr = 1; // blowfish
    fprintf( stderr, "warning: file uses weak encryption\n" );
  }
  else {
    state.method_nr = 2; // blowfish2
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

  crypt_blowfish_init( &state, pass, salt, sizeof(salt), seed, sizeof(seed) );

  char buf[ 256 ];
  int nread;
  for ( ;; ) {
    nread = fread( buf, 1, sizeof(buf), fin );
    if ( nread == 0 ) {
      break;
    }
    crypt_blowfish_decode( &state, buf, nread, buf );
    fwrite( buf, 1, nread, stdout );
  }

  return 0;
}
