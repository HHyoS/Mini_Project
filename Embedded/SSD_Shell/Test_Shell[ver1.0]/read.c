#define _CRT_SECURE_NO_WARNINGS
#include "read.h"
#include <stdio.h>


void read() {
	int idx = atoi(input[1]);
	FILE* fp1;
	fp1 = fopen("result.txt", "w+");
	fprintf(fp1, "[%02d] %s\n", idx, nand[idx]);
	fclose(fp1);

}
void fullread() {
	for (int a = 0; a < 100; ++a) {
		printf("[%02d] %s\n", a,nand[a]);
	}
	FILE* fp1;
	fp1 = fopen("result.txt", "w+");
	fprintf(fp1, "[%02d] %s\n", 99, nand[99]);
	fclose(fp1);
}