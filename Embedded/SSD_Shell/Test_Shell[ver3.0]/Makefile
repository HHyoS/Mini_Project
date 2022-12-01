tShell : ssd run.o shell.o test.o verification.o
	gcc -o tShell run.o shell.o test.o verification.o

run.o : run.c run.h
	gcc -c run.c

shell.o : shell.c
	gcc -c shell.c

test.o : test.c
	gcc -c test.c

verification.o : verification.c
	gcc -c verification.c

ssd : ssd.o
	gcc -o ssd ssd.o

ssd.o : ssd.c
	gcc -c ssd.c

clear :
	rm - ./*.o nand.txt result.txt tShell ssd


