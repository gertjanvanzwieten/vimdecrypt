all: vimdecrypt blowfish.so

%.o: %.c
	gcc -O2 -c $<

vimdecrypt: vimdecrypt.o sha256.o blowfish.o
	gcc $^ -o $@

blowfish.so: blowfish.o sha256.o
	gcc -shared -fPIC $^ -o $@

clean:
	rm *.o

.PHONY: all clean
	
# vim:noexpandtab
