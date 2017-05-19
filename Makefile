vimdecrypt: vimdecrypt.c libvimdecrypt.so
	gcc -L. -lvimdecrypt vimdecrypt.c -o $@

libvimdecrypt.so: blowfish.o sha256.o
	gcc -shared -fPIC $^ -o $@

%.o: %.c
	gcc -O2 -fPIC -c $<

clean:
	rm -f *.o

.PHONY: clean
	
# vim:noexpandtab
