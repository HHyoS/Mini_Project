#include "verification.h"


int main() {
	init();
	while (1) {
		printf("HWANG >> ");
		if (invaild()) {
			char command[50];

			if (strcmp(input[0], "write") == 0) {
				sprintf(command, "./ssd W %s %s", input[1], input[2]);
				system(command);
			}
			else if (strcmp(input[0], "fullwrite") == 0) {
				for (int a = 0; a < 100; ++a) {
					sprintf(command, "./ssd W %d %s", a, input[1]);
					system(command);
				}
			}
			else if (strcmp(input[0], "read") == 0) {
				sprintf(command, "./ssd R %s ",input[1]);
				system(command);
			}
			else if (strcmp(input[0], "fullread") == 0) {
				FILE *fp = fopen("nand.txt","r");
				char output[21];
				for (int a = 0; a < 100; ++a) {
					fgets(output,20,fp);
					printf("%s",output);
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
			else if (strcmp(input[0], "exit") == 0) {
				printf("program exit!\n");
				break;
			}
			else if(strcmp(input[0], "test")==0){
				test(input[1]);
			}
		}
		else
			printf("INVALID COMMAND\n");

	}
}
