vimdecrypt: vimdecrypt.c sha256.c blowfish.c
	gcc -O2 vimdecrypt.c sha256.c blowfish.c -o vimdecrypt
	
# vim:noexpandtab
