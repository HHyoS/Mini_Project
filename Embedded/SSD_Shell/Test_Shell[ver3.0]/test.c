#include "verification.h"

int check(char *tmp) {
	int flag = 0;
	int size = 0;
	int leng = strlen(tmp);
	tmp[leng-1] = '\0';
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
	if (flag == 1) {
		return 1;
	}

	return 0;
}
void test(char* fName) {

	FILE *fp = fopen(fName, "r+");

	char *command[100];
	char origin[100];
	for (int a = 0; fgets(command, sizeof(command), fp)!= NULL; ++a) {
		strcpy(origin,command);
		if (check(command)) 
		{
			int leng = strlen(origin);
			origin[leng-1] = '\0';	
			printf("if you want to execute the [ %s ] command, press 'y'\n",origin);
			char tmp;
			scanf(" %c",&tmp);
			if(tmp == 'y'){
				run();
			}
			else{
				printf("You didn't Press 'y', [ %s ] Do not run the Command.\n\n",origin);
			}
		}
	}
}
