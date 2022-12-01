#define _CRT_SECURE_NO_WARNINGS
#include "write.h"
#include <stdio.h>
#include <string.h>

void write() {

	FILE* fp1;
	FILE* fp2;
	fp1 = fopen("nand.txt", "r");
	fp2 = fopen("temp.txt", "w+");
	char buffer[100] = { 0 };

	for (int a = 0; fgets(buffer, sizeof(buffer), fp1) != NULL; ++a) {
		if (a == idx) {
			fprintf(fp2, "[%02d] %s\n", idx, nand[idx]);
		}
		else
			fputs(buffer, fp2);
	}
	fclose(fp1);
	fclose(fp2);
	remove("nand.txt");
	rename("temp.txt", "nand.txt");
}

void fullwrite() {
	init(input[1]);
}
