# vimdecrypt

Command line tool for decrypting vim-blowfish-encrypted files.

As of version 7.3 vim offers built in blowfish encryption/decryption.
Unfortunately the resulting files can only be read back by vim, precluding
batch processing or scripting. Also longevity of encrypted data is a concern if
a program with the dependencies and size of vim is required to unlock it.

This project provides a very simpe `vimdecrypt` Python module for decrypting
blowfish-encoded file objects, as well as the `vimdecrypt` command line tool
for decrypting files to stdout.

## encryption methods

Vimdecrypt supports only blowfish2 encryption. Files encrypted using either zip
or blowfish should be converted using `:set cm=blowfish2` prior to using this
tool.

## requirements

Besides Python 3, vimdecrypt requires any one of
[PyCryto](https://pycrypto.org), [PyCryptoDome](https://www.pycryptodome.org)
or [blowfish](https://pypi.python.org/pypi/blowfish) to be installed.

## installation

Both the Python module and the command line tool are installable via Pip:

    $ pip install [--user]

This will install the `blowfish` module by default

## usage

With `~/.local/bin` in your executable path, decrypt any file to stdout using:

    $ vimdecrypt [path]

If the path argument is omitted then data is read from stdin:

    $ cat somefile | vimdecrypt

Note that the password is obtained via GNU getpass which does not interfere
with stdin/stdout redirection.

The Python module defines only the `decrypt` method:

    >>> import vimdecrypt
    >>> with open('somefile', 'rb') as f:
    >>>   text = vimdecrypt.decrypt(f)

## credits

Thanks to [@nlitsme](https://github.com/nlitsme) for demonstrating blowfish
decryption in Python. His identically named
[vimdecrypt](https://github.com/nlitsme/vimdecrypt) project supports multiple
encryption methods as well as password cracking.
