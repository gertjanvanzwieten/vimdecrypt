#ifndef VIM__H
#define VIM__H

#include <unistd.h>
#include <stdio.h>
#include <string.h>

#define HAVE_CONFIG_H
#define OK 1
#define FAIL 0
#define STRLEN(s) strlen((char *)(s))
#define STRCPY(d,s) strcpy((char *)(d), (char *)(s))
#define EMSG(s) fprintf(stderr, s);
#define FEAT_CRYPT
#define _(x) (x)
#define __ARGS(x) x
#define mch_memmove(to, from, len) memmove((char *)(to), (char *)(from), len)
#define vim_memset(ptr,c,size) memset((ptr), (c), (size))
#define NUL '\000'

typedef unsigned int UINT32_T;
typedef unsigned char char_u;
typedef struct {
  UINT32_T total[2];
  UINT32_T state[8];
  char_u buffer[64];
} context_sha256_T;

void bf_key_init __ARGS((char_u *password, char_u *salt, int salt_len));
void bf_cfb_init __ARGS((char_u *iv, int iv_len));
void bf_crypt_encode __ARGS((char_u *from, size_t len, char_u *to));
void bf_crypt_decode __ARGS((char_u *ptr, long len));
void bf_crypt_init_keys __ARGS((char_u *passwd));
void bf_crypt_save __ARGS((void));
void bf_crypt_restore __ARGS((void));
int blowfish_self_test __ARGS((void));

void sha256_start __ARGS((context_sha256_T *ctx));
void sha256_update __ARGS((context_sha256_T *ctx, char_u *input, UINT32_T length));
void sha256_finish __ARGS((context_sha256_T *ctx, char_u digest[32]));
char_u *sha256_bytes __ARGS((char_u *buf, int buf_len, char_u *salt, int salt_len));
char_u *sha256_key __ARGS((char_u *buf, char_u *salt, int salt_len));
int sha256_self_test __ARGS((void));
void sha2_seed __ARGS((char_u *header, int header_len, char_u *salt, int salt_len));

#endif /* VIM__H */
