vimdecrypt
==========

Command line tool for decrypting vim-blowfish-encrypted files.

As of version 7.3 vim offers strong built in blowfish encryption/decryption,
which for certain purposes is more convenient than filtering through gnupg.
Unfortunately the resulting files can only be read back by vim which makes it
hard to use them in batch processing or scripting. Also longevity of encrypted
data is a concern if a program with the dependencies and size of vim is
required to unlock it.

Vimdecrypt lifts two relevant files from the vim source, blowfish.c and
sha256.c, and interfaces them in a simple command line tool. Data is read
from a file, decrypted data is written to stdout. 

    vimdecrypt path_to_data

The password is obtained via GNU getpass which does not interfere with
stdin/stdout redirection.

Vim's configure system is entirely stripped away which might have broken
support for other platforms than the 32 bit i386 linux it was developed on.
Since the two relevant files are taken from the vim project unmodified it
should be trivial to restore support on other platforms by fixing the vim.h
header.
