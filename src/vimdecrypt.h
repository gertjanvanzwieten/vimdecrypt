#ifndef VIMDECRYPT__H
#define VIMDECRYPT__H

// Function definitions and data types implemented by the vimdecrypt
// library.

#include <unistd.h>

typedef struct {
  int method_nr;
  void *method_state; // method-specific state information
} cryptstate_T;

void crypt_blowfish_init(
  cryptstate_T *state,
  unsigned char* key,
  unsigned char* salt,
  int salt_len,
  unsigned char* seed,
  int seed_len );

void crypt_blowfish_decode(
  cryptstate_T *state,
  unsigned char *from,
  size_t len,
  unsigned char *to );

#endif /* VIMDECRYPT__H */
