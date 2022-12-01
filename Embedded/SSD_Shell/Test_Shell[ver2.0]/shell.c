#include <stdio.h>
#include <string.h>
#include <stdlib.h>



int main() {
	char input[200];
	init();
	while (1) {
		printf("LEE-HWANG >> ");
		fgets(input, sizeof(input), stdin);
		int leng = strlen(input);
		input[leng - 1] = '\0';

		char* ttmp;
		int size = 0;
		while (ttmp != NULL) {
			strcpy(input[size], ttmp);
			ttmp = strtok(NULL, " ");
			++size;
		}
		if (invaild()) {
			char command[50];

			if (strcmp(input[0], "write") == 0) {
				fprintf(command, "./ssd.c W %s %s", input[1], input[2]);
				system(command);
			}
			else if (strcmp(input[0], "fullwrite") == 0) {
				for (int a = 0; a < 100; ++a) {
					fprintf(command, "./ssd.c W %d %s", a, input[1]);
					system(command);
				}
			}
			else if (strcmp(input[0], "read") == 0) {
				fprintf(command, "./ssd.c R %s ",input[1]);
				system(command);
			}
			else if (strcmp(input[0], "fullread") == 0) {
				for (int a = 0; a < 100; ++a) {
					fprintf(command, "./ssd.c R %d %s", a, input[1]);
					system(command);
				}
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
