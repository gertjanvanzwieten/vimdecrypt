vimdecrypt: vimdecrypt.c blowfish.o sha256.o
	gcc $^ -o $@

libvimdecrypt.so: blowfish.o sha256.o
	gcc -shared -fPIC $^ -o $@

%.o: %.c
	gcc -O2 -fPIC -c $<

clean:
	rm -f *.o

.PHONY: clean
	
# vim:noexpandtab
