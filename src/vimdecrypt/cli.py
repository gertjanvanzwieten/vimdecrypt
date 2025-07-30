#!/usr/bin/env python3

import sys
from .vimdecrypt import decrypt

def main():
    if len(sys.argv) > 2:
        sys.exit('usage: vimdecrypt [path]')

    file = sys.argv[1] if len(sys.argv) == 2 else sys.stdin.buffer
    print(decrypt(file))

if __name__ == "__main__":
    main()

