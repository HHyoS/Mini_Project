#include <stdio.h>
#include "common.h"


void ssd() {

	while (1) {
		printf("LEE-HWANG >> ");
		if (invaild()) {
			if (strcmp(input[0], "write") == 0) {
				write();
			}
			else if (strcmp(input[0], "fullwrite") == 0) {
				fullwrite();
			}
			else if (strcmp(input[0], "read") == 0) {
				read();
			}
			else if (strcmp(input[0], "fullread") == 0) {
				fullread();
			}
			else if (strcmp(input[0], "help") == 0) {
				printf("-------------------------------\n");
				printf("|----------- Menual -----------|\n");
				printf("| 1. write : write LBA Add     |\n");
				printf("| 2. fullwrite : fullwrite Add |\n");
				printf("| 3. read : read LBA           |\n");
				printf("| 4. fullread : fullread       |\n");
				printf("| 5. exit : exit               |\n");
				printf("-------------------------------\n");
			}
			else if ((strcmp(input[0]) == "exit") == 0) {
				printf("program exit!\n");
				break;
			}
		}
		else
			printf("INVALID COMMAND\n");

	}
}