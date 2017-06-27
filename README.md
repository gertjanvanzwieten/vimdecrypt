# vimdecrypt

Command line tool for decrypting vim-blowfish-encrypted files.

As of version 7.3 vim offers strong built in blowfish encryption/decryption,
which for certain purposes is more convenient than filtering through gnupg.
Unfortunately the resulting files can only be read back by vim which makes it
hard to use them in batch processing or scripting. Also longevity of encrypted
data is a concern if a program with the dependencies and size of vim is
required to unlock it.

Vimdecrypt lifts two relevant files from the vim source, blowfish.c and
sha256.c, and builds on that a simple command line tool for file decryption.
Data is read from a file, decrypted data is written to stdout.

    vimdecrypt path_to_data

The password is obtained via GNU getpass which does not interfere with
stdin/stdout redirection.

Note 1. Vim's configure system is entirely stripped away which might have
broken support for other platforms than the 32 bit i386 linux it was developed
on. Since the two relevant files are taken from the vim project unmodified it
should be trivial to restore support on other platforms by fixing the vim.h
header.

Note 2. Recently, somebody with a better knowledge of cryptography developed a
[pure Python solution][1] using pycrypto. Since this is arguably a better
approach, the use if that module is recommended over the one featured here.

## installation

The command line tool can either be compiled as standalone executable, or
installed as a Python script that interfaces the C-routines via ctypes. In
addition the routines can be made available as Python module and/or dynamic
library.

C executable:

    src$ make vimdecrypt
    src$ cp vimdecrypt [directory_in_executable_path]
    $ vimdecrypt [somefile]

C library:

    src$ make libvimdecrypt.so
    src$ cp libvimdecrypt.so [directory_in_library_path]
    src$ cp libvimdecrypt.h [directory_in_header_path]
    $ gcc -lvimdecrypt [source.c]

Python (2/3) module, executable:

    src$ make libvimdecrypt.so
    src$ cp libvimdecrypt.so [directory_in_library_path]
    python$ python setup.py install (--user)
    $ vimdecrypt [somefile]
    >>> import vimdecrypt; s = vimdecrypt.decrypt('somefile')

[1]: https://github.com/nlitsme/vimdecrypt
