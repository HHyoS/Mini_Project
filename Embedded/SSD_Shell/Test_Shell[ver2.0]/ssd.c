#define _CRT_SECURE_NO_WARNINGS
#include <stdio.h>
#include <stdlib.h>
#include <string.h>



int main(int index, char *argv[]) {
	
	FILE* ssd = fopen("nand.txt","w+");
	int idx = atoi(argv[2]);
	fseek(ssd, 16 * idx, SEEK_SET);
	if (strcmp(argv[1], "w") == 0) {
		fprintf(ssd, "[%02d] %s", idx, argv[3]);
		fclose(ssd);
	}
	else {
		FILE* result = fopen("result.txt", "w");
		char arr[20];
		fputs(fgets(arr, 16, ssd), result);
		fclose(result);
	}
	fclose(ssd);
}