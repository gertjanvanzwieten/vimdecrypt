#include "vim.h"

int main() {

  char *pass = getpass( "password: " );
  if ( pass[0] == '\0' ) {
    EMSG( "empty password\n" );
    return 1;
  }

  char magic[12];
  if ( read( 0, magic, 12 ) != 12 || ! strcmp( magic, "VimCrypt~02" ) ) {
    EMSG( "input should be a vim-encrypted file\n" );
    return 1;
  }

  char salt[8], seed[8];
  if ( read( 0, salt, 8 ) != 8 || read( 0, seed, 8 ) != 8 ) {
    EMSG( "data ended prematurely\n" );
    return 1;
  }

	bf_key_init( pass, salt, sizeof(salt) );
	bf_cfb_init( seed, sizeof(seed) );

  char buf[ 256 ];
  int nread;
  for ( ;; ) {
    nread = read( 0, buf, sizeof(buf) );
    if ( nread == 0 ) {
      break;
    }
    bf_crypt_decode( buf, nread );
    write( 1, buf, nread );
  }

  return 0;
}
