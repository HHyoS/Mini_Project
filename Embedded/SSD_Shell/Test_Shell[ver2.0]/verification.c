#define _CRT_SECURE_NO_WARNINGS

#include "verification.h"
#include <io.h>
//#include <unistd.h>

char input[10][101];
int idx;

int isNum(char* nums) {
	int leng = strlen(nums);

	for (int a = 0; a < leng; ++a) {
		if (nums[a] < '0' || nums[a]>'9')
			return 0;
	}
	int num = atoi(nums);
	idx = num;
	if (num < 0 || num >99)
		return 0;

	return 1;
}

int isAddress(char* add) {
	int leng = strlen(add);
	if (leng != 10)
		return 0;

	if (add[0] != '0' || add[1] != 'x')
		return 0;

	for (int a = 2; a < 10; ++a) {
		if ((add[a] >= '0' && add[a] <= '9') || (add[a] >= 'A' && add[a] <= 'F'))
			continue;
		return 0;
	}

	return 1;
}
int invaild() {

	int flag = 0;
	char tmp[50];
	fgets(tmp, 50, stdin);

	int size = 0;
	int leng = strlen(tmp);
	tmp[leng - 1] = '\0';
	char* ttmp = strtok(tmp, " ");

	while (ttmp != NULL) {
		strcpy(input[size], ttmp);
		ttmp = strtok(NULL, " ");
		++size;
	}
	if (size == 1) {
		if (strcmp(input[0], "help") == 0 || strcmp(input[0], "exit") == 0 || strcmp(input[0], "fullread") == 0)
			flag = 1;
	}
	else if (size == 2) {
		if (strcmp(input[0], "read") == 0) {
			if (isNum(input[1])) {
				flag = 1;
			}
		}
		else if (strcmp(input[0], "fullwrite") == 0) {
			if (isAddress(input[1])) {
				flag = 1;
			}
		}
	}
	else if (size == 3) {
		if (strcmp(input[0], "write") == 0) {
			if (isNum(input[1])) {
				if (isAddress(input[2])) {
					flag = 1;
				}
			}
		}
	}

	if (flag) {
		return 1;
	}

	return 0;
}
void init() {
	FILE* fp;
	if (access("nand.txt", 0)) {
		fp = fopen("nand.txt", "w+");
		for (int a = 0; a < 100; ++a) {
			fprintf(fp, "[%02d] 0x00000000\n", a);
		}
	}
	else {
		fp = fopen("nand.txt", "w+");
	}
	fclose(fp);
}