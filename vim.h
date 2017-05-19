#ifndef VIM__H
#define VIM__H

// Minimal header file for compilation of unmodified blowfish.c and
// sha256.c from upream vim source.

#include "vimdecrypt.h"

#include <stdio.h>
#include <string.h>
#include <time.h>
#include <stdlib.h>

#define HAVE_CONFIG_H
#define OK 1
#define FAIL 0
#define FEAT_CRYPT
#define NUL '\000'
#define CRYPT_M_BF 1

#define _(x) (x)
#define __ARGS(x) x
#define STRLEN(s) strlen((char *)(s))
#define STRCPY(d,s) strcpy((char *)(d), (char *)(s))
#define EMSG(...) fprintf(stderr, __VA_ARGS__);
#define mch_memmove(to, from, len) memmove((char *)(to), (char *)(from), len)
#define vim_memset(ptr,c,size) memset((ptr), (c), (size))
#define alloc_clear(size) ((char_u *)calloc(size, sizeof(char_u)))

typedef unsigned int UINT32_T;
typedef unsigned char char_u;
typedef struct {
  UINT32_T total[2];
  UINT32_T state[8];
  char_u buffer[64];
} context_sha256_T;

char_u *sha256_key(char_u *buf, char_u *salt, int salt_len);
int sha256_self_test();
int blowfish_self_test();

#endif /* VIM__H */
