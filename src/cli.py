#!/usr/bin/env python3

import sys
import vimdecrypt

def main():
    if len(sys.argv) > 2:
        sys.exit('usage: vimdecrypt [path]')

    print(vimdecrypt.decrypt(sys.argv[1] if len(sys.argv) == 2 else sys.stdin.buffer))

if __name__ == "__main__":
    main()

